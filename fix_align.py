import re

with open('index.html', 'r') as f:
    content = f.read()

# Make sure canvas element drag clears multi-select
# Update startDrag function
old_drag = """      if (e.button !== 0) return;
      pushHistory();
      if (!state.multiSelectIds.includes(el.id)) {
        state.selectedId = el.id;
        state.multiSelectIds = [];
        renderAll();
      }"""

new_drag = """      if (e.button !== 0) return;
      pushHistory();
      if (!state.multiSelectIds.includes(el.id)) {
        if (!e.shiftKey) {
            state.selectedId = el.id;
            state.multiSelectIds = [];
        } else {
            state.multiSelectIds.push(el.id);
            state.selectedId = null;
        }
        renderAll();
      }"""

content = content.replace(old_drag, new_drag)


with open('index.html', 'w') as f:
    f.write(content)
