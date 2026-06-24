with open('index.html', 'r') as f:
    content = f.read()

start = content.find('function renderTimeline() {')
end = content.find('function startBarDrag')
print(content[start:start+2500])
