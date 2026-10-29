import sys; sys.path.insert(0,'/opt/chip-flow/engine/lib')
import layoutlib as L
df, dr = L.gf180_cells()
for kind, kw in [("n", dict(l_gate=2, w_gate=10, nf=1)), ("n", dict(l_gate=2, w_gate=10, nf=3)), ("p", dict(l_gate=0.28, w_gate=2, nf=2)),("n", dict(l_gate=0.28, w_gate=1, nf=1))]:
    c = (df.draw_nfet if kind=="n" else df.draw_pfet)(**kw)
    print(kind, kw, "bbox", c.dbbox())
    for name, lay in L.GF180_LAYER.items():
        b = L.layer_boxes(c, lay)
        if b: print("  ", name, b)
    print("  poly", L.layer_boxes(c,(30,0)))
