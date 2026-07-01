"""Generate FULL 445 constant table in README.md — FIXED LaTeX."""
import json, math, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, 'README.md')

d = json.load(open(os.path.join(ROOT, 'complete_theory_kit/results/bip39_fit_all_445_v8.json'), 'r', encoding='utf-8'))
rows = d['rows']

def fmt_val(v):
    if v is None: return "—"
    if isinstance(v, float):
        if abs(v) < 1e-3 or abs(v) > 1e9:
            return f"{v:.6e}"
        if v == int(v) and abs(v) < 1e12:
            return str(int(v))
        return f"{v:.8g}"
    return str(v)

# Variable display names for LaTeX
VAR_NAMES = {
    'K': 'K',
    'bits': '\\text{bits}',
    'dict': '\\text{dict}',
    'words': '\\text{words}',
    'entropy': '\\text{entropy}',
    'total_bits': '\\text{total\\_bits}',
    'checksum': '\\text{checksum}',
    'lnK': '\\ln(K)',
    'lnDict': '\\ln(\\text{dict})',
    'U': 'U',
    'f1': 'f_1',
    'pi': '\\pi',
    'e': 'e',
    'bip_density': '\\rho_{\\text{BIP}}',
    'mu_B': '\\mu_B',
}

def fmt_formula(f):
    """Convert sparse_formula to proper LaTeX."""
    # Extract sign
    sign = ''
    if f.startswith('sign(-1) * '):
        sign = '-'
        f = f[11:]
    elif f.startswith('sign(1) * '):
        f = f[10:]
    
    # Handle base units like m_e[MeV], mu_B[J/T]
    base_unit = None
    for bu in ['m_e[MeV]', 'mu_B[J/T]']:
        if bu in f:
            base_unit = bu
            f = f.replace(bu + ' * ', '').replace(bu, '')
            break
    
    # Split by * 
    terms = [t.strip() for t in f.split('*') if t.strip()]
    
    latex_terms = []
    for term in terms:
        # Parse variable name and exponent
        term = term.strip()
        if not term:
            continue
        if term == '1':
            latex_terms.append('1')
            continue
        
        # Check for variable^exponent pattern
        m = re.match(r'^([a-zA-Z_]\w*)\^(-?\d+)$', term)
        if m:
            var, exp = m.group(1), m.group(2)
            var_tex = VAR_NAMES.get(var, var)
            if exp == '1':
                latex_terms.append(var_tex)
            elif exp == '-1':
                latex_terms.append(f'{var_tex}^{{-1}}')
            else:
                latex_terms.append(f'{var_tex}^{{{exp}}}')
        elif re.match(r'^[a-zA-Z_]\w*$', term):
            var = term
            var_tex = VAR_NAMES.get(var, var)
            latex_terms.append(var_tex)
        else:
            # Fallback: keep as-is but escape braces
            latex_terms.append(term)
    
    result = ' \\cdot '.join(latex_terms) if latex_terms else '1'
    if base_unit:
        result = base_unit.split('[')[0] + ' \\cdot ' + result
    
    return sign + result

# Build the table
T = ""

T += "| # | Константа | Ед. | Наблюдение | BIP39-моном | Предсказание | Ошибка % | Статус |\n"
T += "|:-:|:--|:--:|:--:|:--|:--:|:--:|:--|\n"

# Separate dimensionless and dimensional, sort by name
dim_rows = [r for r in rows if r.get('is_dimensionless')]
ndim_rows = [r for r in rows if not r.get('is_dimensionless')]
dim_rows.sort(key=lambda r: r['name'])
ndim_rows.sort(key=lambda r: r['name'])

all_sorted = dim_rows + ndim_rows

for idx, r in enumerate(all_sorted, 1):
    name = r['name']
    unit = r.get('unit', '')
    obs = fmt_val(r['value'])
    pred = fmt_val(r.get('sparse_magnitude_predicted', r.get('sparse_signed_predicted')))
    err = f"{r['sparse_relative_error_percent']:.4f}"
    formula = fmt_formula(r['sparse_formula'])
    
    if r['sparse_pass_1_percent']:
        status = "PASS"
    elif r['sparse_pass_0_1_percent']:
        status = "PASS*"
    else:
        status = "fit"
    
    if len(name) > 45:
        name = name[:42] + "..."
    
    T += f"| {idx} | {name} | {unit} | {obs} | ${formula}$ | {pred} | {err}% | {status} |\n"

print(f"Table size: {len(T)} chars, {len(T.split(chr(10)))} rows")

# Now insert into README
readme = open(README, 'r', encoding='utf-8').read()

marker_start = "## BIP39-мономиальные предсказания: все 445 констант"
end_marker = "Полные данные в JSON"

start_idx = readme.find(marker_start)
end_idx = readme.find(end_marker, start_idx)

if start_idx == -1 or end_idx == -1:
    print("ERROR: Could not find table markers")
    for m in ["BIP39-мономиальные предсказания: все 445", "Полные данные в JSON"]:
        idx = readme.find(m)
        print(f"  '{m}': {'found at ' + str(idx) if idx >= 0 else 'NOT FOUND'}")
    exit(1)

# Find the next ## header or end of section after end_marker
section_end = readme.find('\n## ', end_idx)
if section_end == -1:
    section_end = len(readme)

replacement = f"""## BIP39-мономиальные предсказания: все 445 констант

Полная таблица BIP39-мономиальных предсказаний для всех 445 констант SciPy/CODATA.
Моном — произведение степеней параметров BIP39-словаря: $K$, $\\text{{bits}}$, $\\text{{dict}}$, $\\text{{words}}$, $\\text{{entropy}}$, $\\text{{total\\_bits}}$, $\\text{{checksum}}$, $U$, $f_1$, $\\ln(K)$, $\\ln(\\text{{dict}})$.

Статусы: **PASS** — ошибка < 1%, **PASS*** — ошибка < 0.1%, **fit** — требуется калибровочный коэффициент.

{T}

{end_marker} в JSON: [`bip39_fit_all_445_v8.json`](complete_theory_kit/results/bip39_fit_all_445_v8.json) и [`symbolic_all_445_constants_v10.json`](complete_theory_kit/results/symbolic_all_445_constants_v10.json)."""

new_readme = readme[:start_idx] + replacement + readme[section_end:]

with open(README, 'w', encoding='utf-8') as f:
    f.write(new_readme)

# Validate that all $...$ expressions have balanced braces
import re as re2
dollars = re2.findall(r'\$[^$]+\$', new_readme)
bad_braces = []
for d in dollars:
    opens = d.count('{')
    closes = d.count('}')
    if opens != closes:
        bad_braces.append((d[:60], opens, closes))

if bad_braces:
    print(f"\nWARNING: {len(bad_braces)} LaTeX expressions with unbalanced braces:")
    for expr, o, c in bad_braces[:5]:
        print(f"  {expr}...  opens={o} closes={c}")
else:
    print("\nAll LaTeX expressions have balanced braces!")

print(f"README updated. Size: {len(new_readme)} bytes, {new_readme.count(chr(10))} lines")
