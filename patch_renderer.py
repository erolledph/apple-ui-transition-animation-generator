import re

with open('index.html', 'r') as f:
    content = f.read()

# Replace the transform assignment in renderCanvas
target_replace = "domEl.style.transform = `translate(${el.props.x}px, ${el.props.y}px) scale(${scale}) rotate(${rot}deg)`;\n      domEl.style.opacity = op;"

new_assignment = """
      // Advanced Styles
      let extStyle = '';
      if (el.props.effect === 'glassmorphism') {
        extStyle += `background: var(--effect-glass-bg) !important; backdrop-filter: var(--effect-glass-blur); -webkit-backdrop-filter: var(--effect-glass-blur); border: 1px solid var(--effect-glass-border);`;
        if (el.type === 'text') extStyle += `text-shadow: 0 4px 10px rgba(0,0,0,0.5);`;
      } else if (el.props.effect === 'neumorphism') {
        extStyle += `box-shadow: 8px 8px 16px var(--effect-neumorph-dark), -8px -8px 16px var(--effect-neumorph-light);`;
      } else if (el.props.effect === 'neon') {
        extStyle += `box-shadow: var(--effect-neon-glow); border-color: var(--accent);`;
        if (el.type === 'text') extStyle += `text-shadow: var(--effect-neon-glow);`;
      }

      if (el.type === 'text') {
        extStyle += `font-weight: ${el.props.weight || 600}; letter-spacing: ${el.props.letterSpacing || 0}px;`;
      }

      if (el.props.borderRadius !== undefined && el.type !== 'text') {
        extStyle += `border-radius: ${el.props.borderRadius}px;`;
      }

      let baseScale = el.props.scale !== undefined ? el.props.scale : 1;
      let baseRot = el.props.rotation || 0;
      let baseOp = el.props.opacity !== undefined ? el.props.opacity : 1;

      domEl.style.cssText += `
        transform: translate(${el.props.x}px, ${el.props.y}px) scale(${scale * baseScale}) rotate(${rot + baseRot}deg);
        opacity: ${op * baseOp};
        ${extStyle}
      `;
"""
content = content.replace(target_replace, new_assignment)

# Also fix the inner text gradient
text_target = "domEl.style.color = el.props.color;"
new_text_target = """
        if (el.props.textGradient && el.props.textGradient.trim() !== '') {
          domEl.style.background = el.props.textGradient;
          domEl.style.webkitBackgroundClip = 'text';
          domEl.style.webkitTextFillColor = 'transparent';
        } else {
          domEl.style.color = el.props.color;
        }
"""
content = content.replace(text_target, new_text_target)

with open('index.html', 'w') as f:
    f.write(content)
