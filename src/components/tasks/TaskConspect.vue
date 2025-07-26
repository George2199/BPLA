<template>
  <div class="markdown-container">
    <div v-if="isLoading" class="loading">Загрузка конспекта...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="md-content" v-html="renderedContent"></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { marked } from 'marked'
import api, { API_BASE_URL } from '@/api'

const props = defineProps({ task: Object })

const isLoading = ref(true)
const error = ref(null)
const renderedContent = ref('')

marked.setOptions({
  gfm: true,
  breaks: true,
  sanitize: false,
  xhtml: true
})

async function fetchFileContent(path) {
  const response = await api.get(path)
  return response.data
}

function prepareMarkdown(md) {
  return md
    .replace(/!\[(.*?)\]\(\/data\/(.*?)\)/g, `![$1](${API_BASE_URL}/data/$2)`)
    .replace(/<img\s+src="\/data\/(.*?)"/g, `<img src="${API_BASE_URL}/data/$1"`)
}

function setupCopyButtons() {
  setTimeout(() => {
    const codeBlocks = document.querySelectorAll('.md-content pre')
    codeBlocks.forEach(block => {
      // Создаем кнопку копирования
      const copyBtn = document.createElement('button')
      copyBtn.className = 'copy-code-btn'
      copyBtn.innerHTML = `
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path>
          <rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect>
        </svg>
      `
      
      // Добавляем обработчик клика
      copyBtn.addEventListener('click', () => {
        const code = block.querySelector('code')?.textContent || ''
        navigator.clipboard.writeText(code).then(() => {
          copyBtn.classList.add('copied')
          setTimeout(() => copyBtn.classList.remove('copied'), 2000)
        })
      })
      
      // Добавляем кнопку в блок кода
      block.style.position = 'relative'
      block.appendChild(copyBtn)
    })
  }, 500)
}

function setupDownloadLinks() {
  setTimeout(() => {
    const links = document.querySelectorAll('.md-content a[download]')
    links.forEach(link => {
      const href = link.getAttribute('href')
      if (href?.startsWith('/data/')) {
        const fullUrl = `${API_BASE_URL}/download${href}`
        link.addEventListener('click', e => {
          e.preventDefault()
          const a = document.createElement('a')
          a.href = fullUrl
          a.download = link.getAttribute('download') || ''
          a.style.display = 'none'
          document.body.appendChild(a)
          a.click()
          document.body.removeChild(a)
        })
      }
    })
  }, 500)
}

onMounted(async () => {
  const path = props.task?.conspect_path
  if (!path) {
    error.value = 'Конспект не найден'
    isLoading.value = false
    return
  }

  try {
    const raw = await fetchFileContent(path)
    const markdown = prepareMarkdown(String(raw || ''))
    renderedContent.value = marked.parse(markdown)
    setupDownloadLinks()
    setupCopyButtons()
  } catch (e) {
    error.value = `Ошибка загрузки: ${e.message}`
  } finally {
    isLoading.value = false
  }
})

</script>

<style>

.copy-code-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  padding: 4px 6px;
  cursor: pointer;
  opacity: 0;
  transition: all 0.2s ease;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
}

.copy-code-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.md-content pre:hover .copy-code-btn {
  opacity: 1;
}

.copy-code-btn.copied {
  background: rgba(255, 255, 255, 0.2);
  opacity: 1;
}

.copy-code-btn.copied::after {
  content: 'Скопировано!';
  position: absolute;
  right: 40px;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 12px;
  white-space: nowrap;
}

.copy-tooltip {
  position: absolute;
  right: 100%;
  white-space: nowrap;
  background: #4CAF50;
  color: white;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  opacity: 0;
  transform: translateX(10px);
  transition: all 0.2s ease;
  pointer-events: none;
}

.copy-code-btn.copied .copy-tooltip {
  opacity: 1;
  transform: translateX(0);
}

/* Используем глобальные стили для правильного отображения Markdown */
.markdown-container {
  background: transparent;
  border: 2px solid #CDBDF5;
  border-radius: 30px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  max-width: 100%;
  overflow-x: auto;
  max-height: 620px; /* Увеличиваем высоту */
  overflow-y: auto; /* Добавляем вертикальный скроллинг */
  padding: 20px; /* общий отступ */
  padding-right: 8px; /* дополнительный отступ справа для скроллбара */
  scrollbar-gutter: stable; /* резервируем место под скроллбар */
}

.loading {
  text-align: center;
  padding: 20px;
  color: #666;
}

.error {
  color: #e74c3c;
  padding: 20px;
  border: 1px solid #e74c3c;
  border-radius: 4px;
  background-color: #fdf1f0;
}

.md-content {
  line-height: 1.6;
  color: #ffffff;
}

.md-content h1 {
  font-size: 2em;
  margin-top: 0.5em;
  margin-bottom: 0.5em;
  color: #ffffff;
}

.md-content h2 {
  font-size: 1.5em;
  margin-top: 0.7em;
  margin-bottom: 0.5em;
  color: #ffffff;
}

.md-content h3 {
  font-size: 1.2em;
  margin-top: 0.8em;
  margin-bottom: 0.5em;
  color: #ffffff;
}

.md-content p {
  margin-bottom: 1em;
}

.md-content code {
  background-color: #f8f8f8;
  padding: 2px 4px;
  border-radius: 3px;
  font-family: monospace;
  color: #0c0816;
}

.md-content pre {
  background: #231641 ;
  padding: 10px;
  overflow: auto;
  border-radius: 4px;
  margin-bottom: 1em;
    user-select: text;
}

.md-content ul {
  margin-left: 20px;
  padding-left: 0;
  list-style-type: disc;
  margin-bottom: 1em;
}

.md-content li {
  margin-bottom: 6px;
  display: list-item;
}

.md-content ol {
  margin-left: 20px;
  margin-bottom: 1em;
  list-style-type: decimal;
}

.md-content a {
  color: #3498db;
  text-decoration: none;
}

.md-content a:hover {
  text-decoration: underline;
}

.md-content img, .md-image {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 1em auto;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.md-content blockquote {
  border-left: 4px solid #ccc;
  padding-left: 15px;
  margin-left: 0;
  color: #666;
  margin-bottom: 1em;
}

/* Добавим стиль полосы прокрутки для лучшего UX */
.markdown-container::-webkit-scrollbar {
  width: 10px;
  height: 8px;

}

.markdown-container::-webkit-scrollbar-track {
  background: transparent;
  margin: 35px 0;/* отступы сверху и снизу */
  margin-right: 30px;
  border-radius: 4px;
}

.markdown-container::-webkit-scrollbar-thumb {
  background: #d6cbf381;
  border-radius: 4px;
  background-clip: content-box; /* ограничивает фон только области "бегунка" */
}

</style>