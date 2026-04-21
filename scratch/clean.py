import re
import os

filepath = r'c:\Users\ACH\Downloads\AI-Finder - final\backend\app.py'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Supprimer add_web_source
content = re.sub(r"@app\.route\('/api/sources/web'.*?(?=@app\.route\('/api/sources/database')", "", content, flags=re.DOTALL)

# 2. Supprimer add_database_source
content = re.sub(r"@app\.route\('/api/sources/database'.*?(?=@app\.route\('/api/sources/<source_id>/refresh')", "", content, flags=re.DOTALL)

# 3. Nettoyer refresh_source pour retirer web et database
refresh_old = """        # Actualisation selon le type
        if source_type == 'web':
            new_content = scrape_website(path)
        
        elif source_type == 'database':
            metadata = json.loads(source[3])
            config = json.loads(decrypt_sensitive_data(source[2]))
            
            if metadata['db_type'] == 'postgresql':
                conn = psycopg2.connect(**config)
                cursor = conn.cursor()
                cursor.execute(metadata['query'])
                results = cursor.fetchall()
                new_content = json.dumps(results, default=str)
                conn.close()
        
        else:"""
refresh_new = """        # Actualisation selon le type (plus de web/database)
        if False:
            pass
        else:"""
content = content.replace(refresh_old, refresh_new)

# 4. Supprimer scrape_website()
content = re.sub(r"def scrape_website\(url\):.*?return content\n    except Exception as e:\n        raise Exception\(f\"Erreur scraping: \{str\(e\)\}\"\)\n", "", content, flags=re.DOTALL)

# 5. Supprimer scheduler (auto_update_sources, schedule_source_update, run_scheduler et appel thread)
content = re.sub(r"# ============================================================================\n# ACTUALISATION AUTOMATIQUE DES SOURCES\n# ============================================================================.*?# ============================================================================\n# FONCTIONS UTILITAIRES\n# ============================================================================", "# ============================================================================\n# FONCTIONS UTILITAIRES\n# ============================================================================", content, flags=re.DOTALL)

# 5b. Supprimer run_auto_archiving_job
content = re.sub(r"def run_auto_archiving_job\(\):.*?print\(f\"Erreur job auto-archivage: \{e\}\"\)\n", "", content, flags=re.DOTALL)

# 6. Supprimer le doublon /api/sources/file/structured et /api/data/insights/
# Ces routes sont situées entre "# CORRECTION 1: Fonction add_structured_file() corrigée" et "if __name__ == '__main__':"
content = re.sub(r"# ============================================================================\n# CORRECTION 1: Fonction add_structured_file\(\) corrigée\n# ============================================================================.*?(?=if __name__ == '__main__':)", "", content, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Nettoyage effectué.")
