import re

with open('index.html', 'r') as f:
    content = f.read()

# Add an elastic tension spring mathematical easing for more authentic apple feel
easing = """
    'bounce': bezierSolver(0.68, -0.6, 0.32, 1.6)
  };
"""

new_easing = """
    'bounce': bezierSolver(0.68, -0.6, 0.32, 1.6),
    'elastic': t => {
        const c4 = (2 * Math.PI) / 3;
        return t === 0 ? 0 : t === 1 ? 1 : Math.pow(2, -10 * t) * Math.sin((t * 10 - 0.75) * c4) + 1;
    }
  };
"""

content = content.replace(easing, new_easing)

with open('index.html', 'w') as f:
    f.write(content)
