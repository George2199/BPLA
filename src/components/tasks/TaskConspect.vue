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
  } catch (e) {
    error.value = `Ошибка загрузки: ${e.message}`
  } finally {
    isLoading.value = false
  }
})

</script>

<style>
/* Используем глобальные стили для правильного отображения Markdown */
.markdown-container {
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  max-width: 100%;
  overflow-x: auto;
  max-height: 570px; /* Увеличиваем высоту */
  overflow-y: auto; /* Добавляем вертикальный скроллинг */
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
  color: #333;
}

.md-content h1 {
  font-size: 2em;
  margin-top: 0.5em;
  margin-bottom: 0.5em;
  color: #2c3e50;
}

.md-content h2 {
  font-size: 1.5em;
  margin-top: 0.7em;
  margin-bottom: 0.5em;
  color: #2c3e50;
}

.md-content h3 {
  font-size: 1.2em;
  margin-top: 0.8em;
  margin-bottom: 0.5em;
  color: #2c3e50;
}

.md-content p {
  margin-bottom: 1em;
}

.md-content code {
  background-color: #f8f8f8;
  padding: 2px 4px;
  border-radius: 3px;
  font-family: monospace;
  color: #e74c3c;
}

.md-content pre {
  background: #f1f1f1;
  padding: 10px;
  overflow: auto;
  border-radius: 4px;
  margin-bottom: 1em;
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
  width: 8px;
  height: 8px;
}

.markdown-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.markdown-container::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.markdown-container::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>