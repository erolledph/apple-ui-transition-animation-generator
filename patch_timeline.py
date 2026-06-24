import re

with open('index.html', 'r') as f:
    content = f.read()

# Make the timeline tracks color-coded and organized by elements better, adding thumbnails where applicable
old_html = """        const left = 140 + (anim.delay / 1000) * pxPerSec;
        const width = Math.max(24, (anim.duration / 1000) * pxPerSec);
        const color = TYPE_COLORS[el.type];"""

new_html = """        const left = 140 + (anim.delay / 1000) * pxPerSec;
        const totalW = Math.max(24, ((exit ? exit.start + exit.duration : state.totalDuration) - anim.delay) / 1000 * pxPerSec);
        const color = el.type === 'video' ? '#0a84ff' : el.type === 'audio' ? '#30d158' : el.type === 'image' ? '#bf5af2' : el.type === 'text' ? '#ff9f0a' : '#ff453a';
"""
content = content.replace(old_html, new_html)

# We want the clip to show the duration of the entire element, not just the "anim.duration" which is the in-transition
# Currently it renders tracksHtml += `<div class="tl-track ...
old_track = """        tracksHtml += `
          <div class="tl-track ${state.selectedId === el.id ? 'active' : ''}" data-id="${el.id}">
            <div class="tl-track-header">
              <div class="tl-track-icon">${iconHTML}</div>
              <span class="tl-track-name">${el.name}</span>
            </div>
            <div class="tl-bar-wrap" style="left: ${left}px; width: calc(100% - ${left}px);">
              <div class="tl-bar" data-id="${el.id}" data-mode="delay" style="width: ${width}px; background: rgba(${color.replace('#','')}, 0.2); border: 1px solid rgba(255,255,255,0.2);">
                <div class="tl-handle left" data-mode="delay"></div>
                <span style="font-size: 10px; color: var(--text); padding-left: 6px; font-weight: 500;">${presetName}</span>
                <div class="tl-handle right" data-mode="duration"></div>
              </div>"""

# Replace it to be a real track clip representing full lifespan
new_track = """        tracksHtml += `
          <div class="tl-track ${state.selectedId === el.id ? 'active' : ''} ${state.multiSelectIds.includes(el.id) ? 'multi-selected' : ''}" data-id="${el.id}">
            <div class="tl-track-header">
              <div class="tl-track-icon">${iconHTML}</div>
              <span class="tl-track-name">${el.name}</span>
            </div>
            <div class="tl-bar-wrap" style="left: ${left}px; width: ${totalW}px;">
              <div class="tl-bar full-clip" data-id="${el.id}" style="width: 100%; background: ${color}; border: 1px solid rgba(255,255,255,0.2); border-radius: 6px; opacity: 0.8;">
                <div class="tl-handle left" data-mode="delay" style="background: rgba(255,255,255,0.8); width: 8px;"></div>
                <div style="position: absolute; left: 0; top: 0; height: 100%; width: ${(anim.duration/1000)*pxPerSec}px; background: rgba(0,0,0,0.3); border-radius: 6px 0 0 6px;"></div>
                <span style="font-size: 10px; color: #fff; padding-left: 10px; font-weight: 500; position: absolute; z-index: 2; line-height: 28px;">${el.name}</span>
                ${exit ? `<div style="position: absolute; right: 0; top: 0; height: 100%; width: ${(exit.duration/1000)*pxPerSec}px; background: rgba(0,0,0,0.3); border-radius: 0 6px 6px 0;"></div>` : ''}
                <div class="tl-handle right" data-mode="duration" style="background: rgba(255,255,255,0.8); width: 8px;"></div>
              </div>"""

content = content.replace(old_track, new_track)

with open('index.html', 'w') as f:
    f.write(content)
