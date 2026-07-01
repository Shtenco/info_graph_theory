"""Check README for potential GitHub display issues."""
import re

t = open('README.md', 'r', encoding='utf-8').read()
lines = t.split('\n')

# Long lines
long_lines = [(i, len(l), l[:80]) for i, l in enumerate(lines, 1) if len(l) > 500]
print(f'Lines > 500 chars: {len(long_lines)}')

# Check for broken LaTeX
dollar_pairs = len(re.findall(r'\$\$', t))
print(f'Double dollar pairs: {dollar_pairs}')

# Check for surrogate characters
for i, c in enumerate(t):
    if 0xD800 <= ord(c) <= 0xDFFF:
        print(f'Surrogate at pos {i}: {repr(c)}')
        break
else:
    print('No surrogate characters')

# Check for zero-width characters
zw = sum(1 for c in t if ord(c) in (0x200B, 0x200C, 0x200D, 0xFEFF, 0x00AD))
print(f'Zero-width/control characters: {zw}')

# Check for carriage return consistency
cr = t.count('\r\n')
lf = t.count('\n') - cr
print(f'CRLF: {cr}, LF only: {lf}')

# Check for broken HTML tags
bad_html = re.findall(r'<[^>]*[&<>]', t)
print(f'Potentially broken HTML tags: {len(bad_html)}')

# Check for any non-printable characters
non_print = sum(1 for c in t if ord(c) < 32 and ord(c) not in (10, 13))
print(f'Non-printable control chars (except CR/LF): {non_print}')

print(f'\nTotal size: {len(t)} bytes, {len(lines)} lines')
print(f'Max line length: {max(len(l) for l in lines)}')
print(f'Min line length: {min(len(l) for l in lines)}')
