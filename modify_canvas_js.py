import re

with open('index.html', 'r') as f:
    content = f.read()

# Replace initEditorCanvas to draw rulers
old_init = """  function initEditorCanvas() {
    applyCanvasSize();
    applyZoom();
    applySceneBackground();
  }"""

new_init = """  function initEditorCanvas() {
    applyCanvasSize();
    applyZoom();
    applySceneBackground();
    renderRulers();
  }

  function renderRulers() {
    const wrap = document.getElementById('canvasWrap');
    const rH = document.getElementById('rulerH');
    const rV = document.getElementById('rulerV');

    // We only redraw if needed, simplified ruler drawing
    rH.innerHTML = '';
    rV.innerHTML = '';

    const w = wrap.clientWidth - 20;
    const h = wrap.clientHeight - 20;
    const step = 50; // 50px physical screen pixels

    for (let x = 0; x < w; x += step) {
        let val = Math.round((x - w/2) / state.zoom); // Center relative
        rH.innerHTML += `<div class="ruler-tick ruler-tick-h" style="left:${x+20}px"></div>`;
        rH.innerHTML += `<div class="ruler-label ruler-label-h" style="left:${x+20}px">${val}</div>`;
    }

    for (let y = 0; y < h; y += step) {
        let val = Math.round((y - h/2) / state.zoom); // Center relative
        rV.innerHTML += `<div class="ruler-tick ruler-tick-v" style="top:${y+20}px"></div>`;
        rV.innerHTML += `<div class="ruler-label ruler-label-v" style="top:${y+20}px">${val}</div>`;
    }
  }
"""

content = content.replace(old_init, new_init)

# Hook up scroll/resize to rulers
content = content.replace("document.getElementById('canvasWrap').addEventListener('scroll', () => {", "document.getElementById('canvasWrap').addEventListener('scroll', () => {\n      renderRulers();")


# Handle Safe Zone Toggle
safe_zone_toggle = """
    document.getElementById('safeZoneBtn').addEventListener('click', (e) => {
      e.currentTarget.classList.toggle('active');
      document.getElementById('canvasSafeZone').classList.toggle('visible');
    });
"""
content = content.replace("document.getElementById('gridBtn').addEventListener('click', (e) => {", safe_zone_toggle + "\n    document.getElementById('gridBtn').addEventListener('click', (e) => {")


# Marquee Selection Logic within init()
marquee_logic = """
    const marquee = document.getElementById('marquee');
    let isMarquee = false;
    let startX, startY;

    document.getElementById('canvasWrap').addEventListener('mousedown', e => {
      if (e.target.id === 'canvasWrap' || e.target.id === 'canvasStage' || e.target.classList.contains('canvas-bg')) {
        isMarquee = true;
        const rect = document.getElementById('canvasWrap').getBoundingClientRect();
        startX = e.clientX - rect.left;
        startY = e.clientY - rect.top;
        marquee.style.left = startX + 'px';
        marquee.style.top = startY + 'px';
        marquee.style.width = '0px';
        marquee.style.height = '0px';
        marquee.style.display = 'block';
        if (!e.shiftKey) { state.multiSelectIds = []; state.selectedId = null; renderAll(); }
      }
    });

    document.addEventListener('mousemove', e => {
      if (isMarquee) {
        const rect = document.getElementById('canvasWrap').getBoundingClientRect();
        const curX = e.clientX - rect.left;
        const curY = e.clientY - rect.top;

        const x = Math.min(startX, curX);
        const y = Math.min(startY, curY);
        const w = Math.abs(curX - startX);
        const h = Math.abs(curY - startY);

        marquee.style.left = x + 'px';
        marquee.style.top = y + 'px';
        marquee.style.width = w + 'px';
        marquee.style.height = h + 'px';

        // Select elements
        const stageRect = document.getElementById('canvasStage').getBoundingClientRect();
        const rx = (x - (stageRect.left - rect.left)) / state.zoom;
        const ry = (y - (stageRect.top - rect.top)) / state.zoom;
        const rw = w / state.zoom;
        const rh = h / state.zoom;

        state.multiSelectIds = state.elements.filter(el => {
            return (el.props.x < rx + rw && el.props.x + el.props.width > rx &&
                    el.props.y < ry + rh && el.props.y + el.props.height > ry);
        }).map(el => el.id);

        renderCanvas();
      }
    });

    document.addEventListener('mouseup', () => {
      if (isMarquee) {
        isMarquee = false;
        marquee.style.display = 'none';
        if (state.multiSelectIds.length > 0) {
            state.selectedId = null; // Use multi-select
            document.getElementById('alignToolbar').classList.add('visible');
        } else {
            document.getElementById('alignToolbar').classList.remove('visible');
        }
        renderAll();
      }
    });

    // Alignment logic
    document.querySelectorAll('.align-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            if (state.multiSelectIds.length < 2) return;
            pushHistory();
            const els = state.multiSelectIds.map(id => state.elements.find(e => e.id === id)).filter(Boolean);
            const mode = btn.dataset.align;

            if (mode === 'left') {
                const minX = Math.min(...els.map(e => e.props.x));
                els.forEach(e => e.props.x = minX);
            } else if (mode === 'right') {
                const maxX = Math.max(...els.map(e => e.props.x + e.props.width));
                els.forEach(e => e.props.x = maxX - e.props.width);
            } else if (mode === 'center') {
                const midX = (Math.min(...els.map(e => e.props.x)) + Math.max(...els.map(e => e.props.x + e.props.width))) / 2;
                els.forEach(e => e.props.x = midX - e.props.width / 2);
            } else if (mode === 'top') {
                const minY = Math.min(...els.map(e => e.props.y));
                els.forEach(e => e.props.y = minY);
            } else if (mode === 'bottom') {
                const maxY = Math.max(...els.map(e => e.props.y + e.props.height));
                els.forEach(e => e.props.y = maxY - e.props.height);
            } else if (mode === 'middle') {
                const midY = (Math.min(...els.map(e => e.props.y)) + Math.max(...els.map(e => e.props.y + e.props.height))) / 2;
                els.forEach(e => e.props.y = midY - e.props.height / 2);
            }
            renderAll();
        });
    });
"""

content = content.replace("document.getElementById('canvasStage').addEventListener('mousedown', (e) => {", marquee_logic + "\n    document.getElementById('canvasStage').addEventListener('mousedown', (e) => {")


# Hide align tools when not multi-selected
hide_align = """
      if (state.multiSelectIds.length < 2) document.getElementById('alignToolbar').classList.remove('visible');
"""
content = content.replace("renderLayers();", "renderLayers();\n" + hide_align)


with open('index.html', 'w') as f:
    f.write(content)
