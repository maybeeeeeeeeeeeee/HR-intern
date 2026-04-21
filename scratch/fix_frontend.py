import sys
sys.stdout.reconfigure(encoding='utf-8')

filepath = r'c:\Users\ACH\Downloads\AI-Finder - final\frontend\index.html'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Fix lines 1549-1559: the escaped backticks and dollar signs
# Replace the broken block with clean JS
new_block = """                const configBtn = !s.is_archived
                    ? `<button class="btn-icon" onclick="event.stopPropagation(); configureArchive('${s.id}', ${s.auto_archive_days || 'null'})" title="Auto-archivage" style="font-size: 14px;">⚙️</button>`
                    : '';

                actionButtons = `
                    <div class="source-actions">
                        ${configBtn}
                        ${archiveBtn}
                        <button class="btn-icon btn-delete" onclick="deleteSource('${s.id}')" title="Supprimer">✕</button>
                    </div>
                `;
"""

# Find and replace lines 1549-1559 (0-indexed: 1548-1558)
start_idx = None
end_idx = None
for i, line in enumerate(lines):
    if 'const configBtn = !s.is_archived' in line:
        start_idx = i
    if start_idx and '\\`;' in line and i > start_idx:
        end_idx = i
        break

if start_idx and end_idx:
    lines[start_idx:end_idx+1] = [new_block]
    print(f"Fixed configBtn block (lines {start_idx+1}-{end_idx+1})")
else:
    print(f"Could not find block. start={start_idx}, end={end_idx}")

# Also fix the source-meta line with escaped $
for i, line in enumerate(lines):
    if '\\${date}\\${s.auto_archive_days' in line:
        lines[i] = line.replace('\\${date}\\${s.auto_archive_days', '${date}${s.auto_archive_days')
        print(f"Fixed source-meta line {i+1}")
        break

# Fix the source details modal too
for i, line in enumerate(lines):
    if "\\${s.auto_archive_days ? s.auto_archive_days" in line:
        lines[i] = line.replace('\\${s.auto_archive_days', '${s.auto_archive_days')
        print(f"Fixed details line {i+1}")
    if "\\${s.is_archived" in line:
        lines[i] = lines[i].replace("\\${s.is_archived", "${s.is_archived")
        print(f"Fixed is_archived line {i+1}")

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✅ Frontend JS fixed")
