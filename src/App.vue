<template>
  <div class="app-layout">
    <!-- 🧱 Sidebar всегда сбоку -->
    <Sidebar />

    <!-- Вся остальная часть страницы -->
    <div class="main-and-console">
      <!-- Скроллим здесь -->
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
  padding-top: 60px; /* вот здесь — учитываем высоту шляпы */
}

.main-scroll-zone {
  flex-grow: 1;
  overflow: hidden;
}

.bottom-console {
  background: #111;
  color: #0f0;
  font-family: monospace;
  padding: 12px 20px;
  height: 200px;
  overflow-y: auto;
  border-top: 2px solid #444;
  white-space: pre-wrap;
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