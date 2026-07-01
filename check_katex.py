"""Check for bare LaTeX commands in inline math that would cause KaTeX errors."""
import re

with open('README.md', 'r', encoding='utf-8') as f:
    content = f.read()

BARE_CMDS = ['sum','prod','int','lim','exp','sin','cos','tan','log','ln',
             'sigma','alpha','beta','gamma','lambda','mu','pi','theta','chi',
             'omega','to','mapsto','infty','partial','mathbb','mathcal',
             'mathfrak','mathrm','textbf']

issues = []
i = 0
while i < len(content):
    start = content.find('$', i)
    if start == -1:
        break
    if start + 1 < len(content) and content[start+1] == '$':
        i = start + 2
        continue
    end = content.find('$', start + 1)
    if end == -1:
        break
    if end + 1 < len(content) and content[end+1] == '$':
        i = end + 2
        continue
    expr = content[start+1:end]
    for cmd in BARE_CMDS:
        idx = expr.find(cmd)
        while idx != -1:
            if idx == 0 or expr[idx-1] != '\\':
                before = expr[:idx]
                if before.count('{') <= before.count('}'):
                    issues.append((cmd, expr))
                    break
            idx = expr.find(cmd, idx + 1)
    i = end + 1

for cmd, expr in issues:
    print(f'bare "{cmd}" in: ${expr}$')
print(f'\nTotal: {len(issues)} issues')
