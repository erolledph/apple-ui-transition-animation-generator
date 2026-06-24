with open('index.html', 'r') as f:
    content = f.read()

start = content.find('const EASING_FN')
end = content.find('function bezierSolver')
print(content[start:start+1000])
