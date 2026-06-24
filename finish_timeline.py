import re

with open('index.html', 'r') as f:
    content = f.read()

# Make sure CSS matches the HTML classes used in tracks
timeline_css = """
  /* ====== NEW TIMELINE CSS ====== */
  .tl-bar.full-clip {
    cursor: grab;
    transition: box-shadow 0.15s ease;
  }
  .tl-bar.full-clip:active { cursor: grabbing; box-shadow: 0 0 0 2px var(--accent); }
  .tl-track.active { background: rgba(255,255,255,0.05); }
  .tl-track.multi-selected { background: rgba(10, 132, 255, 0.1); }
  #timelineRuler { cursor: text; } /* Indicates playhead scrubbing */
"""

content = content.replace('/* ====== TIMELINE ====== */', '/* ====== TIMELINE ====== */\n' + timeline_css)


with open('index.html', 'w') as f:
    f.write(content)
