import re

with open('index.html', 'r') as f:
    content = f.read()

# We need to replace the entire renderInspector function to handle the advanced properties
# Let's find the start and end of it.

start_str = "function renderInspector() {"
end_str = "function renderChapterList() {"

start_idx = content.find(start_str)
end_idx = content.find(end_str)

if start_idx != -1 and end_idx != -1:
    old_inspector = content[start_idx:end_idx]

    # We will build a new inspector function
    new_inspector = """function renderInspector() {
    const p = document.getElementById('inspectorPanel');
    if (!state.selectedId) {
      p.innerHTML = '<div style="padding:20px;color:var(--text-tertiary);text-align:center;">No element selected</div>';
      return;
    }
    const el = state.elements.find(e => e.id === state.selectedId);
    if (!el) return;

    let html = `
      <div class="panel-header">
        <span class="panel-title">${el.name}</span>
      </div>
      <div class="inspector-group">
        <div class="inspector-group-title">Transform</div>
        <div class="prop-row"><span class="prop-label">X</span><input type="number" class="prop-input" id="prop-x" value="${Math.round(el.props.x)}"></div>
        <div class="prop-row"><span class="prop-label">Y</span><input type="number" class="prop-input" id="prop-y" value="${Math.round(el.props.y)}"></div>
        <div class="prop-row"><span class="prop-label">W / H</span><div style="display:flex;gap:4px;flex:1"><input type="number" class="prop-input" id="prop-w" value="${Math.round(el.props.width)}"><input type="number" class="prop-input" id="prop-h" value="${Math.round(el.props.height)}"></div></div>
        <div class="prop-row"><span class="prop-label">Rotation</span><input type="number" class="prop-input" id="prop-rot" value="${el.props.rotation || 0}"></div>
        <div class="prop-row"><span class="prop-label">Scale</span><input type="number" class="prop-input" id="prop-scale" step="0.1" value="${el.props.scale !== undefined ? el.props.scale : 1}"></div>
        <div class="prop-row"><span class="prop-label">Opacity</span><input type="number" class="prop-input" id="prop-opacity" step="0.1" min="0" max="1" value="${el.props.opacity !== undefined ? el.props.opacity : 1}"></div>
      </div>
    `;

    if (el.type === 'text') {
      html += `
        <div class="inspector-group">
          <div class="inspector-group-title">Typography</div>
          <div class="prop-row"><span class="prop-label">Text</span><input type="text" class="prop-input" id="prop-text" value="${el.props.text}"></div>
          <div class="prop-row"><span class="prop-label">Font</span>
            <select class="prop-select" id="prop-font">
              <optgroup label="Sans-Serif">
                <option value="Inter" ${el.props.font==='Inter'?'selected':''}>Inter</option>
                <option value="SF Pro Display" ${el.props.font==='SF Pro Display'?'selected':''}>SF Pro Display</option>
                <option value="Geist" ${el.props.font==='Geist'?'selected':''}>Geist</option>
                <option value="Outfit" ${el.props.font==='Outfit'?'selected':''}>Outfit</option>
                <option value="Plus Jakarta Sans" ${el.props.font==='Plus Jakarta Sans'?'selected':''}>Plus Jakarta Sans</option>
                <option value="DM Sans" ${el.props.font==='DM Sans'?'selected':''}>DM Sans</option>
                <option value="Manrope" ${el.props.font==='Manrope'?'selected':''}>Manrope</option>
                <option value="Sora" ${el.props.font==='Sora'?'selected':''}>Sora</option>
                <option value="Nunito" ${el.props.font==='Nunito'?'selected':''}>Nunito</option>
                <option value="Poppins" ${el.props.font==='Poppins'?'selected':''}>Poppins</option>
                <option value="Raleway" ${el.props.font==='Raleway'?'selected':''}>Raleway</option>
                <option value="Montserrat" ${el.props.font==='Montserrat'?'selected':''}>Montserrat</option>
                <option value="Urbanist" ${el.props.font==='Urbanist'?'selected':''}>Urbanist</option>
                <option value="Figtree" ${el.props.font==='Figtree'?'selected':''}>Figtree</option>
                <option value="Onest" ${el.props.font==='Onest'?'selected':''}>Onest</option>
              </optgroup>
              <optgroup label="Serif">
                <option value="Playfair Display" ${el.props.font==='Playfair Display'?'selected':''}>Playfair Display</option>
                <option value="Lora" ${el.props.font==='Lora'?'selected':''}>Lora</option>
                <option value="Merriweather" ${el.props.font==='Merriweather'?'selected':''}>Merriweather</option>
                <option value="Cormorant Garamond" ${el.props.font==='Cormorant Garamond'?'selected':''}>Cormorant</option>
                <option value="DM Serif Display" ${el.props.font==='DM Serif Display'?'selected':''}>DM Serif</option>
                <option value="Fraunces" ${el.props.font==='Fraunces'?'selected':''}>Fraunces</option>
              </optgroup>
              <optgroup label="Monospace">
                <option value="JetBrains Mono" ${el.props.font==='JetBrains Mono'?'selected':''}>JetBrains Mono</option>
                <option value="Fira Code" ${el.props.font==='Fira Code'?'selected':''}>Fira Code</option>
                <option value="Space Mono" ${el.props.font==='Space Mono'?'selected':''}>Space Mono</option>
                <option value="IBM Plex Mono" ${el.props.font==='IBM Plex Mono'?'selected':''}>IBM Plex Mono</option>
              </optgroup>
              <optgroup label="Display">
                <option value="Clash Display" ${el.props.font==='Clash Display'?'selected':''}>Clash Display</option>
                <option value="Cabinet Grotesk" ${el.props.font==='Cabinet Grotesk'?'selected':''}>Cabinet Grotesk</option>
                <option value="Satoshi" ${el.props.font==='Satoshi'?'selected':''}>Satoshi</option>
                <option value="General Sans" ${el.props.font==='General Sans'?'selected':''}>General Sans</option>
                <option value="Bebas Neue" ${el.props.font==='Bebas Neue'?'selected':''}>Bebas Neue</option>
                <option value="Righteous" ${el.props.font==='Righteous'?'selected':''}>Righteous</option>
              </optgroup>
            </select>
          </div>
          <div class="prop-row"><span class="prop-label">Weight</span><input type="number" class="prop-input" id="prop-weight" step="100" min="100" max="900" value="${el.props.weight || 600}"></div>
          <div class="prop-row"><span class="prop-label">Size</span><input type="number" class="prop-input" id="prop-size" value="${el.props.size || 24}"></div>
          <div class="prop-row"><span class="prop-label">Color</span>
            <div class="color-picker-wrap">
              <input type="color" class="color-preview" id="prop-color-picker" value="${el.props.color}">
              <input type="text" class="color-hex" id="prop-color" value="${el.props.color}">
            </div>
          </div>
          <div class="prop-row"><span class="prop-label">Letter Spac.</span><input type="number" class="prop-input" id="prop-letter-spacing" step="0.5" value="${el.props.letterSpacing || 0}"></div>
          <div class="prop-row"><span class="prop-label">Gradient Fill</span><input type="text" class="prop-input" id="prop-text-gradient" placeholder="e.g. linear-gradient(90deg, red, blue)" value="${el.props.textGradient || ''}"></div>
        </div>
      `;
    }

    if (['card', 'button', 'circle'].includes(el.type)) {
      html += `
        <div class="inspector-group">
          <div class="inspector-group-title">Appearance</div>
          <div class="prop-row"><span class="prop-label">Color</span>
            <div class="color-picker-wrap">
              <input type="color" class="color-preview" id="prop-color-picker" value="${el.props.color}">
              <input type="text" class="color-hex" id="prop-color" value="${el.props.color}">
            </div>
          </div>
          <div class="prop-row"><span class="prop-label">Radius</span><input type="number" class="prop-input" id="prop-radius" value="${el.props.borderRadius !== undefined ? el.props.borderRadius : 16}"></div>
        </div>
      `;
    }

    // Add Advanced Effects to all element types
    html += `
      <div class="inspector-group">
        <div class="inspector-group-title">Advanced Effects</div>
        <div class="prop-row"><span class="prop-label">Effect Style</span>
          <select class="prop-select" id="prop-effect">
            <option value="none" ${el.props.effect==='none'?'selected':''}>None</option>
            <option value="glassmorphism" ${el.props.effect==='glassmorphism'?'selected':''}>Glassmorphism</option>
            <option value="neumorphism" ${el.props.effect==='neumorphism'?'selected':''}>Neumorphism</option>
            <option value="neon" ${el.props.effect==='neon'?'selected':''}>Neon Glow</option>
            <option value="glitch" ${el.props.effect==='glitch'?'selected':''}>Glitch Split</option>
          </select>
        </div>
      </div>
    `;

    // Animations section
    html += `
      <div class="inspector-group">
        <div class="inspector-group-title">Animations</div>
        <div class="prop-row"><span class="prop-label">In</span>
          <select class="prop-select" id="prop-anim-in">
            <option value="none" ${el.animIn==='none'?'selected':''}>None</option>
            <option value="fade" ${el.animIn==='fade'?'selected':''}>Fade</option>
            <option value="slide-up" ${el.animIn==='slide-up'?'selected':''}>Slide Up</option>
            <option value="scale-spring" ${el.animIn==='scale-spring'?'selected':''}>Scale Spring</option>
            <option value="swirl" ${el.animIn==='swirl'?'selected':''}>Swirl In</option>
            <option value="glitch" ${el.animIn==='glitch'?'selected':''}>Glitch Reveal</option>
          </select>
        </div>
        <div class="prop-row"><span class="prop-label">Out</span>
          <select class="prop-select" id="prop-anim-out">
            <option value="none" ${el.animOut==='none'?'selected':''}>None</option>
            <option value="fade" ${el.animOut==='fade'?'selected':''}>Fade</option>
            <option value="slide-down" ${el.animOut==='slide-down'?'selected':''}>Slide Down</option>
            <option value="scale-down" ${el.animOut==='scale-down'?'selected':''}>Scale Down</option>
            <option value="swirl" ${el.animOut==='swirl'?'selected':''}>Swirl Out</option>
            <option value="shatter" ${el.animOut==='shatter'?'selected':''}>Shatter</option>
          </select>
        </div>
      </div>
    `;

    p.innerHTML = html;

    // Bind events
    const updateProp = (key, val, isNumeric) => {
      pushHistory();
      if (isNumeric) val = parseFloat(val) || 0;
      el.props[key] = val;
      renderAll();
    };

    ['x','y','w','h','rot','scale','opacity'].forEach(k => {
      const elNode = document.getElementById('prop-'+k);
      if(elNode) elNode.addEventListener('change', e => {
        let keyMap = {x:'x',y:'y',w:'width',h:'height',rot:'rotation',scale:'scale',opacity:'opacity'};
        updateProp(keyMap[k], e.target.value, true);
      });
    });

    if (document.getElementById('prop-text')) document.getElementById('prop-text').addEventListener('input', e => { el.props.text = e.target.value; renderAll(); });
    if (document.getElementById('prop-font')) document.getElementById('prop-font').addEventListener('change', e => updateProp('font', e.target.value, false));
    if (document.getElementById('prop-weight')) document.getElementById('prop-weight').addEventListener('change', e => updateProp('weight', e.target.value, true));
    if (document.getElementById('prop-size')) document.getElementById('prop-size').addEventListener('change', e => updateProp('size', e.target.value, true));
    if (document.getElementById('prop-letter-spacing')) document.getElementById('prop-letter-spacing').addEventListener('change', e => updateProp('letterSpacing', e.target.value, true));
    if (document.getElementById('prop-text-gradient')) document.getElementById('prop-text-gradient').addEventListener('change', e => updateProp('textGradient', e.target.value, false));
    if (document.getElementById('prop-radius')) document.getElementById('prop-radius').addEventListener('change', e => updateProp('borderRadius', e.target.value, true));
    if (document.getElementById('prop-effect')) document.getElementById('prop-effect').addEventListener('change', e => updateProp('effect', e.target.value, false));

    if (document.getElementById('prop-color-picker')) {
      document.getElementById('prop-color-picker').addEventListener('input', e => {
        document.getElementById('prop-color').value = e.target.value;
        el.props.color = e.target.value; renderAll();
      });
      document.getElementById('prop-color-picker').addEventListener('change', pushHistory);
      document.getElementById('prop-color').addEventListener('change', e => {
        document.getElementById('prop-color-picker').value = e.target.value;
        updateProp('color', e.target.value, false);
      });
    }

    if (document.getElementById('prop-anim-in')) document.getElementById('prop-anim-in').addEventListener('change', e => { pushHistory(); el.animIn = e.target.value; renderTimeline(); });
    if (document.getElementById('prop-anim-out')) document.getElementById('prop-anim-out').addEventListener('change', e => { pushHistory(); el.animOut = e.target.value; renderTimeline(); });
  }
"""

    content = content[:start_idx] + new_inspector + content[end_idx:]
    with open('index.html', 'w') as f:
        f.write(content)
