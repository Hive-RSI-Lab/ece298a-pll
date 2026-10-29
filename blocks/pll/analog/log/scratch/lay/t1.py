import sys; sys.path.insert(0,'.'); import harness
sys.path.insert(0,'/opt/chip-flow/engine/lib'); import layoutlib as L
import gdsfactory as gf
df, dr = L.gf180_cells()
from cells.draw_cap_mim import draw_cap_mim
top=gf.Component()
M1=L.GF180_LAYER["metal1"]; LBL=L.GF180_LAYER["metal1_label"]
segs=[]
for i in range(2):
    r=top.add_ref(dr.draw_ppolyf_res(l_res=10, w_res=1, res_type="ppolyf_u")); r.rotate(90); r.move((i*3.0,0))
# rotated: body x -1..0 (+i*3), y 0..10 ; heads y -0.52..-0.14 & 10.14..10.52 at x -0.69..-0.31
L.rect(top,-0.69,-0.52,3-0.31,-0.14,M1)   # bottom strap
L.rect(top,-0.69,10.14,-0.31,11.5,M1); L.rect(top,3-0.69,10.14,3-0.31,11.5,M1)
L.rect(top,-0.69-0.3,-1.89,3.0,-1.51,M1)  # sub taps bar? 
cap=top.add_ref(draw_cap_mim(mim_option="MIM-B", metal_level="M5", lc=10, wc=10)); cap.move((10,0))
labels=[("a",-0.5,11.3,LBL),("b",2.5,11.3,LBL),("vss",0,-1.7,LBL)]
print(L.layer_boxes(cap.cell if hasattr(cap,'cell') else top,(81,0))[:3])
c=L.finalize(top,"t1",labels)
ref=""".subckt t1 a b vss
X1 a b vss ppolyf_u r_width=1e-6 r_length=20e-6
XC1 ct cb cap_mim_2f0_m4m5_noshield c_width=10e-6 c_length=10e-6
.ends
"""
harness.run(c,"t1",ref,"w1")
