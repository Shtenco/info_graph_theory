"""
Fix LaTeX rendering issues in README.md for GitHub:
Convert ```text ... ``` fenced code blocks containing LaTeX to $$...$$ display math,
and convert inline backtick code spans containing LaTeX to $...$ inline math.
"""
import re

with open('README.md', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
output = []
i = 0

def is_definitely_not_latex(text):
    """Check if text is definitely NOT LaTeX (plain text like status, path, etc)."""
    non_latex_indicators = [
        r'^MACHINE VERIFY',
        r'^DEEP README AUDIT', 
        r'^FULL NUMERIC VERIFICATION',
        r'^CAS SYMBOLIC VERIFICATION',
        r'^PASS',
        r'^C:\\',
        r'^\d+/\d+ числовых проверок',
        r'^\d+ / \d+',
        r'^Ключевое ядро',
        r'^Слишком сильное утверждение',
        r'^Следующий технический этап',
        r'^Чтобы закрыть',
        r'^Честный вывод',
        r'^Текущая теория прошла',
        r'^Что проверено',
        r'^Итого:',
        r'^Этот документ',
        r'^Цель документа',
        r'^Физическая истинность',
        r'^Набор',
        r'^Только',
        r'^Все строки',
        r'^Строк с процентной',
        r'^максимум ошибки',
        r'^последняя частичная',
        r'^последний член',
        r'^верхняя оценка',
        r'^Проверка тождества',
        r'^- `K =',
        r'^- `p =',
        r'^- `N =',
        r'^\- последний член',
        r'^\- последняя частичная',
        r'^\- верхняя оценка',
        r'^\- узлов:',
        r'^\- локальная связность:',
        r'^\- ребер:',
        r'^\- `trace',
        r'^\- `sum',
        r'^\- ошибка следа',
        r'^\- нулевых мод',
        r'^\- минимальная положительная',
        r'^\- максимальная мода',
        r'^Суммарный потенциальный',
        r'^Сектор',
        r'^Квантовые вычисления',
        r'^Полупроводники',
        r'^Фармацевтика',
        r'^Криптография',
        r'^Big Data',
        r'^Материаловедение',
        r'^ИТОГО',
        r'^\|:--',
        r'^C:\\\\Users',
        r'^├──',
        r'^└──',
    ]
    for pattern in non_latex_indicators:
        if re.search(pattern, text):
            return True
    # Plain text with mostly natural language and few/no LaTeX commands
    text_no_space = text.replace(' ', '')
    # If text has many Cyrillic characters, it's likely plain text
    cyrillic_count = len(re.findall(r'[а-яА-Я]', text))
    if cyrillic_count > 10 and not re.search(r'\\[a-zA-Z]{3,}', text):
        return True
    return False

def has_latex_commands(text):
    """Count LaTeX command occurrences in text."""
    score = 0
    # Count LaTeX commands (backslash + word)
    latex_cmds = re.findall(r'\\[a-zA-Z]{2,}', text)
    score += len(latex_cmds)
    # Count LaTeX special characters
    if '{' in text and '}' in text:
        score += 0.5
    if re.search(r'_[a-zA-Z0-9{}]', text) or re.search(r'\^[a-zA-Z0-9{}]', text):
        score += 1
    # Check for \begin or \end
    if re.search(r'\\begin\{|\\end\{', text):
        score += 3
    # Check for \boxed
    if '\\boxed' in text:
        score += 2
    # Check for display-style fractions
    if '\\frac' in text:
        score += 2
    # Check for \text
    if re.search(r'\\text\{', text):
        score += 0.5
    # Check for sum, prod, int
    if re.search(r'\\sum|\\prod|\\int|\\lim', text):
        score += 2
    # Mathematical symbols
    if re.search(r'\\to|\\mapsto|\\infty|\\partial', text):
        score += 1
    # \qquad, \quad
    if re.search(r'\\qquad|\\quad', text):
        score += 0.5
    # Parentheses that are part of math: \( and \)
    if re.search(r'\\\(|\\\)', text):
        score += 1
    return score

def contains_latex(text):
    """Determine if a code block contains LaTeX that should be rendered as math."""
    if is_definitely_not_latex(text):
        return False
    return has_latex_commands(text) >= 1.0

def has_generic_latex_command(code):
    """Check if a short inline code span has LaTeX commands."""
    return bool(re.search(r'\\[a-zA-Z]{2,}', code))

FILE_EXTENSIONS = ('.py', '.md', '.json', '.csv', '.txt', '.tex', '.yml', '.yaml',
                   '.toml', '.ini', '.cfg', '.sh', '.bat', '.ps1', '.js', '.ts',
                   '.css', '.html', '.xml', '.svg', '.png', '.jpg', '.jpeg', '.gif',
                   '.pdf', '.tsv', '.rst', '.jsonl')

def looks_like_filepath(text):
    """Check if text looks like a file path or name rather than LaTeX."""
    # Windows drive letter (e.g., C:\)
    if re.search(r'[A-Za-z]:\\', text):
        return True
    # Contains forward slash path separators (but not if part of LaTeX like \mu)
    if '/' in text:
        return True
    # Ends with a known file extension
    if text.lower().endswith(FILE_EXTENSIONS):
        return True
    # Has a dot followed by 1-4 alphanumeric chars at end (generic extension)
    if re.search(r'\.[a-zA-Z0-9]{1,4}$', text):
        return True
    return False

while i < len(lines):
    line = lines[i]
    stripped = line.strip()
    
    # Check for fenced code block start: ```text
    fenced_match = re.match(r'^```(\w*)$', stripped)
    if fenced_match:
        lang = fenced_match.group(1)
        
        # Find the closing fence
        j = i + 1
        code_lines = []
        while j < len(lines) and not lines[j].strip().startswith('```'):
            code_lines.append(lines[j])
            j += 1
        
        if j < len(lines):  # Found closing fence
            code_text = '\n'.join(code_lines)
            
            # Convert if language is 'text' (or empty/tex/latex) and contains LaTeX
            # but NOT for 'powershell', 'bash', 'python', 'json', 'csv', etc.
            if lang in ('', 'text', 'tex', 'latex') and contains_latex(code_text):
                indent = line[:len(line) - len(line.lstrip())]
                output.append(f'{indent}$$\n{code_text}\n{indent}$$')
                i = j + 1
                continue
        
        # If we didn't convert, output all lines as-is
        while i <= j and i < len(lines):
            output.append(lines[i])
            i += 1
        continue
    
    # Handle inline backtick code spans with LaTeX
    def replace_inline_latex(match):
        code = match.group(1)
        # If it has actual LaTeX commands, convert regardless of other patterns
        if has_generic_latex_command(code):
            return f'${code}$'
        # Never convert file paths or names
        if looks_like_filepath(code):
            return match.group(0)
        # Also convert if it looks like an equation (has = or math operators)
        if re.search(r'[=+\-*/^_{}]', code) and len(code) > 2:
            return f'${code}$'
        return match.group(0)
    
    line = re.sub(r'`([^`]+)`', replace_inline_latex, line)
    output.append(line)
    i += 1

result = '\n'.join(output)

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(result)

print("Conversion complete. README.md has been updated.")
print(f"Total lines processed: {len(lines)}")

# Count changes
old_latex_count = len(re.findall(r'\$\$[^$]+\$\$', content))
new_latex_count = len(re.findall(r'\$\$[^$]+\$\$', result))
old_inline = len(re.findall(r'\$[^$\n]+\$', content))
new_inline = len(re.findall(r'\$[^$\n]+\$', result))
old_fences = len(re.findall(r'^```text$', content, re.MULTILINE))
new_fences = len(re.findall(r'^```text$', result, re.MULTILINE))
print(f"Display math blocks: {old_latex_count} -> {new_latex_count}")
print(f"Inline math: {old_inline} -> {new_inline}")
print(f"Fenced 'text' blocks: {old_fences} -> {new_fences}")
