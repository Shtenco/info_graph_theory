"""Generate summary poster image for the theory."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

fig, ax = plt.subplots(1, 1, figsize=(20, 14))
ax.set_xlim(0, 20)
ax.set_ylim(0, 14)
ax.axis('off')

# Colors
C_BG = '#0a0a1a'
C_GOLD = '#ffd700'
C_CYAN = '#00d4ff'
C_GREEN = '#00ff88'
C_RED = '#ff4466'
C_WHITE = '#ffffff'
C_GRAY = '#888899'
C_BOX = '#1a1a3a'

fig.patch.set_facecolor(C_BG)
ax.set_facecolor(C_BG)

def draw_box(x, y, w, h, text, color=C_CYAN, size=12, bold=False, border=None):
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15",
                         facecolor=C_BOX, edgecolor=color, linewidth=2 if border else 1.5)
    ax.add_patch(box)
    ax.text(x + w/2, y + h/2, text, fontsize=size, fontweight='bold' if bold else 'normal',
            color=color, ha='center', va='center', zorder=5)

def draw_arrow(x1, y1, x2, y2, color=C_GRAY, text="", lw=1.5):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=lw))
    if text:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx, my+0.15, text, fontsize=8, color=C_GRAY, ha='center', va='bottom', style='italic')

def draw_label(x, y, text, color=C_WHITE, size=10, ha='center'):
    ax.text(x, y, text, fontsize=size, color=color, ha=ha, va='center')

# Title
ax.text(10, 13.2, 'ИНФОРМАЦИОННЫЙ ГРАФ', fontsize=28, fontweight='bold',
        color=C_GOLD, ha='center', va='center')
ax.text(10, 12.5, 'Единая теория фундаментальной физики из графа Уоттса-Строгаца',
        fontsize=14, color=C_CYAN, ha='center', va='center')

# Three core parameters box
draw_box(7.5, 10.8, 5, 0.9, 'Три параметра:  K=6  |  p=4.8×10⁻⁴²  |  N=4.2×10¹²¹',
         C_GOLD, 13, bold=True)
draw_label(10, 10.3, 'Граф малого мира G(N,K,p)', C_GRAY, 10)

# Arrow to structural functions
draw_arrow(10, 10.6, 10, 9.6, C_CYAN, 'спектр')

# Structural functions box
draw_box(12, 8.8, 6, 0.8, 'Шесть структурных функций  f₁-f₆',
         C_CYAN, 12, bold=True)
draw_label(15, 8.3, 'f₁=104.37  f₂=lnK  f₃=√(Kp)  f₄=1/p  f₅=K/lnK  f₆=1.0527', C_GRAY, 9)

# BIP39 box
draw_box(2, 8.8, 6, 0.8, 'BIP39: язык инфотона (8 параметров)',
         C_GREEN, 12, bold=True)
draw_label(5, 8.3, '11 бит/слово · 2048 слов · 24 слова/фразу · 256 бит энтропии', C_GRAY, 9)

draw_arrow(5, 9.8, 5, 9.6, C_GREEN, 'K=6 → все параметры')

# Spectral invariants
draw_box(10, 7.2, 8, 0.8, 'Спектральные инварианты:  χ_I=85  |  C_p=0.93335  |  C_W=0.98254',
         C_CYAN, 11, bold=True, border=True)
draw_arrow(10, 8.6, 10, 8.0, C_CYAN, 'спектр лапласиана')

# Infoton
draw_box(2, 7.2, 5, 0.8, 'Инфотон (1 нат):  M_Inf = 5.60 мкэВ',
         C_GOLD, 12, bold=True, border=True)
draw_arrow(5, 8.4, 5, 8.0, C_GREEN)
draw_arrow(5, 7.2, 7, 6.2, C_GOLD, 'квант информации')

# Predictions section
draw_box(1, 5.3, 18, 0.7, 'ФУНДАМЕНТАЛЬНЫЕ ПРЕДСКАЗАНИЯ (NO_FIT)',
         C_GOLD, 13, bold=True, border=True)

predictions = [
    ('α (пост. тонкой структуры)', '0.00729807', '0.0099%'),
    ('α_s (сильная связь)', '0.11314', '4.12%'),
    ('M_p (протон)', '938.3000 MeV', '0.003%'),
    ('M_W (W-бозон)', '80.38001 GeV', '1.1×10⁻⁵%'),
    ('G (гравитация)', '6.676×10⁻¹¹', '0.035%'),
    ('Λ (косм. постоянная)', '1.103×10⁻⁵²', '1.38%'),
]

y_pos = 4.6
dx = 0
for name, val, err in predictions:
    col = (dx % 3) * 6 + 1.5
    row = dx // 3
    yy = y_pos - row * 0.6
    ax.text(col, yy, name, fontsize=9, color=C_CYAN, ha='left', va='center')
    ax.text(col + 3.5, yy, val, fontsize=9, color=C_WHITE, ha='left', va='center')
    ax.text(col + 5.2, yy, f'ош. {err}', fontsize=9, color=C_GREEN, ha='left', va='center')
    dx += 1

# 445 constants
draw_box(1, 2.3, 18, 0.6, '445 КОНСТАНТ SciPy/CODATA — BIP39-мономиальные предсказания',
         C_GREEN, 11, bold=True)

stats = [
    ('445', 'всего констант'),
    ('230/445', 'проходят 1%'),
    ('80/128', 'безразмерных pass 1%'),
    ('150/317', 'размерных pass 1%'),
    ('101635', 'мономов/константу'),
    ('43/445', 'проходят 0.1%'),
]
for i, (val, desc) in enumerate(stats):
    xx = i * 3 + 1.5
    ax.text(xx, 1.7, val, fontsize=14, fontweight='bold', color=C_GOLD, ha='center', va='center')
    ax.text(xx, 1.3, desc, fontsize=8, color=C_GRAY, ha='center', va='center')

# Footer
ax.text(10, 0.6, 'Полная цепочка:  Граф → Спектр → Структурные функции → BIP39 → χ_I → C_p, C_W → M_Inf, M_p, M_W → α, α_s, G, Λ',
        fontsize=10, color=C_CYAN, ha='center', va='center', style='italic')
ax.text(10, 0.2, 'github.com/Shtenco/info_graph_theory',
        fontsize=10, color=C_GRAY, ha='center', va='center')

# Save
plt.tight_layout()
plt.savefig('info_graph_theory_poster.png', dpi=200, bbox_inches='tight', facecolor=C_BG)
print("Poster saved: info_graph_theory_poster.png")
