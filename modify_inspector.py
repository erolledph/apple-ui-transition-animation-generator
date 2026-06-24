import re

with open('index.html', 'r') as f:
    content = f.read()

# Add expanded properties to elements and rendering
# Specifically, update the inspector HTML first

inspector_css = """
  .inspector-group { padding: 12px 16px; border-bottom: 1px solid var(--border); }
  .inspector-group-title { font-size: 11px; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 12px; }
  .prop-row { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; gap: 8px; }
  .prop-label { font-size: 12px; color: var(--text-tertiary); width: 80px; flex-shrink: 0; }
  .prop-input { flex: 1; background: rgba(255, 255, 255, 0.05); border: 1px solid var(--border); color: var(--text); padding: 5px 8px; border-radius: 6px; font-size: 12px; font-family: inherit; width: 100%; }
  .prop-input:focus { border-color: var(--accent); outline: none; }
  .prop-select { flex: 1; background: rgba(255, 255, 255, 0.05); border: 1px solid var(--border); color: var(--text); padding: 5px 8px; border-radius: 6px; font-size: 12px; width: 100%; outline: none; }

  /* Color picker combo */
  .color-picker-wrap { display: flex; flex: 1; gap: 4px; }
  .color-preview { width: 24px; height: 24px; border-radius: 4px; border: 1px solid var(--border); cursor: pointer; flex-shrink: 0; }
  .color-hex { flex: 1; background: rgba(255, 255, 255, 0.05); border: 1px solid var(--border); color: var(--text); padding: 4px 6px; border-radius: 4px; font-size: 11px; font-family: monospace; }
"""
content = content.replace('/* ====== RIGHT SIDEBAR ====== */', '/* ====== RIGHT SIDEBAR ====== */\n' + inspector_css)


fonts_list = [
    "Inter", "SF Pro Display", "Geist", "Outfit", "Plus Jakarta Sans", "DM Sans", "Manrope", "Sora", "Nunito", "Poppins", "Raleway", "Montserrat", "Urbanist", "Figtree", "Onest",
    "Playfair Display", "Lora", "Merriweather", "Cormorant Garamond", "DM Serif Display", "Fraunces",
    "JetBrains Mono", "Fira Code", "Space Mono", "IBM Plex Mono",
    "Clash Display", "Cabinet Grotesk", "Satoshi", "General Sans", "Bebas Neue", "Righteous"
]

fonts_options = "".join([f'<option value="{f}">{f}</option>' for f in fonts_list])


# Let's find `function renderInspector()` and inject new UI elements
# We will inject the HTML generation inside renderInspector based on element type

with open('index.html', 'w') as f:
    f.write(content)
