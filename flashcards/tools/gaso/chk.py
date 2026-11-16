import sys, importlib
sys.path.insert(0, ".")
from gaso_cards import render
for mod in sys.argv[1:]:
    m = importlib.import_module(mod)
    for name in [x for x in dir(m) if x.startswith("T") and x[1:].isdigit()]:
        tit, cards = getattr(m, name); print(f"== {name} {tit}: {len(cards)} cards")
        for i, c in enumerate(cards, 1):
            if c["kind"] == "caso":
                try:
                    fr, vs, R = render(c, i)
                    print(f"  {i:2d} pH {R['lab']['ph']} {'+'.join(R['codes'])} AGc={R['agc'] if R['agc'] is None else round(R['agc'],1)} dd={round(R['dd'],2) if 'dd' in R else '-'}")
                except AssertionError as e: print("  ❌", e)
