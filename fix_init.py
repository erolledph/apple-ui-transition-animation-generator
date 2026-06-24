import re

with open('index.html', 'r') as f:
    content = f.read()

# Fix the placement of init calls
content = content.replace('''      if (loadDemo)
    initMediaLibrary();
    setupCanvasDrop();
loadDemoScene('default');''', '''      if (loadDemo) loadDemoScene('default');''')

# Put it correctly right after renderChapters();
target = "renderChapters();"
content = content.replace(target, target + "\n    initMediaLibrary();\n    setupCanvasDrop();\n")

with open('index.html', 'w') as f:
    f.write(content)
