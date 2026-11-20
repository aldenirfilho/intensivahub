import re, sqlite3, zipfile, json, sys
sys.path.insert(0,'.')
import build
z=zipfile.ZipFile('out/Escrituras_Axiomas_360X_1141_flashcards.apkg'); z.extract('collection.anki2','/tmp/rc')
db=sqlite3.connect('/tmp/rc/collection.anki2')
rows={r[0].split('\x1f')[0]:r[0].split('\x1f') for r in db.execute('select flds from notes')}
def render(t,f):
    d=dict(zip(build.CAMPOS,f))
    t=re.sub(r'{{#(\w+)}}(.*?){{/\1}}',lambda m:m.group(2) if d.get(m.group(1)) else '',t,flags=re.S)
    return re.sub(r'{{(\w+)}}',lambda m:d.get(m.group(1),''),t)
ids=sys.argv[1:]
body=''
for i in ids:
    f=rows[i]
    body+=f'<div class="card" style="display:flex;gap:10px"><div style="flex:1">{render(build.FRENTE1,f)}</div><div style="flex:1">{render(build.VERSO1,f)}</div></div>'
open('/tmp/rc/prev.html','w').write(f'<html><head><meta charset=utf-8><style>{build.CSS} body{{background:#0b0f16;margin:0}}</style></head><body>{body}</body></html>')
