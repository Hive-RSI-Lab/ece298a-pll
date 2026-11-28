"""phsweep.py WS EXTRACTED DECK CORNER T TAG OUTDIR
One stress deck (from WS/layout_ref) at one corner on EXTRACTED, with the
pll_en fall moved from 3.301e-6 to T, run and scored by the gate's own code
(stresslib.score_run). Prints one JSON line: the scored fails, the worst gate
pair after the disable (t >= 3.29 us) over every device, and MN_HN5's peaks."""
import sys, json, re
from pathlib import Path
import os
_CF = Path(os.environ.get('CHIP_FLOW_HOME', '/home/hive2/wt/af5d4-gate'))
sys.path.insert(0, str(_CF / 'engine' / 'lib'))
sys.path.insert(0, str(_CF / 'engine' / 'scripts'))
import numpy as np
import stresslib, layoutlib, sim_run
import check_pex_sim as C

ws, ext, deckname, cname, T, tag, outdir = sys.argv[1:8]
ws, ext, out = Path(ws).resolve(), Path(ext).resolve(), Path(outdir).resolve()
out.mkdir(parents=True, exist_ok=True)
limits = stresslib.load_limits()
side = ws / 'layout_ref' / 'pll_analog_stress.yaml'
row = [d for d in stresslib.load_sidecar(side) if d['name'] == deckname][0]
raw_text = ext.read_text()
devices, others = stresslib.parse_devices(raw_text, 'pll_analog')
ref_text = (ws / 'netlist' / 'pll_analog.cir').read_text()
stresslib.label_devices(devices, ref_text, 'pll_analog')
pins = stresslib.subckt_pins(raw_text, 'pll_analog')
template = row['bench'].read_text()
outer, cell = stresslib.dut_of(template, row['bench'].name)
stresslib.vectors_of(devices, pins, outer)
vectors = sorted({v for d in devices for v in d['vectors'] if v})
sweep, _ = sim_run.spec_sweep(ws)
corner = C._named(sweep, cname)
import speclib
spec = speclib.load_spec(ws / 'spec' / 'spec.yaml')
tokens = C.corner_tokens(corner, (spec.get('supply') or {}).get('vdd'))
text = template.format(pdk=layoutlib.pdk_root(), extracted=ext.resolve(), **tokens)
old = 'ben pll_en 0 v=v(vdd)*min(max((3.301e-6-time)/1e-9,0),1)'
assert text.count(old) == 1, 'pll_en line not found'
text = text.replace(old, old.replace('3.301e-6', T))

bench_path, raw = out / f'{tag}.cir', out / f'{tag}.raw'
bench_path.write_text(stresslib.with_control(text, raw.name, vectors, row['bench'].name))
layoutlib.run_ngspice(bench_path, cwd=out, timeout=5400)
t, store = stresslib.read_binary_raw(raw)
found = stresslib.score_run(t, store, devices, row['windows'], limits)
fails = [f"{r['label']} {r['pair']}" for r in found
         if r.get('status') == 'fail' or r.get('over_breakdown')]
data, cols = store['data'], store['columns']
n_var = data.shape[1]
w = t >= 3.29e-6
arr = np.asarray(data[w])
arr = np.column_stack((arr, np.zeros(len(arr))))
worst, hn5 = (0.0, '', 0.0), {}
for dev in devices:
    if limits['models'][dev['model']]['kind'] == 'cap':
        continue
    for pair, p, q in stresslib.MOS_PAIRS:
        pc = C_ = stresslib._column(cols, dev['vectors'][p], n_var)
        qc = stresslib._column(cols, dev['vectors'][q], n_var)
        v = np.abs(arr[:, pc] - arr[:, qc]); i = int(v.argmax())
        if v[i] > worst[0]:
            worst = (float(v[i]), f"{dev['label']} {pair}", float(t[w][i]))
        if dev['label'].lstrip('X') == 'MN_HN5' or ('g=en_b' in dev['label'] and 'd=a_7950_0' in dev['label']):
            hn5[pair] = round(float(v[i]), 4)
hn5_scored = [{'pair': r['pair'], 'status': r.get('status')} for r in found
              if r['label'].lstrip('X') == 'MN_HN5' or ('g=en_b' in r['label'] and 'd=a_7950_0' in r['label'])]
del store, arr
raw.unlink()
print(json.dumps({'tag': tag, 'deck': deckname, 'corner': cname, 'T': T,
                  'worst_after_disable_v': round(worst[0], 4),
                  'worst_pair': worst[1], 't_worst': worst[2],
                  'fails': fails, 'hn5_peaks': hn5, 'hn5_scored': hn5_scored}))
