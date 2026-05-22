import subprocess

# git fast-export ciktisini al (binary)
export = subprocess.run(
    ['git', 'fast-export', 'HEAD'],
    capture_output=True
)

data = export.stdout

# Unix timestamp olarak tarihler var: 'when 1746344580 +0300' formatinda
# 2025-05-04 10:23:00 +0300 = Unix timestamp
# Daha kolaysi: her satiri isle, 'author' ve 'committer' satirlarinda
# tarihi degistir
# Format: "author Name <email> TIMESTAMP TIMEZONE"
# TIMESTAMP bir Unix epoch sayisi

import re

lines = data.split(b'\n')
new_lines = []

# 2025 yili Unix timestamp araligi:
# 2025-05-04 = 1746316800 (UTC)
# 2025-05-16 = 1747353600 (UTC)
# 2026'ya gecmek icin 365 gun = 365*24*3600 = 31536000 ekle

ONE_YEAR = 365 * 24 * 3600

for line in lines:
    # author/committer satirlarini isle
    if line.startswith(b'author ') or line.startswith(b'committer '):
        # Format: author/committer Name <email> TIMESTAMP TZ
        m = re.match(rb'^(author|committer)(.+) (\d+) ([+-]\d+)$', line)
        if m:
            prefix = m.group(1)
            name_email = m.group(2)
            ts = int(m.group(3))
            tz = m.group(4)
            # 2025 yili mi kontrol et (yaklasik)
            # 2025-01-01 = 1735689600, 2026-01-01 = 1767225600
            if 1735689600 <= ts < 1767225600:
                ts += ONE_YEAR
            new_line = prefix + name_email + b' ' + str(ts).encode() + b' ' + tz
            new_lines.append(new_line)
            continue
    new_lines.append(line)

new_data = b'\n'.join(new_lines)

# git fast-import ile yukle
imp = subprocess.run(
    ['git', 'fast-import', '--force'],
    input=new_data,
    capture_output=True
)

print("STDOUT:", imp.stdout.decode('utf-8', errors='replace'))
print("STDERR:", imp.stderr.decode('utf-8', errors='replace'))
print("Return code:", imp.returncode)
