<template>
  <div v-if="!$route.meta.fullscreen" class="app-layout">
  <TatliStarts />



    <div class="main-and-console" :class="{ 'with-header': $route.meta.hasHeader }">
      <div class="main-scroll-zone">
        <router-view :key="$route.fullPath" v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>

      <div v-if="consoleVisible" class="bottom-console">
        <pre>{{ consoleOutput }}</pre>
      </div>
    </div>
  </div>

  <!-- 👇 если fullscreen, просто рендерим компонент -->
  <router-view v-else :key="$route.fullPath" />
</template>


<script setup>
import TatliStarts from '@/components/TatliStarts.vue'
import { consoleOutput, consoleVisible, toggleConsole, hideConsole } from '@/store/console'
import { onMounted, onBeforeUnmount } from 'vue'
import { std } from '@/themes/themes'

function applyTheme(theme) {
  for (const [key, value] of Object.entries(theme)) {
    document.documentElement.style.setProperty(`--${key}`, value)
  }
}


onMounted(() => {
  applyTheme(std)

  const keyListener = (e) => {
    const tag = e.target.tagName?.toLowerCase()
    const isTyping = ['input', 'textarea'].includes(tag) || e.target.isContentEditable

    // Esc закрывает, если не в поле ввода
    if (e.key === 'Escape' && !isTyping) {
      hideConsole()
    }

    // Ctrl + ~ (Backquote) переключает консоль
    if (e.ctrlKey && e.code === 'Backquote') {
      e.preventDefault()
      toggleConsole()
    }
  }

  window.addEventListener('keydown', keyListener, true)
  window._keyListener = keyListener
})

onBeforeUnmount(() => {
  if (window._escListener) {
    window.removeEventListener('keydown', window._escListener)
    delete window._escListener
  }
})

</script>

<style>
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  overscroll-behavior: none;
  overflow:auto;
  user-select: none;
}

#app,
.app-layout {
  height: 100vh;
  width: 100%;
  display: flex;
  flex-direction: row;
}

.main-and-console {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  height: 100%;
 overflow:auto;
}

/* .main-and-console.with-header .main-scroll-zone{
  padding-top: 60px; добавляем отступ, если есть шляпа
} */

.main-scroll-zone {
  flex-grow: 1;
  overflow: auto;
  min-height: 0;
}

.bottom-console {
  flex: 0 0 200px;
  background: #111;
  color: #0f0;
  font-family: monospace;
  padding: 12px 20px;
  overflow-y: auto;
  border-top: 2px solid #444;
  white-space: pre-wrap;
  box-sizing: border-box;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.1s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}



</style>