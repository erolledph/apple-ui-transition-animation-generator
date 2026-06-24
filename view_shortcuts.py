with open('index.html', 'r') as f:
    content = f.read()

start = content.find("document.addEventListener('keydown', (e) => {")
end = content.find("document.getElementById('totalTime')", start)
print(content[start:start+1500])
