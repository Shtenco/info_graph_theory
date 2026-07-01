"""Generate FULL 445 constant table in README.md."""
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

def fmt_formula(f):
    """Convert sparse_formula to readable LaTeX."""
    f = f.replace('sign(1) * ', '').replace('sign(-1) * ', '-')
    f = f.replace(' * ', ' \\cdot ')
    f = f.replace('^-', '^{-').replace('^', '^{')
    # Close braces for negative exponents
    f = re.sub(r'\^{(-?\d+)', r'^{\1}', f)
    f = f.replace('dict', '\\text{dict}')
    f = f.replace('total_bits', '\\text{total\\_bits}')
    f = f.replace('checksum', '\\text{checksum}')
    f = f.replace('entropy', '\\text{entropy}')
    f = f.replace('words', '\\text{words}')
    f = f.replace('bits', '\\text{bits}')
    f = f.replace('lnK', '\\ln(K)')
    f = f.replace('lnDict', '\\ln(\\text{dict})')
    f = f.replace('m_e', 'm_e')
    f = f.replace('mu_B', '\\mu_B')
    f = f.replace('U', 'U')
    f = f.replace('f1', 'f_1')
    f = f.replace('bip_density', '\\rho_{\\text{BIP}}')
    # Clean up empty braces
    f = f.replace('{}', '')
    return f

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
    
    # Shorten long names for table fit
    if len(name) > 45:
        name = name[:42] + "..."
    
    T += f"| {idx} | {name} | {unit} | {obs} | ${formula}$ | {pred} | {err}% | {status} |\n"

print(f"Table size: {len(T)} chars, {len(T.split(chr(10)))} rows")

# Now insert into README
readme = open(README, 'r', encoding='utf-8').read()

# Find the prediction table section and replace it
marker_start = "## BIP39-мономиальные предсказания: 445 констант"
marker_end = "Полные таблицы всех 445 констант"

start_idx = readme.find(marker_start)
end_idx = readme.find(marker_end, start_idx)

if start_idx == -1 or end_idx == -1:
    print("ERROR: Could not find table markers in README")
    # Let me search more broadly
    for m in ["BIP39-мономиальные предсказания", "Полные таблицы", "Безразмерные константы"]:
        idx = readme.find(m)
        if idx >= 0:
            print(f"  Found '{m}' at pos {idx} (line {readme[:idx].count(chr(10))+1})")
    exit(1)

# Find the end of the paragraph after marker_end
end_of_section = readme.find('\n', readme.find('\n', end_idx) + 1)
# Actually find the next ## header or end of file
next_header = readme.find('\n## ', end_idx + 50)
if next_header == -1:
    next_header = len(readme)

# Build replacement
replacement = f"""## BIP39-мономиальные предсказания: все 445 констант

Полная таблица BIP39-мономиальных предсказаний для всех 445 констант SciPy/CODATA.
Моном — произведение степеней параметров BIP39-словаря: $K$, bits, dict, words, entropy, total_bits, checksum, $U$, $f_1$, $\ln(K)$, $\ln(\\text{{dict}})$.

Статусы: **PASS** — ошибка < 1%, **PASS*** — ошибка < 0.1%, **fit** — калибровочный коэффициент.

{ T }

Полные данные в JSON: [`bip39_fit_all_445_v8.json`](complete_theory_kit/results/bip39_fit_all_445_v8.json) и [`symbolic_all_445_constants_v10.json`](complete_theory_kit/results/symbolic_all_445_constants_v10.json)."""

new_readme = readme[:start_idx] + replacement + readme[end_of_section:]

with open(README, 'w', encoding='utf-8') as f:
    f.write(new_readme)

print(f"READme updated. New size: {len(new_readme)} bytes, {new_readme.count(chr(10))} lines")
