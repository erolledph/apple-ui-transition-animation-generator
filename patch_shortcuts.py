import re

with open('index.html', 'r') as f:
    content = f.read()

# Add missing shortcuts: Ctrl+D (duplicate), [ / ] (move clip left/right by 1 frame), Ctrl+A (Select all)
# Update keydown logic

old_keydown = """      else if ((e.metaKey || e.ctrlKey) && e.shiftKey && e.code === 'KeyD') { e.preventDefault(); splitElement(); }
      else if (e.code === 'Space') { e.preventDefault(); togglePlay(); }
      else if (e.code === 'KeyR') { restart(); }
      else if (e.code === 'KeyG') { document.getElementById('gridBtn').click(); }
      else if (e.code === 'Delete' || e.code === 'Backspace') { if (state.selectedId) { e.preventDefault(); deleteElement(state.selectedId); } }
      else if (e.code === 'ArrowLeft') { e.preventDefault(); stepTime(-1); }
      else if (e.code === 'ArrowRight') { e.preventDefault(); stepTime(1); }"""

new_keydown = """      else if ((e.metaKey || e.ctrlKey) && e.shiftKey && e.code === 'KeyD') { e.preventDefault(); splitElement(); }
      else if ((e.metaKey || e.ctrlKey) && !e.shiftKey && e.code === 'KeyD') {
          e.preventDefault();
          if (state.selectedId) {
              const el = state.elements.find(x => x.id === state.selectedId);
              if (el) {
                  pushHistory();
                  const dup = JSON.parse(JSON.stringify(el));
                  dup.id = 'el_' + Date.now();
                  dup.props.x += 20; dup.props.y += 20;
                  state.elements.push(dup);
                  state.selectedId = dup.id;
                  renderAll();
              }
          }
      }
      else if ((e.metaKey || e.ctrlKey) && e.code === 'KeyA') { e.preventDefault(); state.multiSelectIds = state.elements.map(x=>x.id); renderAll(); }
      else if ((e.metaKey || e.ctrlKey) && e.code === 'KeyY') { e.preventDefault(); redo(); }
      else if (e.code === 'Space') { e.preventDefault(); togglePlay(); }
      else if (e.code === 'KeyR') { restart(); }
      else if (e.code === 'KeyG') { document.getElementById('gridBtn').click(); }
      else if (e.code === 'Delete' || e.code === 'Backspace') {
          if (state.selectedId || state.multiSelectIds.length > 0) {
              e.preventDefault(); pushHistory();
              if (state.selectedId) { state.elements = state.elements.filter(x => x.id !== state.selectedId); state.selectedId = null; }
              if (state.multiSelectIds.length > 0) { state.elements = state.elements.filter(x => !state.multiSelectIds.includes(x.id)); state.multiSelectIds = []; }
              renderAll();
          }
      }
      else if (e.code === 'BracketLeft') {
          e.preventDefault();
          if (state.selectedId) {
              const el = state.elements.find(x => x.id === state.selectedId);
              if (el) { pushHistory(); el.animation.delay = Math.max(0, el.animation.delay - 33); renderTimeline(); }
          }
      }
      else if (e.code === 'BracketRight') {
          e.preventDefault();
          if (state.selectedId) {
              const el = state.elements.find(x => x.id === state.selectedId);
              if (el) { pushHistory(); el.animation.delay += 33; renderTimeline(); }
          }
      }
      else if (e.key === '?') { e.preventDefault(); document.getElementById('shortcutsBtn').click(); }
      else if (e.code === 'ArrowLeft') { e.preventDefault(); stepTime(-1); }
      else if (e.code === 'ArrowRight') { e.preventDefault(); stepTime(1); }"""

content = content.replace(old_keydown, new_keydown)

# Optimize RAF by ensuring play loop uses native rAF (which it appears to already based on `function loop(ts)`)
# We will just verify it's correctly written

with open('index.html', 'w') as f:
    f.write(content)
