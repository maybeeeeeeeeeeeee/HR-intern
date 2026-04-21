import sys
sys.stdout.reconfigure(encoding='utf-8')

# =============================================
# 1. BACKEND: Add auto-archive check in get_sources
# =============================================
filepath = r'c:\Users\ACH\Downloads\AI-Finder - final\backend\app.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Add auto-archive check right after fetching sources, before building result
old_get_sources = """        result = []
        for s in sources:"""

new_get_sources = """        # Auto-archivage: vérifier les sources dont auto_archive_days a expiré
        for s in sources:
            auto_days = s[10] if len(s) > 10 else None
            is_archived = s[9] if len(s) > 9 else 0
            last_updated = s[4]
            if auto_days and not is_archived and last_updated:
                try:
                    from datetime import datetime as dt_check
                    updated_date = dt_check.strptime(str(last_updated)[:19], '%Y-%m-%d %H:%M:%S')
                    if (datetime.now() - updated_date).days >= auto_days:
                        db.execute("UPDATE sources SET is_archived = 1 WHERE id = ?", (s[0],))
                        app.logger.info(f"Source {s[1]} auto-archivée après {auto_days} jours")
                except Exception as e:
                    app.logger.debug(f"Erreur auto-archivage: {e}")
        
        # Re-fetch after auto-archive
        sources = db.execute(\"\"\"
            SELECT id, name, type, path, last_updated, next_update, 
                   update_frequency, metadata, is_active, is_archived, auto_archive_days, allowed_roles
            FROM sources 
            WHERE user_id = ? AND is_active = 1 AND (allowed_roles IS NULL OR allowed_roles LIKE '%' || ? || '%')
            ORDER BY is_archived ASC, last_updated DESC
        \"\"\", (g.user_id, g.role), fetch=True)
        
        result = []
        for s in sources:"""

content = content.replace(old_get_sources, new_get_sources, 1)

# Fix duplicate metadata line
content = content.replace(
    "                'metadata': json.loads(s[7]) if s[7] else {},\n                'metadata': json.loads(s[7]) if s[7] else {},",
    "                'metadata': json.loads(s[7]) if s[7] else {},",
    1
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ Backend updated")

# =============================================
# 2. FRONTEND: Add ⚙️ button + show days info
# =============================================
frontend_path = r'c:\Users\ACH\Downloads\AI-Finder - final\frontend\index.html'
with open(frontend_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Add the ⚙️ configure button next to archive button
old_actions = """                actionButtons = `
                    <div class="source-actions">
                        ${archiveBtn}
                        <button class="btn-icon btn-delete" onclick="deleteSource('${s.id}')" title="Supprimer">✕</button>
                    </div>
                `;"""

new_actions = """                const configBtn = !s.is_archived
                    ? \`<button class="btn-icon" onclick="event.stopPropagation(); configureArchive('\${s.id}', \${s.auto_archive_days || 'null'})" title="Auto-archivage" style="font-size: 14px;">⚙️</button>\`
                    : '';

                actionButtons = \`
                    <div class="source-actions">
                        \${configBtn}
                        \${archiveBtn}
                        <button class="btn-icon btn-delete" onclick="deleteSource('\${s.id}')" title="Supprimer">✕</button>
                    </div>
                \`;"""

html = html.replace(old_actions, new_actions, 1)

# Add auto_archive_days info in the source meta display
old_meta = """<div class="source-meta">${date}</div>"""
new_meta = """<div class="source-meta">\${date}\${s.auto_archive_days ? ' · ⏱ Auto-archive: ' + s.auto_archive_days + 'j' : ''}</div>"""

html = html.replace(old_meta, new_meta, 1)

# Add the auto-archive info in source details modal
old_details_archived = """${s.is_archived ? '<div style="color: var(--text-muted); font-style: italic; font-size: 12px;">Ce fichier est archivé.</div>' : ''}"""

new_details_archived = """<div style="margin-bottom: 16px;">
                        <label class="form-label">Auto-archivage</label>
                        <div class="input" style="background: #f9fafb;">\${s.auto_archive_days ? s.auto_archive_days + ' jours après ajout' : 'Désactivé'}</div>
                    </div>
                    \${s.is_archived ? '<div style="color: var(--text-muted); font-style: italic; font-size: 12px;">Ce fichier est archivé.</div>' : ''}"""

html = html.replace(old_details_archived, new_details_archived, 1)

with open(frontend_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("✅ Frontend updated")
