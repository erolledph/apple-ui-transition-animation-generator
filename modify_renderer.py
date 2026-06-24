import re

with open('index.html', 'r') as f:
    content = f.read()

# Let's find renderCanvas() and inject the advanced effect CSS generation logic
# The element is created and styled in a loop inside renderCanvas.

start_str = "    const t = state.currentTime;"
end_str = "      if (state.selectedId === el.id) {"

start_idx = content.find(start_str)
end_idx = content.find(end_str)

if start_idx != -1 and end_idx != -1:
    old_loop = content[start_idx:end_idx]

    # We want to patch where elements are styled.
    # Currently it sets domEl.style.transform = ...
    # We need to add the effects.

    inject = """
      // Advanced Styles
      let extStyle = '';
      if (el.props.effect === 'glassmorphism') {
        extStyle += `background: var(--effect-glass-bg) !important; backdrop-filter: var(--effect-glass-blur); -webkit-backdrop-filter: var(--effect-glass-blur); border: 1px solid var(--effect-glass-border);`;
      } else if (el.props.effect === 'neumorphism') {
        extStyle += `box-shadow: 8px 8px 16px var(--effect-neumorph-dark), -8px -8px 16px var(--effect-neumorph-light);`;
      } else if (el.props.effect === 'neon') {
        extStyle += `box-shadow: var(--effect-neon-glow); border-color: var(--accent);`;
      } else if (el.props.effect === 'glitch') {
        // Will be handled via animation
      }

      if (el.type === 'text') {
        extStyle += `font-weight: ${el.props.weight || 600}; letter-spacing: ${el.props.letterSpacing || 0}px;`;
        if (el.props.textGradient) {
            extStyle += `background: ${el.props.textGradient}; -webkit-background-clip: text; -webkit-text-fill-color: transparent;`;
        }
      }

      if (el.props.borderRadius !== undefined && el.type !== 'text') {
        extStyle += `border-radius: ${el.props.borderRadius}px;`;
      }

      domEl.style.cssText = `
        position: absolute; left: 0; top: 0;
        width: ${el.props.width}px; height: ${el.props.height}px;
        transform: translate(${el.props.x}px, ${el.props.y}px) scale(${scale * (el.props.scale||1)}) rotate(${rot + (el.props.rotation||0)}deg);
        opacity: ${op * (el.props.opacity!==undefined?el.props.opacity:1)};
        pointer-events: auto;
        ${extStyle}
      `;

      // We also need to override the inner properties, so let's let the original code run its switch case but override wrapper style
"""

    # We will search for `domEl.style.transform = ` inside renderCanvas and replace it.

with open('index.html', 'w') as f:
    f.write(content)
