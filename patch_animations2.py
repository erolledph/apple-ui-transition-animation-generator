import re

with open('index.html', 'r') as f:
    content = f.read()

# We need to inject the new swirl, apple-inspired, and modern trendy transitions into getElementStateAtTime
# Let's find the start of the switch statement in `getElementStateAtTime` for IN and OUT animations

switch_in = """
      switch(anim.type) {
        case 'fade-in': st.opacity = (el.opacity / 100) * eased; break;
"""
switch_in_new = """
      switch(anim.type) {
        case 'fade-in': st.opacity = (el.opacity / 100) * eased; break;
        case 'swirl-in': st.rotation = el.rotation + (360 * intensity) * (1 - eased); st.scale = eased; st.opacity = (el.opacity / 100) * eased; break;
        case 'spiral-zoom': st.rotation = el.rotation - (180 * intensity) * (1 - eased); st.scale = eased * 1.5; st.opacity = (el.opacity / 100) * eased; break;
        case 'app-expand': const s = EASING_FN['spring'] ? EASING_FN['spring'](progress) : eased; st.scale = 0.5 + 0.5 * s; st.y = el.y + 100 * (1-s); st.opacity = (el.opacity / 100) * eased; break;
        case 'glitch-reveal': st.x = el.x + (Math.random() > 0.5 ? 10 : -10) * (1-eased) * intensity; st.opacity = Math.random() > 0.5 ? 1 : 0.5; if (progress === 1) { st.x = el.x; st.opacity = el.opacity/100; } break;
"""
content = content.replace(switch_in, switch_in_new)


switch_out = """
      switch(exit.type) {
        case 'fade-out': st.opacity = (el.opacity / 100) - (el.opacity / 100) * eased; break;
"""
switch_out_new = """
      switch(exit.type) {
        case 'fade-out': st.opacity = (el.opacity / 100) - (el.opacity / 100) * eased; break;
        case 'swirl-out': st.rotation = el.rotation - (360 * intensity) * eased; st.scale = 1 - eased; st.opacity = (el.opacity / 100) - (el.opacity / 100) * eased; break;
        case 'shatter': st.y = el.y + (100 * intensity) * eased; st.rotation = el.rotation + (45 * intensity) * eased; st.opacity = (el.opacity / 100) * (1 - eased); st.filter = `drop-shadow(10px 10px 0px rgba(0,0,0,0.5))`; break;
        case 'genie': st.y = el.y + 200 * eased; st.scale = 1 - 0.8 * eased; st.x = el.x + (cw/2 - el.x) * eased; st.opacity = (el.opacity / 100) * (1 - eased); break;
"""
content = content.replace(switch_out, switch_out_new)

with open('index.html', 'w') as f:
    f.write(content)
