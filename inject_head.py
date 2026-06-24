import re

with open('index.html', 'r') as f:
    content = f.read()

fonts_url = "https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Cormorant+Garamond:wght@400;700&family=DM+Sans:opsz,wght@9..40,400;700&family=DM+Serif+Display&family=Figtree:wght@400;700&family=Fira+Code:wght@400;700&family=Fraunces:opsz,wght@9..144,400;700&family=IBM+Plex+Mono:wght@400;700&family=Inter:wght@100..900&family=JetBrains+Mono:wght@400;700&family=Lora:ital,wght@0,400;0,700;1,400&family=Manrope:wght@400;700&family=Merriweather:wght@400;700&family=Montserrat:wght@100..900&family=Nunito:wght@400;700&family=Onest:wght@400;700&family=Outfit:wght@400;700&family=Playfair+Display:wght@400;700&family=Plus+Jakarta+Sans:wght@400;700&family=Poppins:wght@100..900&family=Raleway:wght@100..900&family=Righteous&family=Sora:wght@400;700&family=Space+Mono:wght@400;700&family=Urbanist:wght@400;700&display=swap"

head_additions = f"""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{fonts_url}" rel="stylesheet">
<!-- Fonts not on Google Fonts (Clash Display, Cabinet Grotesk, Satoshi, General Sans, Geist) loaded via fontshare/other CDNs -->
<link href="https://api.fontshare.com/v2/css?f[]=clash-display@400,700&f[]=cabinet-grotesk@400,700&f[]=satoshi@400,700&f[]=general-sans@400,700&display=swap" rel="stylesheet">
<link href="https://cdn.jsdelivr.net/npm/geist@1.0.0/dist/fonts/geist-sans/style.css" rel="stylesheet">

<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gif.js/0.2.0/gif.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
"""

content = content.replace('<title>Transition Studio Pro — Motion & Video Editor</title>', '<title>Transition Studio Pro — Motion & Video Editor</title>' + head_additions)

with open('index.html', 'w') as f:
    f.write(content)
