import re
import os

filepath = r'c:\Users\ACH\Downloads\AI-Finder - final\backend\app.py'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Supprimer les imports de check
content = re.sub(r"from modules\.check import HallucinationDetector, ReliabilityScorer\n", "", content)

# 2. Supprimer OPENAI_API_KEY def
content = re.sub(r"OPENAI_API_KEY = os\.getenv\('OPENAI_API_KEY'\)\n", "", content)

# 3. Supprimer l'instanciation des modules checks
modules_start = "hallucination_detector = HallucinationDetector()\nreliability_scorer = ReliabilityScorer()\n"
content = content.replace(modules_start, "")

# 4. Supprimer get_openai_client()
content = re.sub(r"# ============================================================================\n# CLIENT OPENAI ROBUSTE\n# ============================================================================.*?def get_openai_client\(\):.*?return client\n", "", content, flags=re.DOTALL)

# 5. Supprimer faux add_query_result dans process_query
# A cause de l'indentation on supprime 'reliability_scorer.add_query_result(verification)'
content = re.sub(r"[ \t]*reliability_scorer\.add_query_result\(verification\)\n", "", content)

# 6. Supprimer extract_comparison_from_text (bien que peut-être déjà en partie retiré ou inutile)
content = re.sub(r"def extract_comparison_from_text\(query, chunks\):.*?return None\n", "", content, flags=re.DOTALL)

# 7. Supprimer /api/query/enhanced
content = re.sub(r"# ============================================================================\n# NOUVELLES FONCTIONNALITÃ‰S AVANCÃ‰ES\n# ============================================================================.*?@app\.route\('/api/query/enhanced', methods=\['POST'\]\).*?# ============================================================================", "# ============================================================================", content, flags=re.DOTALL)

# 8. Nettoyer les vérifications dans main()
content = content.replace("print(f\"ðŸ¤– AI: OpenAI GPT-4o-mini\")", "print(f\"ðŸ¤– AI: RAG Local (Autonome)\")")
content = content.replace("print(f\"ðŸŽ¯ Anti-Hallucination: âœ… Activé\")\n", "")
content = content.replace("    if not OPENAI_API_KEY:\n        print(\"âš ï¸   ATTENTION: Créez un fichier .env avec:\")\n        print(\"   OPENAI_API_KEY=votre_cle\")\n        print(\"   JWT_SECRET=votre_secret_jwt\")\n        print(\"   ENCRYPTION_KEY=votre_cle_chiffrement\")", "    if not JWT_SECRET:\n        print(\"âš ï¸   ATTENTION: Vérifiez votre .env (JWT_SECRET, ENCRYPTION_KEY)\")")
content = content.replace("'api_configured': OPENAI_API_KEY is not None,", "'api_configured': True,")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Nettoyage OpenAI effectué.")
