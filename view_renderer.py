with open('index.html', 'r') as f:
    content = f.read()

start = content.find('function renderCanvas() {')
end = content.find('function updateCanvasTime() {')
print(content[start:start+1500])
