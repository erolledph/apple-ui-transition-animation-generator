with open('index.html', 'r') as f:
    content = f.read()

start = content.find('async function startVideoExport() {')
end = content.find('function startGifExport() {')
print(content[start:start+1500])
