import re

with open('index.html', 'r') as f:
    content = f.read()

# Add state for media library
state_add = """
    mediaLibrary: [], // Array of {id, type, url, file, name}
"""
content = content.replace('chapters: [],', 'chapters: [],\n' + state_add)

# Add Media Library JS functions
media_js = """
  // ===== MEDIA LIBRARY =====
  function initMediaLibrary() {
    document.querySelectorAll('.sidebar-tab').forEach(tab => {
      tab.addEventListener('click', (e) => {
        document.querySelectorAll('.sidebar-tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.sidebar-pane').forEach(p => p.classList.remove('active'));
        e.target.classList.add('active');
        document.getElementById('pane-' + e.target.dataset.tab).classList.add('active');
      });
    });

    const uploadArea = document.getElementById('mediaUploadArea');
    const fileInput = document.getElementById('mediaFileInput');

    uploadArea.addEventListener('click', () => fileInput.click());
    uploadArea.addEventListener('dragover', e => { e.preventDefault(); uploadArea.classList.add('drag-over'); });
    uploadArea.addEventListener('dragleave', () => uploadArea.classList.remove('drag-over'));
    uploadArea.addEventListener('drop', e => {
      e.preventDefault();
      uploadArea.classList.remove('drag-over');
      handleMediaFiles(e.dataTransfer.files);
    });

    fileInput.addEventListener('change', e => {
      handleMediaFiles(e.target.files);
      fileInput.value = ''; // Reset
    });
  }

  function handleMediaFiles(files) {
    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      let type = '';
      if (file.type.startsWith('image/')) type = 'image';
      else if (file.type.startsWith('video/')) type = 'video';
      else if (file.type.startsWith('audio/')) type = 'audio';
      else continue;

      const url = URL.createObjectURL(file);
      const mediaItem = { id: 'media_' + Date.now() + '_' + i, type, url, file, name: file.name };
      state.mediaLibrary.push(mediaItem);
    }
    renderMediaLibrary();
  }

  function renderMediaLibrary() {
    const grid = document.getElementById('mediaGrid');
    grid.innerHTML = '';
    state.mediaLibrary.forEach(media => {
      const el = document.createElement('div');
      el.className = 'media-item';
      el.draggable = true;
      el.dataset.mediaId = media.id;

      if (media.type === 'image') {
        el.innerHTML = `<img src="${media.url}" alt="${media.name}"><div class="media-type">IMG</div>`;
      } else if (media.type === 'video') {
        el.innerHTML = `<video src="${media.url}" muted></video><div class="media-type">VID</div>`;
        el.addEventListener('mouseenter', () => el.querySelector('video').play().catch(()=>{}));
        el.addEventListener('mouseleave', () => { el.querySelector('video').pause(); el.querySelector('video').currentTime = 0; });
      } else if (media.type === 'audio') {
        el.innerHTML = `<div style="text-align:center;color:var(--accent);"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18V5l12-2v13"></path><circle cx="6" cy="18" r="3"></circle><circle cx="18" cy="16" r="3"></circle></svg></div><div class="media-type">AUD</div>`;
      }

      el.innerHTML += `<div class="media-name">${media.name}</div>`;

      el.addEventListener('dragstart', e => {
        e.dataTransfer.setData('application/json', JSON.stringify({ source: 'mediaLibrary', mediaId: media.id }));
      });

      grid.appendChild(el);
    });
  }

  // Canvas drop handling for media
  function setupCanvasDrop() {
    const canvasStage = document.getElementById('canvasStage');
    canvasStage.addEventListener('dragover', e => e.preventDefault());
    canvasStage.addEventListener('drop', e => {
      e.preventDefault();
      try {
        const data = JSON.parse(e.dataTransfer.getData('application/json'));
        if (data.source === 'mediaLibrary') {
          const media = state.mediaLibrary.find(m => m.id === data.mediaId);
          if (media) {
            pushHistory();
            const rect = canvasStage.getBoundingClientRect();
            const x = (e.clientX - rect.left) / state.zoom;
            const y = (e.clientY - rect.top) / state.zoom;

            if (media.type === 'image') {
                addElement('image', { x, y, url: media.url, width: 200, height: 200 });
            } else if (media.type === 'video') {
                addElement('video', { x, y, url: media.url, width: 320, height: 180 });
            } else if (media.type === 'audio') {
                state.audio = { src: media.url, name: media.name };
                renderAudio();
            }
          }
        }
      } catch (err) {}
    });
  }

"""

# Inject after 'function init()'
init_idx = content.find('function init() {')

# Find a good spot before init to put the functions
funcs_inject_point = content.rfind('\n', 0, init_idx)
content = content[:funcs_inject_point] + media_js + content[funcs_inject_point:]

# Inject init calls inside init()
init_body_idx = content.find('  init();', init_idx)
# We need to inject inside the function body
inject_calls = """
    initMediaLibrary();
    setupCanvasDrop();
"""
# Find a place inside init
load_demo_idx = content.find('loadDemoScene(\'default\');')
content = content[:load_demo_idx] + inject_calls + content[load_demo_idx:]

with open('index.html', 'w') as f:
    f.write(content)
