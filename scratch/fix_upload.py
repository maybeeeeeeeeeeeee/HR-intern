filepath = r'c:\Users\ACH\Downloads\AI-Finder - final\backend\app.py'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the dead CSV/Excel redirect + old extraction block
old_block = """        # \u2705 SI CSV/EXCEL \u2192 ROUTE STRUCTUR\u00c9E
        if file_ext in ['csv', 'xlsx', 'xls']:
            # Rediriger vers le traitement structur\u00e9
            file.seek(0)  # R\u00e9initialiser le curseur
            return add_structured_file_direct(file, filename, file_ext)
        
        # Extraction du contenu pour autres formats
        if file_ext == 'pdf':
            content = extract_pdf_content(file_data)
        elif file_ext == 'docx':
            content = extract_docx_content(file_data)
        else:
            content = file_data.decode('utf-8', errors='ignore')"""

new_block = """        # Extraction du contenu selon le format
        if file_ext == 'pdf':
            content = extract_pdf_content(file_data)
        elif file_ext == 'docx':
            content = extract_docx_content(file_data)
        elif file_ext == 'csv':
            content = extract_csv_content(file_data)
        else:
            content = file_data.decode('utf-8', errors='ignore')"""

if old_block in content:
    content = content.replace(old_block, new_block)
    print("Block replaced successfully!")
else:
    print("ERROR: old block not found, trying line-by-line...")
    # Try finding the lines individually
    lines = content.split('\n')
    new_lines = []
    skip_until_extract = False
    for i, line in enumerate(lines):
        if 'SI CSV/EXCEL' in line:
            skip_until_extract = True
            # Insert new block
            new_lines.append('        # Extraction du contenu selon le format')
            continue
        if skip_until_extract:
            if "content = file_data.decode('utf-8', errors='ignore')" in line:
                # This is the last line of old block, insert new extraction
                new_lines.append('        if file_ext == \'pdf\':')
                new_lines.append('            content = extract_pdf_content(file_data)')
                new_lines.append('        elif file_ext == \'docx\':')
                new_lines.append('            content = extract_docx_content(file_data)')
                new_lines.append('        elif file_ext == \'csv\':')
                new_lines.append('            content = extract_csv_content(file_data)')
                new_lines.append('        else:')
                new_lines.append("            content = file_data.decode('utf-8', errors='ignore')")
                skip_until_extract = False
                continue
            else:
                continue
        new_lines.append(line)
    content = '\n'.join(new_lines)
    print("Line-by-line replacement done!")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("File saved.")
