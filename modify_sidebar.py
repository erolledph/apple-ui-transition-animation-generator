import re

with open('index.html', 'r') as f:
    content = f.read()

# Add CSS for tabs
css_additions = """
  /* ====== SIDEBAR TABS ====== */
  .sidebar-tabs { display: flex; border-bottom: 1px solid var(--border); }
  .sidebar-tab { flex: 1; padding: 12px; background: transparent; border: none; color: var(--text-secondary); font-size: 13px; font-weight: 500; cursor: pointer; transition: all 0.15s ease; border-bottom: 2px solid transparent; }
  .sidebar-tab.active { color: var(--text); border-bottom-color: var(--accent); }
  .sidebar-tab:hover:not(.active) { color: var(--text); background: rgba(255, 255, 255, 0.05); }

  .sidebar-pane { display: flex; flex-direction: column; flex: 1; overflow: hidden; }
  .sidebar-pane:not(.active) { display: none; }

  /* ====== MEDIA LIBRARY ====== */
  .media-upload-area {
    margin: 16px; padding: 24px 16px; border: 2px dashed var(--border-strong); border-radius: 12px;
    text-align: center; color: var(--text-tertiary); font-size: 13px; cursor: pointer; transition: all 0.2s ease;
  }
  .media-upload-area:hover, .media-upload-area.drag-over { border-color: var(--accent); background: var(--accent-soft); color: var(--accent); }

  .media-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; padding: 0 16px 16px; overflow-y: auto; flex: 1; }
  .media-item {
    aspect-ratio: 1; background: rgba(255, 255, 255, 0.05); border-radius: 8px; border: 1px solid var(--border);
    overflow: hidden; position: relative; cursor: grab; display: flex; align-items: center; justify-content: center;
  }
  .media-item:hover { border-color: var(--border-strong); }
  .media-item img, .media-item video { width: 100%; height: 100%; object-fit: cover; }
  .media-item .media-type { position: absolute; bottom: 4px; right: 4px; background: rgba(0,0,0,0.6); padding: 2px 4px; border-radius: 4px; font-size: 9px; font-weight: bold; }
  .media-item .media-name { position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(transparent, rgba(0,0,0,0.8)); padding: 12px 4px 4px; font-size: 10px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
"""

content = content.replace('/* ====== LEFT SIDEBAR ====== */', '/* ====== LEFT SIDEBAR ====== */\n' + css_additions)


# Update HTML
sidebar_start = content.find('<aside class="sidebar-left">')
sidebar_end = content.find('</aside>', sidebar_start) + len('</aside>')

old_sidebar = content[sidebar_start:sidebar_end]

new_sidebar = """<aside class="sidebar-left">
    <div class="sidebar-tabs">
      <button class="sidebar-tab active" data-tab="layers">Layers</button>
      <button class="sidebar-tab" data-tab="media">Media</button>
    </div>
    <div class="sidebar-pane active" id="pane-layers">
""" + old_sidebar[len('<aside class="sidebar-left">'):-len('</aside>')] + """
    </div>
    <div class="sidebar-pane" id="pane-media">
      <input type="file" id="mediaFileInput" multiple accept="image/*,video/*,audio/*" style="display: none;">
      <div class="media-upload-area" id="mediaUploadArea">
        Drag & Drop files here<br>or click to browse
      </div>
      <div class="media-grid" id="mediaGrid"></div>
    </div>
  </aside>"""

content = content[:sidebar_start] + new_sidebar + content[sidebar_end:]

with open('index.html', 'w') as f:
    f.write(content)
