import re

with open('index.html', 'r') as f:
    content = f.read()

css_additions = """
    /* Advanced Effect Variables */
    --effect-glass-bg: rgba(255, 255, 255, 0.05);
    --effect-glass-border: rgba(255, 255, 255, 0.1);
    --effect-glass-blur: blur(20px) saturate(150%);

    --effect-neumorph-light: rgba(255, 255, 255, 0.05);
    --effect-neumorph-dark: rgba(0, 0, 0, 0.5);

    --effect-neon-glow: 0 0 10px var(--accent), 0 0 20px var(--accent), 0 0 40px var(--accent);
"""

content = content.replace('--shadow-lg: 0 20px 60px rgba(0, 0, 0, 0.6);', '--shadow-lg: 0 20px 60px rgba(0, 0, 0, 0.6);' + css_additions)

with open('index.html', 'w') as f:
    f.write(content)
