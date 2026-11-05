def C(f, b, x="", s="", i=""):
    return dict(f=f, b=b, x=x, s=s, i=i)

def T(*rows):
    h = "<table class=t><tr>" + "".join(f"<th>{c}</th>" for c in rows[0]) + "</tr>"
    for r in rows[1:]:
        h += "<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>"
    return h + "</table>"

def L(*items):
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"
