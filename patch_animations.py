import re

with open('index.html', 'r') as f:
    content = f.read()

# It looks like the codebase has `getElementStateAtTime` which controls the animations based on the current time and keyframes/transitions.
# Let's inspect `getElementStateAtTime`.

start = content.find('function getElementStateAtTime')
end = content.find('function applySceneBackground()')

print(content[start:start+1500])
