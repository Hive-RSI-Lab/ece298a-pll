import sys; sys.path.insert(0,'/opt/chip-flow/engine/lib')
import layoutlib as L
import klayout.db as kdb
df, dr = L.gf180_cells()
c = dr.draw_ppolyf_res(l_res=30, w_res=1, res_type="ppolyf_u")
print("bbox", c.dbbox())
for li in c.kcl.layer_indexes():
    info=c.kcl.get_info(li)
    b=L.layer_boxes(c,(info.layer,info.datatype))
    if b: print(info.layer, info.datatype, b[:6], len(b))
