import os
import re

base_dir = r'c:\Users\ACH\Downloads\AI-Finder - final'

# ==========================================
# 1. CLEAN APP.PY
# ==========================================
app_py_path = os.path.join(base_dir, 'backend', 'app.py')
with open(app_py_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix ALLOWED_EXTENSIONS
content = re.sub(r"ALLOWED_EXTENSIONS = \{'pdf', 'docx', 'txt', 'csv', 'xlsx', 'xls'\}", "ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}", content)

# Remove add_structured_file_direct()
content = re.sub(r"def add_structured_file_direct\(file, filename, file_ext\):.*?(?=@app\.route\('/api/sources/<source_id>', methods=\['DELETE'\]\))", "", content, flags=re.DOTALL)

# Safely Remove process_enhanced_query and analyze_data_source blocks
content = re.sub(r"# ============================================================================\n# NOUVELLES FONCTIONNALITÃ‰S AVANCÃ‰ES\n# ============================================================================.*?if __name__ == '__main__':", "if __name__ == '__main__':", content, flags=re.DOTALL)

with open(app_py_path, 'w', encoding='utf-8') as f:
    f.write(content)

# ==========================================
# 2. CLEAN REQUIREMENTS.TXT
# ==========================================
req_path = os.path.join(base_dir, 'backend', 'requirements.txt')
with open(req_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip_list = ['openai==', 'httpx==', 'psycopg2-binary==', 'mysql-connector-python==', 
             'beautifulsoup4==', 'requests==', 'lxml==', 'pandas==', 'numpy==', 
             'plotly==', 'kaleido==', 'openpyxl==', 'xlrd==', 'scipy==', 
             'scikit-learn==', 'python-Levenshtein==']

for line in lines:
    if any(s in line for s in skip_list):
        continue
    new_lines.append(line)

with open(req_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)


# ==========================================
# 3. CLEAN DOCKER-COMPOSE.YML
# ==========================================
compose_path = os.path.join(base_dir, 'backend', 'Docker - docker-compose.yml')
with open(compose_path, 'r', encoding='utf-8') as f:
    c_lines = f.readlines()

new_compose = []
skip = False
for line in c_lines:
    if "OPENAI_API_KEY" in line:
        continue
        
    if "BASE DE DONN" in line and "POSTGRESQL" in line:
        skip = True
    
    if skip and "REDIS (CACHE" in line:
        skip = False
        
    if skip:
        continue
        
    if "depends_on:" in line:
        pass # Handle carefully
    
    # We'll just remove the postgres block, and references to it
    if "postgres_data:" in line:
        continue
    if "driver: local" in line and len(new_compose) > 0 and 'postgres_data' in new_compose[-1]:
        continue
        
    new_compose.append(line)

with open(compose_path, 'w', encoding='utf-8') as f:
    f.writelines(new_compose)


# ==========================================
# 4. DELETE USELESS MODULES FILES
# ==========================================
check_py = os.path.join(base_dir, 'backend', 'modules', 'check.py')
data_py = os.path.join(base_dir, 'backend', 'modules', 'data.py')
if os.path.exists(check_py):
    os.remove(check_py)
if os.path.exists(data_py):
    os.remove(data_py)

print("Nuke successfully executed.")
