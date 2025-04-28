<template>
  <div class="app-layout" :class="{ 'no-sidebar': $route.meta.hideSidebar }">
    <Sidebar v-if="!$route.meta.hideSidebar" />

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
</template>

<script setup>
import Sidebar from '@/components/Sidebar.vue'
import { consoleOutput, consoleVisible } from '@/store/console'
import { onMounted } from 'vue'
import { std } from '@/themes/themes'

function applyTheme(theme) {
  for (const [key, value] of Object.entries(theme)) {
    document.documentElement.style.setProperty(`--${key}`, value)
  }
}

onMounted(() => {
  applyTheme(std)
})

</script>

<style>
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  overscroll-behavior: none;
  overflow: hidden;
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
  overflow: hidden;
}

.main-and-console.with-header .main-scroll-zone{
  padding-top: 60px; /* добавляем отступ, если есть шляпа */
}

.main-scroll-zone {
  flex-grow: 1;
  overflow: hidden;
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

.app-layout.no-sidebar .main-and-console {
  padding-left: 0 !important;
}

.app-layout.no-sidebar {
  flex-direction: column; /* или row, если надо */
}

</style>