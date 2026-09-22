"""Refresh media from the current content records without overwriting editorial copy.
Usage: python3 scripts/prepare_assets.py SOURCE_DIR
Requires Pillow, ffmpeg. Original filenames are retained in content as provenance.
"""
from pathlib import Path
import json,sys,subprocess
from PIL import Image,ImageOps
R=Path(__file__).resolve().parents[1];S=Path(sys.argv[1]);D=R/'dist';P=json.loads((R/'content/projects.json').read_text());I=json.loads((R/'content/identity.json').read_text())
def image(a):
 im=ImageOps.exif_transpose(Image.open(S/a['source'])).convert('RGB');out=D/a['src'].lstrip('/');out.parent.mkdir(parents=True,exist_ok=True)
 for cap,suffix in [(1600,''),(800,'-800'),(480,'-480')]:
  cp=im.copy();cp.thumbnail((cap,cap*2));cp.save(out.with_name(out.stem+suffix+'.webp'),'WEBP',quality=88)
for p in P:
 if p.get('video'):
  out=D/p['video']['src'].lstrip('/');out.parent.mkdir(parents=True,exist_ok=True)
  subprocess.run(['ffmpeg','-v','error','-i',str(S/p['preferredSource']),'-map','0:v:0','-map','0:a?','-c','copy','-movflags','+faststart','-y',str(out)],check=True)
  # Keep the curated poster; do not silently choose a different frame.
 for a in p['assets']:
  if a.get('source'):image(a)
  # Banner captures and curated posters already in dist are retained.
image(I['portrait'])
for a in I['photos']:image(a)
print('Refreshed media. Project copy, ordering, sources, dimensions and curated posters preserved.')
