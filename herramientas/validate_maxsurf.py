#!/usr/bin/env python3
import pandas as pd
import os
from pathlib import Path

PROJECT_DIR = Path('/Users/robertgaraban/Downloads/DNVGL Examen 2020')
CSV_PATH = PROJECT_DIR / 'maxsurf_table_quoted.csv'
REPORT_HTML = PROJECT_DIR / 'maxsurf_validation_report.html'
FLAGS_CSV = PROJECT_DIR / 'maxsurf_flags.csv'

# Read CSV
if not CSV_PATH.exists():
    print('CSV not found:', CSV_PATH)
    raise SystemExit(1)

df = pd.read_csv(CSV_PATH)
# Ensure parsed_value numeric where possible

def to_num(x):
    try:
        return float(x)
    except:
        return None

# Create a mapping key->parsed_value_num
vals = {}
for idx, row in df.iterrows():
    key = row['key']
    parsed = row.get('parsed_value', None)
    num = None
    if pd.notna(parsed):
        num = to_num(parsed)
    vals[key] = {
        'raw': row.get('raw_value',''),
        'num': num,
        'unit': row.get('unit',''),
        'notes': row.get('notes','')
    }

# Checks
flags = []
# 1. Delta vs rho*V
rho = 1025.0
if vals.get('Volume_displaced', {}).get('num') is not None and vals.get('Displacement', {}).get('num') is not None:
    V = vals['Volume_displaced']['num']
    disp = vals['Displacement']['num']
    expected = rho * V
    diff = abs(expected - disp)
    rel = diff / max(expected, 1e-6)
    if rel > 0.005:  # >0.5% difference
        flags.append({'check':'Delta_vs_rhoV','message':f'Displacement {disp} vs rho*V {expected:.3f} (rel diff {rel:.3%})','severity':'HIGH'})
    else:
        flags.append({'check':'Delta_vs_rhoV','message':f'OK (rel diff {rel:.3%})','severity':'OK'})
else:
    flags.append({'check':'Delta_vs_rhoV','message':'Missing Volume or Displacement','severity':'MEDIUM'})

# 2. Coeff ranges
for k, low, high in [('Block_coeff_Cb',0.45,0.9), ('Prismatic_coeff_Cp',0.45,0.95)]:
    v = vals.get(k, {}).get('num')
    if v is None:
        flags.append({'check':k,'message':'Missing value','severity':'MEDIUM'})
    else:
        if v < low or v > high:
            flags.append({'check':k,'message':f'Out of expected range [{low},{high}]: {v}','severity':'MEDIUM'})
        else:
            flags.append({'check':k,'message':f'OK: {v}','severity':'OK'})

# 3. KM == KB + BM
KB = vals.get('KB', {}).get('num')
BM = vals.get('BMt', {}).get('num')
KM = vals.get('KMt', {}).get('num')
if KB is None or BM is None or KM is None:
    flags.append({'check':'KM_relation','message':'Missing KB/BM/KM','severity':'MEDIUM'})
else:
    km_calc = KB + BM
    if abs(km_calc - KM) > 0.02:
        flags.append({'check':'KM_relation','message':f'KM mismatch: KM table {KM} vs KB+BM {km_calc:.3f}','severity':'HIGH'})
    else:
        flags.append({'check':'KM_relation','message':'OK','severity':'OK'})

# 4. GM = KM - KG
KG = vals.get('KG_fluid', {}).get('num')
GM = vals.get('GMt_corrected', {}).get('num')
if KM is None or KG is None or GM is None:
    flags.append({'check':'GM_relation','message':'Missing KM/KG/GM','severity':'MEDIUM'})
else:
    gm_calc = KM - KG
    if abs(gm_calc - GM) > 0.05:
        flags.append({'check':'GM_relation','message':f'GM mismatch: GM table {GM} vs KM-KG {gm_calc:.3f}','severity':'HIGH'})
    else:
        flags.append({'check':'GM_relation','message':'OK','severity':'OK'})

# 5. Reasonable magnitudes for verticals
for key in ['KB','BMt','KMt','KG_fluid','GMt_corrected']:
    v = vals.get(key, {}).get('num')
    if v is None:
        continue
    if v < 0 or v > 30:
        flags.append({'check':'magnitude','message':f'{key} has suspicious magnitude {v}','severity':'MEDIUM'})

# 6. Detect OCR artifacts in raw strings
for k, info in vals.items():
    raw = str(info.get('raw',''))
    if any(s in raw.lower() for s in ['fro','tonn','tonn','mm','cm']):
        flags.append({'check':'ocr_artifact','message':f'{k} raw contains "{raw}"','severity':'LOW'})
    if info.get('num') is None and info.get('raw','')!='':
        # If parsed numeric missing but raw has digits
        if any(ch.isdigit() for ch in raw):
            flags.append({'check':'parse_fail','message':f'{k} could not parse numeric value from raw "{raw}"','severity':'MEDIUM'})

# 7. Percent fields
for k in ['LCB_percent','LCF_percent']:
    v = vals.get(k, {}).get('num')
    if v is not None:
        if abs(v) > 200:
            flags.append({'check':'percent_range','message':f'{k} value {v} out of expected percent range','severity':'MEDIUM'})

# Compose flags dataframe
flags_df = pd.DataFrame(flags)
if flags_df.empty:
    print('No flags generated')
else:
    flags_df.to_csv(FLAGS_CSV, index=False)
    print('Flags written to', FLAGS_CSV)

# Generate simple HTML report
html = []
html.append('<html><head><meta charset="utf-8"><title>Maxsurf validation report</title></head><body>')
html.append('<h1>Maxsurf validation report</h1>')
html.append('<h2>Source CSV</h2>')
html.append(f'<p>{CSV_PATH}</p>')
html.append('<h2>Summary checks</h2>')
html.append('<table border="1" cellpadding="4"><tr><th>Check</th><th>Message</th><th>Severity</th></tr>')
for _, r in flags_df.iterrows():
    html.append(f"<tr><td>{r['check']}</td><td>{r['message']}</td><td>{r['severity']}</td></tr>")
html.append('</table>')
html.append('<h2>All extracted values</h2>')
html.append('<table border="1" cellpadding="4"><tr><th>Key</th><th>Raw</th><th>Value</th><th>Unit</th><th>Notes</th></tr>')
for k, v in vals.items():
    html.append(f"<tr><td>{k}</td><td>{v['raw']}</td><td>{v['num']}</td><td>{v['unit']}</td><td>{v['notes']}</td></tr>")
html.append('</table>')
html.append('</body></html>')

with open(REPORT_HTML, 'w', encoding='utf-8') as f:
    f.write('\n'.join(html))

print('Report written to', REPORT_HTML)
print('Done')
