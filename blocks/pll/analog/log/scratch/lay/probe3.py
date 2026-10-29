import sys; sys.path.insert(0,'/opt/chip-flow/engine/lib')
import layoutlib as L
df, dr = L.gf180_cells()
for kind, kw in [("n", dict(l_gate=0.28, w_gate=1, gate_con_pos="top")),("p", dict(l_gate=0.5, w_gate=5, gate_con_pos="top")),("p", dict(l_gate=10, w_gate=0.5, gate_con_pos="top")),("n", dict(l_gate=2, w_gate=0.5, gate_con_pos="top"))]:
    c = (df.draw_nfet if kind=="n" else df.draw_pfet)(**kw)
    print(kind, kw, "bbox", c.dbbox())
    for name in ["comp","poly2","metal1","nwell","nplus","pplus"]:
        print("  ",name, L.layer_boxes(c, L.GF180_LAYER[name]))
