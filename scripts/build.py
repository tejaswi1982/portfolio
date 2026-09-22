"""Build static, individually addressable portfolio pages from content data."""
from pathlib import Path
import json,html,shutil
R=Path(__file__).resolve().parents[1];D=R/'dist';P=json.loads((R/'content/projects.json').read_text());I=json.loads((R/'content/identity.json').read_text());by={p['slug']:p for p in P}
BASE='https://portfolio.abhinandantejaswi.com'
# Keep experiments available in the model, but hidden until it has distinct work.
PUBLIC_CATEGORIES=('film','digital','print','ai')
def e(s):return html.escape(str(s),quote=True)
def url(p):return '/work/'+p['slug']+'/'
def display_title(p):return '<br>'.join(e(line) for line in p.get('titleLines',[p['title']]))
def image(a,cls='',eager=False):
 src=a['src'];stem=src[:-5]
 return f'<img class="{cls}" src="{src}" srcset="{stem}-480.webp {min(a["width"],480)}w, {stem}-800.webp {min(a["width"],800)}w, {src} {min(a["width"],1600)}w" sizes="(max-width: 700px) 92vw, 80vw" width="{a["width"]}" height="{a["height"]}" alt="{e(a["alt"])}" loading="{"eager" if eager else "lazy"}" decoding="async">'
def head(title,desc,path):
 full_title = 'Abhinandan Tejaswi | Creative Director, Writer, Film and Digital' if path=='/' else title+' | Abhinandan Tejaswi'
 project=by.get(path.strip('/').split('/')[-1]) if path.startswith('/work/') else None
 social=(project.get('poster') or project.get('heroAsset')) if project else '/og.png'
 social_alt=project['title'] if project else 'Abhinandan Tejaswi. Creative Direction. Writing. Film. Digital. Ideas.'
 return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{e(full_title)}</title><meta name="description" content="{e(desc)}"><meta name="theme-color" content="#eeeae1"><link rel="canonical" href="{BASE}{path}"><meta property="og:type" content="website"><meta property="og:title" content="{e(full_title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{BASE}{path}"><meta property="og:image" content="{BASE}{social}"><meta property="og:image:alt" content="{e(social_alt)}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(full_title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{BASE}{social}"><meta name="twitter:image:alt" content="{e(social_alt)}"><link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'%3E%3Crect width='40' height='40' fill='%23c84322'/%3E%3Ctext x='7' y='29' font-family='Arial' font-size='27' fill='%23eeeae1'%3Ea.%3C/text%3E%3C/svg%3E"><link rel="stylesheet" href="/style.css"><script type="module" src="/app.js"></script></head><body><a class="skip" href="#main">Skip to work</a>'''
def nav(active='selected'):
 links=[('selected','Selected','/'),('film','Film','/film/'),('digital','Digital','/digital/'),('print','Print','/print/'),('ai','AI','/ai/'),('index','Index','/index/'),('about','About','/about/')]
 return '<header class="nav"><a class="wordmark" href="/" aria-label="Abhinandan Tejaswi home">at<span>.</span></a><nav aria-label="Portfolio">'+''.join(f'<a href="{u}" {"aria-current=page" if k==active else ""}>{label}</a>' for k,label,u in links)+'</nav><span class="nav-location">Mumbai, India</span></header>'
def footer():return '''<footer><a class="footer-name" href="/about/">Abhinandan Tejaswi<span>Creative Direction. Writing. Making.</span></a><div><a href="https://abhinandantejaswi.com" target="_blank" rel="noopener" aria-label="Say hello via the main site">Say hello ↗</a><a href="/index/">Work index ↗</a><p>© 2026 Abhinandan Tejaswi</p></div><a class="backtop" href="#top" aria-label="Back to top">↑</a></footer><dialog id="lightbox" aria-label="Enlarged artwork"><button class="close-lightbox" aria-label="Close enlarged artwork">Close ×</button><img alt=""><p></p></dialog></body></html>'''
def chapter(n,title,extra=''):return f'<div class="chapter"><span>{n} / {title}</span><span>{extra}</span></div>'
def duration(v):return f'{int(v["duration"])//60:02d}:{int(v["duration"])%60:02d}'
def player(p):
 v=p['video'];arch=v['height']<=576
 return f'''<div class="film-player {'archive' if arch else ''}" style="--display:{p['recommendedDisplaySize']}px"><video controls playsinline preload="none" poster="{v['poster']}" width="{v['width']}" height="{v['height']}" aria-label="Play {e(p['title'])}"><source src="{v['src']}" type="video/mp4"><a href="{v['src']}">Open film</a></video><div class="player-meta"><span>{'ARCHIVE / ' if arch else ''}{v['width']} × {v['height']}</span><span>{duration(v)} / SOUND ON</span></div></div>'''
def result_line(p):return f'<p>{e(p["result"])}</p>' if p.get("result") else ""
def selected_note(p):return f'<p class="selected-note">{e(p["selectedNote"])}</p>' if p.get('selectedNote') else ''
def card(slug,cls=''):
 p=by[slug];v=p.get('video');a=next((a for a in p['assets'] if a.get('src')==p['heroAsset']),None)
 media=(f'<img src="{p["poster"]}" width="{v["width"]}" height="{v["height"]}" alt="{e(p["title"])} film still" loading="lazy">' if v else image(a))
 return f'''<article class="project-card {cls}"><a class="art-link" href="{url(p)}">{media}<span class="open-art">{'Play film' if v else 'View project'} ↗</span></a><div class="card-caption"><div><span class="eyebrow">{e(p['client'])} / {e(p['subCategory'])}</span><h3><a href="{url(p)}">{display_title(p)}</a></h3>{selected_note(p)}</div><span class="card-arrow" aria-hidden="true">↗</span></div></article>'''
def enlarge(a):return f'<button class="enlarge" data-enlarge="{a["src"]}" data-caption="{e(a["alt"])}" aria-label="Enlarge: {e(a["alt"])}">{image(a)}<span>Enlarge ↗</span></button>'
def carousel(p):
 return '<section class="carousel" tabindex="0" aria-label="Vodafone Busy Message screen sequence" aria-roledescription="carousel"><div class="browser-bar"><span>Vodafone / Busy Message</span><span>Interactive archive</span></div><div class="slides">'+''.join(f'<figure class="slide" aria-label="Screen {i+1} of {len(p["assets"])}">{enlarge(a)}<figcaption><span>{i+1:02d}</span> {e(a["alt"])}</figcaption></figure>' for i,a in enumerate(p['assets']))+f'</div><div class="carousel-tools"><p>Seven screens. One experience.</p><div><button data-step="-1" aria-label="Previous screen">←</button><span class="counter" aria-live="polite">01 / {len(p["assets"]):02d}</span><button data-step="1" aria-label="Next screen">→</button></div></div></section>'
def interlude(i,line):return f'<figure class="detour">{image(I["photos"][i])}<figcaption><span>{line}</span><span>Field notes / {i+1:02d}</span></figcaption></figure>'
def table(projects,filters=False):
 fs='<div class="filters" role="group" aria-label="Filter work">'+''.join(f'<button data-filter="{x}" aria-pressed="{str(x=="all").lower()}">{x.title()}</button>' for x in ['all',*PUBLIC_CATEGORIES])+'</div>' if filters else ''
 return fs+'''<div class="work-table"><div class="table-head"><span>Project</span><span>Client</span><span>Year</span><span>Format</span><span></span></div>'''+''.join(f'<a class="work-row" data-category="{p["category"]} {" ".join(p["tags"])}" href="{url(p)}"><span>{e(p["title"])}</span><span>{e(p["client"])}</span><span>{p["year"] or ""}</span><span>{e(p["subCategory"])}</span><span aria-hidden="true">↗</span></a>' for p in projects)+'</div><p class="filter-result" aria-live="polite"></p>'
def save(path,title,desc,body,active):
 dest=D/path.strip('/')/'index.html' if path!='/' else D/'index.html';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(head(title,desc,path)+'<div id="top"></div>'+nav(active)+'<main id="main">'+body+'</main>'+footer())
hero=f'''<section class="identity"><div class="hero-note eyebrow">Independent creative practice / Selected work</div><div class="portrait">{image(I['portrait'],eager=True)}<span class="portrait-coordinate">01 / A WORK IN PROGRESS</span></div><div class="identity-copy"><h1>ABHINANDAN<br>TEJASWI<span>.</span></h1><p class="disciplines">Creative Direction. Writing.<br>Film. Digital. Ideas.</p><p class="intro">Twenty-something years of making things<br class="desktop-br"> people might actually watch.</p><a class="start" href="#first-film">Start somewhere <span>↓</span></a></div><span class="margin-note">The long way around.</span></section>'''
p=by['prime']
body=hero+f'''<section class="hero-film section" id="first-film">{chapter('01','A place to begin','Film / 00:45')}<div class="section-title"><h2>A different<br><em>perspective.</em></h2><a class="text-link" href="{url(p)}">{e(p['title'])} / {e(p['subCategory'])} ↗</a></div>{player(p)}</section>'''
body+=f'''<section class="section selected">{chapter('02','Selected work','Different formats. Same curiosity.')}<div class="editorial-grid">{card('bro-bytes-dosa','wide')}{card('twenty-one','paper')}{card('corner-seat','small')}<div class="selection-note"><span class="orange">↳</span><p>The medium<br>keeps changing.</p><a class="text-link" href="/film/">All 13 films ↗</a></div>{card('mad-about-markets','offset')}{card('awaaz','narrow')}</div></section>'''
body+='''<section class="type-interlude"><span class="eyebrow">A note on the way</span><p>Some were 30 seconds.<br>Some were websites.<br>Some were printed.<br><em>Some didn’t have<br>a format yet.</em></p><span class="annotation">Keep going. ↓</span></section>'''
body+=interlude(0,'THERE WERE DETOURS.')
body+=f'''<section class="section digital-feature">{chapter('03','The early internet','Digital / Interactive')}<div class="section-title"><h2>Made to<br><em>be clicked.</em></h2><div><p>{e(by['busy-message']['description'])}</p><a class="text-link" href="/work/busy-message/">The project ↗</a></div></div>{carousel(by['busy-message'])}<div class="digital-pair">{card('zoozoo')}<div class="digital-aside"><span class="eyebrow">Emirates / Animated banners</span><h3>A world in<br>a small window.</h3>{banner(by['emirates']['assets'][0]) if False else ''}<video controls playsinline muted preload="none" width="320" height="266" poster="{by['emirates']['assets'][0]['poster']}" aria-label="Emirates Zurich banner"><source src="{by['emirates']['assets'][0]['src']}" type="video/mp4"></video><a class="text-link" href="/work/emirates/">Explore the three banners ↗</a></div></div></section>'''
body+=f'''<section class="section print-feature">{chapter('04','Off the screen','Print / Campaigns')}<div class="section-title"><h2>Worth<br><em>a second look.</em></h2><a class="text-link" href="/print/">Print archive ↗</a></div><div class="print-pair">{''.join(enlarge(a) for a in by['twenty-one']['assets'])}</div><div class="caption-line"><h3>{e(by["twenty-one"]["title"])}</h3><a href="/work/twenty-one/">Print campaign / Three executions ↗</a></div></section>'''
body+=interlude(1,'SOMEWHERE BETWEEN ONE THING AND THE NEXT.')
body+=f'''<section class="section new-media-feature">{chapter('05','No brief required','Proactive / Speculative')}<div class="section-title"><h2>adidas<br><em>Physics of Performance</em></h2><div><p>{e(by["adidas"]["headline"])}</p><span class="eyebrow">{e(by["adidas"]["subCategory"])}</span></div></div><div class="adidas-spread">{''.join(enlarge(a) for a in by['adidas']['assets'])}</div><div class="caption-line"><p>AI-assisted imagery. A self-initiated concept.<br>Not commissioned by Adidas.</p><a class="text-link" href="/work/adidas/">Explore the idea ↗</a></div></section>'''
body+='''<section class="new-medium"><span class="eyebrow">06 / The next medium</span><h2>Another tool.<br><em>The same curiosity.</em></h2><p>Ideas, art direction and storytelling.<br>Now with a few new ways to make them.</p><a class="text-link" href="/ai/">AI-assisted work ↗</a></section>'''
body+=f'<section class="section">{chapter("07","Find your own way","The complete index")}<h2 class="index-heading">There’s more.</h2>{table(P,True)}</section>'
save('/','Creative direction. Writing. Film. Digital.','Selected creative work by Abhinandan Tejaswi, across television, film, digital, print and new media.',body,'selected')
for cat,title,desc in [('film','Moving pictures.','Writing and co-production across television promos, launches and brand films.'),('digital','Made to be clicked.','Microsites, animated banners and a few pieces of internet history.'),('print','Off the screen.','Campaigns made to be read, noticed and looked at again.'),('ai','Another way to make.','New tools inside a longer creative practice.')]:
 ps=[p for p in P if p['category']==cat or cat in p['tags']];ps=sorted(ps,key=lambda x:x['priority'])
 b=f'<section class="section collection"><span class="eyebrow">{cat.upper()} / {len(ps):02d} PROJECTS</span><h1>{title}</h1><p class="collection-intro">{desc}</p>'
 if cat=='film':
  b+='<div class="film-list">'
  for n,p in enumerate(ps):b+=f'<div class="film-entry"><div><span class="eyebrow">{n+1:02d} / {e(p["client"])}</span><h2><a href="{url(p)}">{e(p["title"])} ↗</a></h2><p>{e(p["subCategory"])}</p>{result_line(p)}</div>{player(p)}</div>'
  b+='</div>'
 elif cat=='digital':
  b+=f'<h2 class="collection-subtitle">{e(by["busy-message"]["client"])} / {e(by["busy-message"]["title"])}</h2><p>{e(by["busy-message"]["subCategory"])}</p><p>{e(by["busy-message"]["description"])}</p>{carousel(by["busy-message"])}<a class="text-link" href="/work/busy-message/">Project notes ↗</a><div class="digital-pair">{card("zoozoo")}<div class="digital-aside"><h2>Emirates</h2><p>{e(by["emirates"]["description"])}</p><a class="text-link" href="/work/emirates/">Watch the banners ↗</a></div></div>'
 else:
  for p in ps:
   b+=f'<div class="collection-project"><div class="caption-line"><h2><a href="{url(p)}">{display_title(p)} ↗</a></h2><span class="eyebrow">{e(p["client"])} / {e(p["subCategory"])}</span></div><div class="{"adidas-spread" if p["slug"]=="adidas" else "print-pair"}">'+''.join(enlarge(a) for a in p['assets'])+'</div>'+(f'<p>{e(p["note"])}</p>' if p['note'] else '')+(f'<p>{e(p["description"])}</p>' if cat=='print' else '')+'</div>'
 b+='</section>';save('/'+cat+'/',{'film':'Film and television','digital':'Digital and interactive','print':'Print campaigns','ai':'AI and new media'}[cat],desc,b,cat)
for n,p in enumerate(P):
 b=f'<article class="project-detail section"><a class="breadcrumb" href="/{p["category"]}/">← {p["category"].title()}</a><div class="project-intro"><span class="eyebrow">{e(p["client"])} / {e(p["subCategory"])}</span><h1>{display_title(p)}</h1><p>{e(p["headline"])}</p></div>'
 if p.get('video'):b+=player(p)
 elif p['projectType']=='carousel':b+=carousel(p)
 elif p['projectType']=='banners':
  b+='<div class="banners">'+''.join(f'<figure><div class="banner-label">{a["alt"]} / 320 × 266</div><video controls playsinline muted preload="none" width="320" height="266" poster="{a["poster"]}" aria-label="Emirates {a["alt"]} banner"><source src="{a["src"]}" type="video/mp4"></video><figcaption>{a["alt"]}</figcaption></figure>' for a in p['assets'])+'</div>'
 else:b+='<div class="project-art '+('adidas-spread' if p['slug']=='adidas' else '')+'">'+''.join(enlarge(a) for a in p['assets'])+'</div>'
 b+=f'<div class="project-notes"><div>'+ (f'<span class="eyebrow">The context</span><p>{e(p["description"])}</p>' if p['description'] != p['headline'] else '') + result_line(p) +(f'<span class="eyebrow">A note</span><p>{e(p["note"])}</p>' if p['note'] else '')+'</div><dl><dt>Client / context</dt><dd>'+e(p['client'])+'</dd><dt>Format</dt><dd>'+e(p['subCategory'])+'</dd>'+(f'<dt>AI Tools</dt><dd>{e(", ".join(p["aiTools"]))}</dd>' if p.get('aiTools') else '')+(f'<dt>Year</dt><dd>{p["year"]}</dd>' if p['year'] else '')+(f'<dt>My role</dt><dd>{e(p["role"])}</dd>' if p['role'] else '')+(f'<dt>Duration</dt><dd>{duration(p["video"])}</dd>' if p.get('video') else f'<dt>Executions / screens</dt><dd>{len(p["assets"])}</dd>')+'</dl></div>'
 nxt=P[(n+1)%len(P)];b+=f'<a class="next-project" href="{url(nxt)}"><span class="eyebrow">Next turn</span><span>{e(nxt["title"])} ↗</span></a></article>'
 save(url(p),p['title'],p['description'],b,p['category'])
save('/index/','Work index','Browse the creative archive by medium.',f'<section class="section index-page"><span class="eyebrow">The archive / {len(P)} projects</span><h1>Pick a thread.</h1>{table(P,True)}</section>','index')
about=f'''<section class="section about"><div>{image(I['portrait'])}</div><div><span class="eyebrow">A little context</span><h1>Still<br><em>curious.</em></h1><h2>Abhinandan Tejaswi</h2><p>Creative Director. Writer. Maker.</p><p>Twenty-something years across television, promos, film, advertising, digital and new media.</p><p>The formats change. The pleasure of finding an idea, and finding a way to make it, stays.</p><p>Mumbai, India.</p><a class="text-link" href="https://abhinandantejaswi.com" target="_blank" rel="noopener">Main site ↗</a></div></section>'''
save('/about/','About','Abhinandan Tejaswi. Creative Director, Writer and Maker. Mumbai, India.',about,'about')
save('/404/','Page not found','Find your way back to the work.','<section class="section"><span class="eyebrow">An unexpected detour / 404</span><h1>Wrong turn.</h1><a class="text-link" href="/">Back to selected work ↗</a></section>','')
(D/'404.html').write_text((D/'404/index.html').read_text())
(D/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+BASE+'/sitemap.xml\n')
paths=['/','/film/','/digital/','/print/','/ai/','/index/','/about/']+[url(p) for p in P]
(D/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+BASE+p+'</loc></url>' for p in paths)+'</urlset>')
shutil.rmtree(D/'experiments',ignore_errors=True)
print('Built',len(paths),'routes.')
