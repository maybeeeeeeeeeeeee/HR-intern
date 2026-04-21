with open('backend/app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "Structured Data:" in line and line.startswith("        print"):
        lines[i] = "    " + line.lstrip()
    if "if not OPENAI_API_KEY:" in line:
        lines[i] = "    if not JWT_SECRET or not ENCRYPTION_KEY:\n"
    if "OPENAI_API_KEY=votre_cle" in line:
        lines[i] = ""

with open('backend/app.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Indentation fixed.")
