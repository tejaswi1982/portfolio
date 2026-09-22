from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import json
R=Path(__file__).resolve().parents[1];D=R/'dist';errors=[];count=0
class Check(HTMLParser):
 def __init__(self,path):super().__init__();self.path=path;self.ids=set();self.fragments=[]
 def handle_starttag(self,tag,attrs):
  global count
  a=dict(attrs)
  if 'id' in a:self.ids.add(a['id'])
  if tag=='img' and a.get('src') and not all(k in a for k in ['alt','width','height']):errors.append(f'{self.path}: incomplete image metadata')
  if tag=='video' and any(k not in a for k in ['controls','playsinline','preload','poster','width','height']):errors.append(f'{self.path}: incomplete video attributes')
  if tag=='video' and 'autoplay' in a:errors.append(f'{self.path}: unintended autoplay')
  for key in ['src','href','poster']:
   value=a.get(key,'')
   if value.startswith('#'):self.fragments.append(value[1:]);continue
   if not value.startswith('/'):continue
   path=D/urlsplit(value).path.lstrip('/')
   if not path.exists():errors.append(f'{self.path}: missing {value}')
   elif path.is_dir() and not (path/'index.html').exists():errors.append(f'{self.path}: missing page {value}')
   count+=1
for f in D.rglob('*.html'):
 text=f.read_text();parser=Check(f.relative_to(D));parser.feed(text)
 for frag in parser.fragments:
  if frag not in parser.ids:errors.append(f'{f}: missing anchor {frag}')
 if '\u2014' in text:errors.append(f'{f}: em dash')
 if '<title>' not in text or 'name="description"' not in text:errors.append(f'{f}: missing metadata')
projects=json.loads((R/'content/projects.json').read_text())
assert len([p for p in projects if p['category']=='film'])==13
assert len({p['slug'] for p in projects})==len(projects)
assert len(next(p for p in projects if p['slug']=='busy-message')['assets'])==7
for f in (D/'assets').iterdir():
 if f.stat().st_size>=25*1024*1024:errors.append(f'Host file-size limit: {f}')
report={'pages':len(list(D.rglob('*.html'))),'local_references_checked':count,'projects':len(projects),'films':13,'errors':errors,'browser_review':'Not run: buildless static preview unsupported in this managed environment.'}
(R/'docs/site-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
raise SystemExit(bool(errors))
