import glob,re,sys
from curate360 import curate, strip
nums=sys.argv[1].split(','); out=[]
for n in nums:
    p=glob.glob(f'/home/claude/app2/data/decks/ia360-temi-2028-{n}-*.json')[0]
    d,tema,cards=curate(p); out.append(f"##### {tema} ({len(d['cards'])} → {len(cards)})")
    for c in cards:
        v=c['verso'].replace('</td></tr>',' ¦ ').replace('</th><td>',': ')
        out.append(f"{c['_k'].split('#')[1]} [{c['subtema']}] {strip(c['frente'])} => {strip(v)}{' || '+strip(c['pegadinha']) if c['pegadinha'] and not c['pegadinha'].startswith('Conceito') else ''}")
open(sys.argv[2],'w').write("\n".join(out)); print(len(out), sum(map(len,out)))
