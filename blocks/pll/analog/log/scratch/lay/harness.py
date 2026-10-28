import sys, json
sys.path.insert(0,'/opt/chip-flow/engine/lib')
from pathlib import Path
import layoutlib as L
def run(comp, name, ref_text, work, drc=True, lvs=True):
    work=Path(work); work.mkdir(parents=True, exist_ok=True)
    gds=work/f"{name}.gds"; comp.write_gds(str(gds))
    print("bbox", comp.dbbox())
    if drc:
        L.run_klayout_drc(gds.resolve(), name, (work/"drc.lyrdb").resolve(), timeout=1800)
        items=L.parse_drc_rdb(work/"drc.lyrdb")
        from collections import Counter
        print("DRC", len(items), Counter(i["category"] for i in items).most_common(30))
    if lvs:
        (work/"ref.spice").write_text(L.setup_spelling(ref_text, L.netgen_setup()))
        sp,_=L.run_magic_extract(work, gds.resolve(), name, parasitics=False, timeout=1800)
        try:
            ok, txt = L.run_netgen_lvs(work, sp.name, name, "ref.spice", name, "lvs.log", timeout=1800)
            print("LVS", ok); print("\n".join(txt.splitlines()[-25:]))
        except L.LayoutError as e:
            print("LVS refused", str(e)[:1500])
