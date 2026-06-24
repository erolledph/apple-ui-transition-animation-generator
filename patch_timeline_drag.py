import re

with open('index.html', 'r') as f:
    content = f.read()

# Fix the timeline drag logic to support the new "full clip" track architecture
old_drag = """        if (mode === 'move') {
          let newDelay = startDelay + dMs;
          newDelay = Math.max(0, Math.min(state.totalDuration - el.animation.duration, newDelay));
          el.animation.delay ="""

new_drag = """        if (mode === 'move') {
          let newDelay = startDelay + dMs;
          newDelay = Math.max(0, newDelay);
          el.animation.delay = newDelay;
          if (el.exit) el.exit.start += dMs; // move exit sync
          """

content = content.replace(old_drag, new_drag)


# Also add playhead scrubbing logic over the timeline ruler
scrub_logic = """
    document.getElementById('timelineRuler').addEventListener('mousedown', e => {
      const updateTime = (ex) => {
        const rect = document.getElementById('timelineContent').getBoundingClientRect();
        const pxPerSec = 100 * state.timelineZoom;
        const x = ex - rect.left - 140; // 140 is header width
        const time = Math.max(0, Math.min(state.totalDuration, (x / pxPerSec) * 1000));
        state.currentTime = time;
        updatePlayhead();
      };
      updateTime(e.clientX);

      const onMove = e => updateTime(e.clientX);
      const onUp = () => { document.removeEventListener('mousemove', onMove); document.removeEventListener('mouseup', onUp); };
      document.addEventListener('mousemove', onMove);
      document.addEventListener('mouseup', onUp);
    });
"""

# inject right before `function startBarDrag`
content = content.replace("function startBarDrag", scrub_logic + "\n  function startBarDrag")

with open('index.html', 'w') as f:
    f.write(content)
