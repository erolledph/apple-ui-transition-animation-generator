import re

with open('index.html', 'r') as f:
    content = f.read()

# Enhance startVideoExport to support WebM output explicitly and ensure HTML2Canvas plays well if native isn't enough,
# though it looks like it already uses canvas rendering and MediaRecorder. Let's make sure audio is supported and add code generation tools.

# Let's add export options for React/CSS code generation
code_gen_html = """
<div id="codeExportModal" class="modal-overlay">
  <div class="modal">
    <div class="modal-header">
      <div class="panel-title">Export Code</div>
      <button class="icon-btn" id="closeCodeExport"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6L6 18M6 6l12 12"/></svg></button>
    </div>
    <div class="modal-body">
      <div class="export-options" style="margin-bottom: 12px; display: flex; gap: 8px;">
        <button class="opt-btn active" id="btnExportCSS">CSS Keyframes</button>
        <button class="opt-btn" id="btnExportReact">React / Framer</button>
      </div>
      <textarea id="codeExportArea" style="width: 100%; height: 300px; background: rgba(0,0,0,0.5); color: var(--text); border: 1px solid var(--border); border-radius: 8px; padding: 12px; font-family: monospace; font-size: 12px; resize: none;" readonly></textarea>
    </div>
    <div class="modal-footer">
      <button class="btn-primary" id="copyCodeBtn">Copy to Clipboard</button>
    </div>
  </div>
</div>
"""

# inject right before `</body>`
content = content.replace("</body>", code_gen_html + "\n</body>")

# Add TopBar Button for Code
topbar_btn = """      <button class="btn-ghost" id="exportCodeBtn">Code</button>\n      <button class="btn-ghost" id="exportGifBtn">"""
content = content.replace('      <button class="btn-ghost" id="exportGifBtn">', topbar_btn)

with open('index.html', 'w') as f:
    f.write(content)
