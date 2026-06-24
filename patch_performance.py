import re

with open('index.html', 'r') as f:
    content = f.read()

# Add hardware acceleration via `will-change: transform, opacity`
hardware_css = """
  .canvas-element {
    position: absolute; pointer-events: auto; transform-origin: center center;
    box-sizing: border-box; overflow: hidden;
    will-change: transform, opacity, filter; /* Hardware acceleration */
  }
"""
content = content.replace('.canvas-element { position: absolute; pointer-events: auto; transform-origin: center center; box-sizing: border-box; overflow: hidden; }', hardware_css)

# Add debouncing to window resize
# Look for resize event
content = content.replace("window.addEventListener('resize', () => { clearTimeout(resizeTimer); resizeTimer = setTimeout(() => { renderTimeline(); initEditorCanvas(); }, 100); });", "window.addEventListener('resize', () => { clearTimeout(resizeTimer); resizeTimer = setTimeout(() => { requestAnimationFrame(() => { renderTimeline(); initEditorCanvas(); renderAll(); }); }, 100); });")

with open('index.html', 'w') as f:
    f.write(content)
