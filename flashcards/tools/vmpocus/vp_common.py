"""Utilitários comuns dos cards VM/POCUS."""
def c(sp, ctx, dx, crit, cond, peg): return dict(sp=sp, ctx=ctx, dx=dx, crit=crit, cond=cond, peg=peg, q=None)
def vm(**k): k["kind"] = "vm"; return k
def b(scene, sub="", **args): return dict(kind="b", scene=scene, args=args, sub=sub)
def pair(sa, aa, sb, ab, la, lb, sub=""): return dict(kind="pair", a=(sa, aa), b=(sb, ab), la=la, lb=lb, sub=sub)
def mml(kind, sub="Modo M · pulmão (linear, tórax anterior)", **p): return dict(kind="mml", mk=kind, sub=sub, p=p)
def mmt(kind, sub="", **p): return dict(kind="mmt", mk=kind, sub=sub, p=p)
def dop(kind, sub="", **p): return dict(kind="dop", dk=kind, sub=sub, p=p)
