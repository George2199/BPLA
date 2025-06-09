<template>
  <div class="markdown-container">
    <div v-if="isLoading" class="loading">
      Загрузка конспекта...
    </div>
    <div v-else-if="error" class="error">
      {{ error }}
    </div>
    <div v-else class="md-content" v-html="renderedContent"></div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { marked } from 'marked'
import api, { API_BASE_URL } from '@/api'

const props = defineProps({
  task: Object
})

const isLoading = ref(true)
const error = ref(null)
const mdContent = ref('')
const renderedContent = ref('')

// Получаем базовый URL API
const apiBaseUrl = API_BASE_URL
console.log('API URL:', apiBaseUrl);

// Настраиваем marked для поддержки HTML
marked.setOptions({
  gfm: true,
  breaks: true,
  headerIds: true,
  sanitize: false, // Позволяет использовать HTML
  smartLists: true,
  xhtml: true // Строгий XHTML
});

// Функция для загрузки содержимого файла по URL
async function fetchFileContent(url) {
  try {
    console.log(`Загрузка файла с URL: ${apiBaseUrl}${url}`);
    const response = await api.get(`${url}`);
    console.log('Файл успешно загружен');
    return response.data;
  } catch (err) {
    console.error(`Ошибка загрузки файла по URL ${apiBaseUrl}${url}:`, err);
    throw new Error(`Не удалось загрузить файл ${url}: ${err.message}`);
  }
}

// Функция для активации скриптов в HTML
function activateScripts() {
  setTimeout(() => {
    const scripts = document.querySelectorAll('.md-content script');
    console.log('Найдено скриптов в контенте:', scripts.length);
    
    scripts.forEach((oldScript) => {
      const newScript = document.createElement('script');
      
      // Копируем атрибуты из старого скрипта в новый
      Array.from(oldScript.attributes).forEach(attr => {
        newScript.setAttribute(attr.name, attr.value);
      });
      
      // Копируем содержимое скрипта
      newScript.innerHTML = oldScript.innerHTML;
      
      // Заменяем старый скрипт новым (это заставит его выполниться)
      oldScript.parentNode.replaceChild(newScript, oldScript);
    });
  }, 500);
}

// Добавляем глобальную функцию для скачивания любого контента
window.downloadAnyContent = function(url, filename) {
  try {
    console.log(`Скачивание контента: ${url}, имя файла: ${filename}`);
    
    const fullUrl = url.startsWith('http') ? url : `${apiBaseUrl}${url}`;
    
    // Используем fetch для получения контента как blob
    fetch(fullUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP ошибка! статус: ${response.status}`);
        }
        return response.blob();
      })
      .then(blob => {
        // Создаем объект URL из blob
        const blobUrl = window.URL.createObjectURL(blob);
        
        // Создаем временную ссылку для скачивания
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = blobUrl;
        a.download = filename || 'download'; // Используем имя файла или 'download' по умолчанию
        
        // Добавляем ссылку в DOM, кликаем и удаляем
        document.body.appendChild(a);
        a.click();
        
        // Очищаем ресурсы
        setTimeout(() => {
          window.URL.revokeObjectURL(blobUrl);
          document.body.removeChild(a);
        }, 100);
        
        console.log('Скачивание инициировано успешно');
      })
      .catch(error => {
        console.error('Ошибка при скачивании:', error);
        alert(`Не удалось скачать файл: ${error.message}`);
      });
  } catch (e) {
    console.error('Общая ошибка в функции скачивания:', e);
    alert(`Произошла ошибка: ${e.message}`);
  }
};

// Обработка клика по ссылкам с атрибутом download
function setupDownloadLinks() {
  setTimeout(() => {
    const links = document.querySelectorAll('.md-content a[download]');
    console.log('Найдено ссылок для скачивания:', links.length);
    
    links.forEach((link) => {
      const originalHref = link.getAttribute('href');
      // Преобразуем относительные пути в абсолютные
      if (originalHref && originalHref.startsWith('/data/')) {
        const fullUrl = `${apiBaseUrl}${originalHref}`;
        
        // Меняем обработчик клика для гарантированного скачивания
        link.addEventListener('click', (e) => {
          e.preventDefault();
          console.log(`Скачивание файла: ${fullUrl}`);
          
          // Создаем невидимый iframe для скачивания
          const iframe = document.createElement('iframe');
          iframe.style.display = 'none';
          iframe.src = fullUrl;
          document.body.appendChild(iframe);
          
          // Удаляем iframe после начала загрузки
          setTimeout(() => {
            document.body.removeChild(iframe);
          }, 2000);
          
          // Также открываем в новой вкладке для надежности
          window.open(fullUrl, '_blank');
        });
      }
    });
  }, 1000);
}

// Использовать стандартный синтаксис marked без кастомного рендерера
onMounted(async () => {
  try {
    console.log('TaskConspect mounted, task:', props.task);
    
    if (!props.task?.content) {
      error.value = 'Не указан контент конспекта';
      console.error('Ошибка: Не указан контент конспекта', props.task);
      isLoading.value = false;
      return;
    }

    console.log('Тип контента:', typeof props.task.content);

    // Определяем, откуда брать контент
    if (typeof props.task.content === 'object' && props.task.content.text) {
      // Если контент - объект с полем text
      mdContent.value = props.task.content.text;
      console.log('Используем текст из объекта');
    } else if (typeof props.task.content === 'string') {
      // Если контент - строка URL, загружаем содержимое файла
      const contentPath = props.task.content;
      console.log('Путь к контенту:', contentPath);
      
      if (contentPath.startsWith('/data/')) {
        try {
          const fileContent = await fetchFileContent(contentPath);
          mdContent.value = fileContent;
          console.log('Загружен файл, первые 100 символов:', 
            typeof fileContent === 'string' ? fileContent.substring(0, 100) + '...' : 'Не строка');
        } catch (err) {
          console.error('Ошибка при загрузке файла:', err);
          error.value = `Ошибка загрузки файла: ${err.message}`;
          isLoading.value = false;
          return;
        }
      } else {
        // Если это просто текст, используем его напрямую
        mdContent.value = props.task.content;
        console.log('Используем текст напрямую');
      }
    } else {
      error.value = 'Неверный формат контента конспекта';
      console.error('Ошибка: Неверный формат контента конспекта', props.task.content);
      isLoading.value = false;
      return;
    }
    
    try {
      // Проверяем, что mdContent - строка
      if (typeof mdContent.value !== 'string') {
        console.warn('mdContent не является строкой:', mdContent.value);
        mdContent.value = String(mdContent.value || '');
      }
      
      // Заменяем пути к изображениям в Markdown перед рендерингом
      console.log('Обработка путей изображений');
      const processedContent = mdContent.value.replace(/!\[(.*?)\]\(\/data\/(.*?)\)/g, 
        (match, alt, path) => `![${alt}](${apiBaseUrl}/data/${path})`);
      
      // Также заменяем HTML-синтаксис для изображений
      const finalContent = processedContent.replace(
        /<img\s+src="\/data\/(.*?)"/g, 
        `<img src="${apiBaseUrl}/data/$1"`
      );
      
      console.log('Обработанный контент (начало):', finalContent.substring(0, 150));
      
      // Используем библиотеку marked для рендеринга Markdown
      console.log('Начинаем рендеринг Markdown');
      renderedContent.value = marked.parse(finalContent);
      console.log('Рендеринг успешно завершен');
      
      // Активируем скрипты в HTML
      activateScripts();
      
      // Настраиваем обработчики для скачивания файлов
      setupDownloadLinks();
      
      // Добавляем обработчик событий для контроля загрузки изображений
      setTimeout(() => {
        const images = document.querySelectorAll('.md-content img');
        console.log('Найдено изображений:', images.length);
        
        images.forEach((img, index) => {
          console.log(`Изображение ${index + 1}:`, img.src);
          
          img.onerror = function() {
            console.error(`Ошибка загрузки изображения: ${img.src}`);
            img.style.border = '2px solid red';
            img.style.padding = '5px';
            img.title = 'Ошибка загрузки';
          };
          
          img.onload = function() {
            console.log(`Изображение успешно загружено: ${img.src}`);
          };
        });
      }, 500);
      
      if (renderedContent.value) {
        console.log('Результат рендеринга (первые 100 символов):', 
          renderedContent.value.substring(0, 100) + '...');
      } else {
        console.warn('Результат рендеринга пустой');
      }
    } catch (renderErr) {
      console.error('Ошибка рендеринга Markdown:', renderErr);
      error.value = `Ошибка рендеринга Markdown: ${renderErr.message}`;
      isLoading.value = false;
      return;
    }
    
    isLoading.value = false;
  } catch (err) {
    console.error('Общая ошибка обработки конспекта:', err);
    error.value = 'Ошибка обработки конспекта. Пожалуйста, попробуйте позже.';
    isLoading.value = false;
  }
});
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