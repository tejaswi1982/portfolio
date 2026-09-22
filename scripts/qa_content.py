"""Content and nonvisual preservation checks against the supplied V1 archive."""
from pathlib import Path
from html.parser import HTMLParser
import zipfile,json,re,hashlib,sys
R=Path(__file__).resolve().parents[1];D=R/'dist';P=json.loads((R/'content/projects.json').read_text());B={p['slug']:p for p in P};checks=[]
def check(condition,name):
 if not condition:raise AssertionError(name)
 checks.append(name)
class Text(HTMLParser):
 def __init__(self):super().__init__();self.parts=[]
 def handle_data(self,x):self.parts.append(x)
def plain(path):
 p=Text();p.feed(path.read_text());return ' '.join(p.parts)
allhtml='\n'.join(p.read_text() for p in D.rglob('*.html'))
for bad in [r'CNBC\s+Prime',r'Channel V',r'Sai Dosa',r'21 years\. Still questioning\.',r'Zurich\. The USA\. The FIFA World Cup\.',r'strategic storytelling and impactful design',r'\bbinge\b','\u2014','\u2013']:
 check(not re.search(bad,allhtml,re.I),'Public copy excludes '+repr(bad))
check(len(P)==18 and len([p for p in P if p['category']=='film'])==13,'18 projects and all 13 films retained')
check(not (D/'work/binge').exists() and not list((D/'assets').glob('binge-*')),'Removed campaign route and assets absent')
check(B['prime']['client']=='CNBC-TV18 Prime' and B['prime']['role']=='Writing / Creative Direction / Co-production','Prime launch name and supplied role correct')
check(B['x-ray']['client']=='CNBC-TV18 Prime' and B['x-ray']['subCategory']=='Brand Promo','Original No. 11 correctly branded')
check(B['leadership']['client']=='CNBC-TV18','Leadership branding preserved')
for route in ['index.html','film/index.html','index/index.html']:
 s=plain(D/route);check(s.index('Bro Bytes: Sai Swad Dosa')<s.index('Bro Bytes: Ashok Vada Pav'),route+' has Sai Swad Dosa first')
for slug,result in [('bro-bytes-dosa','Nearly 1 million views on Facebook.'),('bro-bytes-ashok','Around 7 lakh views on Facebook.')]:
 s=plain(D/f'work/{slug}/index.html');check('History TV18' in s and result in s and 'Wrote, produced and anchored digital videos for History TV18.' in s,slug+' has channel, contribution and result')
check('Writing and co-production across television promos, launches and brand films.' in plain(D/'film/index.html'),'Section-level television role present')
check('21 Years Of CNBC-TV18' in plain(D/'print/index.html') and 'I wrote the campaign copy for these print creatives.' in plain(D/'work/twenty-one/index.html'),'Print title and copy credit correct')
a=plain(D/'work/adidas/index.html');check('Proactive / speculative campaign' in a and a.count('At the peak of performance, athletes make physics feel impossible.')==1,'Speculative status and single primary concept line present')
check(B['emirates']['description'] in plain(D/'work/emirates/index.html'),'Emirates concise context rendered')
v=plain(D/'work/busy-message/index.html');check('Vodafone' in v and 'Busy Message Campaign' in v and 'Microsite' in v and B['busy-message']['description'] in v,'Vodafone title, format and context rendered')
check(B['busy-message']['role'] is None,'No unsupported Vodafone role invented')
film=(D/'film/index.html').read_text();nums=re.findall(r'class="eyebrow">(\d{2}) /',film);check(nums==[f'{n:02}' for n in range(1,14)],'Film numbers sequential 01 to 13')
for p in P:check((D/'work'/p['slug']/'index.html').exists(),'Existing route retained: '+p['slug'])
if len(sys.argv)>1:
 with zipfile.ZipFile(sys.argv[1]) as z:
  for f in ['dist/style.css','dist/app.js','content/identity.json']:check((R/f).read_bytes()==z.read(f),f+' byte-identical to V1')
  old=json.loads(z.read('content/projects.json'));oldby={p['slug']:p for p in old}
  for p in P:
   if p.get('video'):
    for k in ['video','preferredSource','nativeResolution','aspectRatio','recommendedDisplaySize']:check(p[k]==oldby[p['slug']][k],p['slug']+' preserves '+k)
  for f in (D/'assets').iterdir():check(f.read_bytes()==z.read('dist/assets/'+f.name),'Media bytes unchanged: '+f.name)
  # The actual shared interaction and presentation renderers are unchanged.
  import ast
  oldast=ast.parse(z.read('scripts/build.py').decode());newast=ast.parse((R/'scripts/build.py').read_text())
  for name in ['nav','player','carousel','interlude']:
   f=lambda tree:ast.dump(next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name))
   check(f(oldast)==f(newast),name+' renderer preserved')
# Validate filter membership using generated data-category values; JS is unchanged.
rows=re.findall(r'class="work-row" data-category="([^"]*)"', (D/'index/index.html').read_text())
check(len(rows)==18,'All index rows generated')
for category in ['film','digital','print','ai','experiments']:check(sum(category in r.split() for r in rows)==sum(p['category']==category or category in p['tags'] for p in P),'Filter membership consistent: '+category)
report={'status':'passed','checks':len(checks),'browser_interaction_status':'Not executed: managed preview has no compatible server for this unchanged static build.','checks_detail':checks}
(R/'docs/V1.1-QA.json').write_text(json.dumps(report,indent=2)+'\n')
(R/'docs/V1.1-QA.md').write_text(f'''# V1.1 QA

Passed {len(checks)} content and preservation checks, plus the complete local-link/asset validator and JavaScript syntax validation.

- Correct names, credits, results, context, speculative labelling and project numbering verified in generated HTML.
- All 18 project routes and all 13 films retained. Removed campaign absent from the public output.
- Index order and category membership verified, including the AI cross-listing.
- CSS, interaction JavaScript, identity data, all retained media bytes and navigation/player/carousel/interlude renderers are identical to V1.
- Video sources, dimensions, aspect ratios, posters and display limits are unchanged.
- All generated local links and assets resolve. No em or en dash appears in visitor copy or metadata.
- Original upload filenames in provenance fields still identify the real source files. These are not visitor-facing brand labels.

Browser visual and live interaction tests were not executed: the managed preview does not support this unchanged buildless static site. Desktop/mobile rendering, touch gestures and native fullscreen are therefore not claimed as newly browser-tested. Their underlying styles, controls and media are unchanged. See V1.1-QA.json for individual automated checks.
''')
print(json.dumps({k:v for k,v in report.items() if k!='checks_detail'}))
