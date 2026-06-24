import re

with open('index.html', 'r') as f:
    content = f.read()

# Add CSS for Rulers, Guides, and Safe Zone
canvas_css = """
  /* ====== CANVAS ENHANCEMENTS ====== */
  .canvas-ruler-h { position: absolute; top: 0; left: 20px; right: 0; height: 20px; background: rgba(255,255,255,0.02); border-bottom: 1px solid var(--border); z-index: 10; pointer-events: none; overflow: hidden; }
  .canvas-ruler-v { position: absolute; top: 20px; left: 0; bottom: 0; width: 20px; background: rgba(255,255,255,0.02); border-right: 1px solid var(--border); z-index: 10; pointer-events: none; overflow: hidden; }
  .canvas-corner { position: absolute; top: 0; left: 0; width: 20px; height: 20px; background: var(--bg-glass); border-right: 1px solid var(--border); border-bottom: 1px solid var(--border); z-index: 11; }

  .ruler-tick { position: absolute; background: var(--border-strong); }
  .ruler-tick-h { top: 12px; height: 8px; width: 1px; }
  .ruler-tick-v { left: 12px; width: 8px; height: 1px; }
  .ruler-label { position: absolute; font-size: 9px; color: var(--text-tertiary); font-family: monospace; }
  .ruler-label-h { top: 2px; transform: translateX(-50%); }
  .ruler-label-v { left: 2px; transform: translateY(-50%) rotate(-90deg); transform-origin: left center; }

  .canvas-safe-zone {
    position: absolute; border: 1px dashed rgba(255,255,255,0.2); pointer-events: none; z-index: 5;
    left: 10%; right: 10%; top: 10%; bottom: 10%; display: none;
  }
  .canvas-safe-zone.visible { display: block; }

  /* Alignment Toolbar */
  .align-toolbar {
    position: absolute; top: 30px; left: 50%; transform: translateX(-50%);
    background: var(--bg-glass-strong); padding: 4px; border-radius: 8px; border: 1px solid var(--border);
    display: none; gap: 4px; z-index: 20; box-shadow: var(--shadow-lg);
  }
  .align-toolbar.visible { display: flex; }
  .align-btn { background: transparent; border: none; color: var(--text-secondary); width: 28px; height: 28px; border-radius: 4px; cursor: pointer; display: flex; align-items: center; justify-content: center; }
  .align-btn:hover { background: rgba(255,255,255,0.1); color: var(--text); }

  /* Selection Marquee */
  .selection-marquee {
    position: absolute; border: 1px solid var(--accent); background: rgba(10, 132, 255, 0.1);
    pointer-events: none; z-index: 100; display: none;
  }
"""

content = content.replace('/* ====== CANVAS AREA ====== */', '/* ====== CANVAS AREA ====== */\n' + canvas_css)

# Update HTML layout for the canvas
canvas_html_old = """
    <div class="canvas-wrap" id="canvasWrap">
      <div class="canvas-stage" id="canvasStage">
        <div class="canvas-bg" id="canvasBg"></div>
        <div class="canvas-grid-overlay" id="canvasGridOverlay"></div>
        <div class="canvas-elements" id="canvasElements"></div>
      </div>
    </div>
"""

canvas_html_new = """
    <div class="align-toolbar" id="alignToolbar">
      <button class="align-btn" data-align="left" title="Align Left"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 22V2M4 12h10M4 6h16M4 18h16"/></svg></button>
      <button class="align-btn" data-align="center" title="Align Center"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22V2M6 12h12M4 6h16M4 18h16"/></svg></button>
      <button class="align-btn" data-align="right" title="Align Right"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 22V2M10 12h10M4 6h16M4 18h16"/></svg></button>
      <div style="width:1px; background:var(--border); margin:0 2px;"></div>
      <button class="align-btn" data-align="top" title="Align Top"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 4h20M12 4v10M6 4v16M18 4v16"/></svg></button>
      <button class="align-btn" data-align="middle" title="Align Middle"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 12h20M12 6v12M6 4v16M18 4v16"/></svg></button>
      <button class="align-btn" data-align="bottom" title="Align Bottom"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 20h20M12 10v10M6 4v16M18 4v16"/></svg></button>
    </div>
    <div class="canvas-wrap" id="canvasWrap">
      <div class="canvas-corner"></div>
      <div class="canvas-ruler-h" id="rulerH"></div>
      <div class="canvas-ruler-v" id="rulerV"></div>
      <div class="selection-marquee" id="marquee"></div>
      <div class="canvas-stage" id="canvasStage">
        <div class="canvas-bg" id="canvasBg"></div>
        <div class="canvas-grid-overlay" id="canvasGridOverlay"></div>
        <div class="canvas-safe-zone" id="canvasSafeZone"></div>
        <div class="canvas-elements" id="canvasElements"></div>
      </div>
    </div>
"""

content = content.replace(canvas_html_old, canvas_html_new)

# Add topbar button for safe zone
btn_old = """<button class="ctrl-btn" id="gridBtn" title="Toggle Grid (G)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 3h18v18H3zM9 3v18M15 3v18M3 9h18M3 15h18"/></svg></button>"""
btn_new = btn_old + """\n        <button class="ctrl-btn" id="safeZoneBtn" title="Toggle Safe Zone"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="5" y="5" width="14" height="14" rx="2" stroke-dasharray="4 4"/></svg></button>"""
content = content.replace(btn_old, btn_new)


with open('index.html', 'w') as f:
    f.write(content)
