with open('index.html', 'r') as f:
    content = f.read()

start = content.find('function startBarDrag(e, elId, mode, animMode)')
end = content.find('function updatePlayhead()')
print(content[start:start+1500])
