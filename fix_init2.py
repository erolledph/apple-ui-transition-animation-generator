import re

with open('index.html', 'r') as f:
    content = f.read()

# Make sure the drop logic actually creates standard elements
# Need to patch addElement to support image and video if not already present
patch = """
    } else if (type === 'image') {
      props = { x: opts.x||0, y: opts.y||0, width: opts.width||200, height: opts.height||200, url: opts.url, opacity: 1, rotation: 0, scale: 1, borderRadius: 0 };
    } else if (type === 'video') {
      props = { x: opts.x||0, y: opts.y||0, width: opts.width||320, height: opts.height||180, url: opts.url, opacity: 1, rotation: 0, scale: 1, borderRadius: 0 };
    }
"""
content = content.replace("} else if (type === 'circle') {", patch.strip() + "\n    } else if (type === 'circle') {")

with open('index.html', 'w') as f:
    f.write(content)
