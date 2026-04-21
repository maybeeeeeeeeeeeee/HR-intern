import re
import os

filepath = r'c:\Users\ACH\Downloads\AI-Finder - final\backend\app.py'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove refresh
content = re.sub(r"@app\.route\('/api/sources/<source_id>/refresh', methods=\['POST'\]\).*?(?=@app\.route\('/api/sources/<source_id>', methods=\['DELETE'\]\))", "", content, flags=re.DOTALL)

# 2. Remove process_enhanced_query
content = re.sub(r"@app\.route\('/api/query/enhanced', methods=\['POST'\]\)\n@login_required\ndef process_enhanced_query\(\):.*?(?=@app\.route\('/api/data/analyze/<source_id>', methods=\['GET'\]\))", "", content, flags=re.DOTALL)

# 3. Remove analyze_data_source
content = re.sub(r"@app\.route\('/api/data/analyze/<source_id>', methods=\['GET'\]\)\n@login_required\ndef analyze_data_source\(source_id\):.*?(?=\nif __name__ == '__main__':)", "", content, flags=re.DOTALL)

# Clean up imports and instantiation
content = re.sub(r"from modules\.data import StructuredDataProcessor\n", "", content)
content = re.sub(r"import pandas as pd\n", "", content)
content = re.sub(r"import numpy as np\n", "", content)
content = re.sub(r"data_processor = StructuredDataProcessor\(\)\n", "", content)

# Remove prints
content = re.sub(r"    print\(f\"ðŸ“ˆ Visualization: âœ… Activé\"\)\n", "", content)
content = re.sub(r"    print\(f\"ðŸ“Š Structured Data: âœ… Activé\"\)\n", "", content)

# Also fix the convert_to_serializable so it doesn't need numpy if possible
# Since we removed numpy import, the convert_to_serializable might crash if np is used.
# Let's remove the np parts from convert_to_serializable:
numpy_checks = r"    if isinstance\(obj, np\.integer\):\n        return int\(obj\)\n    if isinstance\(obj, np\.floating\):\n        return float\(obj\)\n    if isinstance\(obj, np\.ndarray\):\n        return obj\.tolist\(\)\n"
content = content.replace(numpy_checks, "")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Final clean completed")
