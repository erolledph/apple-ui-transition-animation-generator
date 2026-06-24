with open('index.html', 'r') as f:
    content = f.read()

start = content.find('function updateCanvasTime() {')
end = content.find('function startDrag')
print(content[start:start+1500])
