<template>
  <div class="app-layout"
  :class="{ 'no-sidebar': $route.meta.hideSidebar }"
  :style="{
    '--bg': background_color,
    '--border': border_color,
    '--text': text_color,
    '--kruglik': kruglik_size,
    '--grad_clr_l': grad_color_left,
    '--grad_clr_r': grad_color_right,
  }">
    <!-- 🧱 Sidebar всегда сбоку -->
    <Sidebar v-if="!$route.meta.hideSidebar" />

    <!-- Вся остальная часть страницы -->
    <div class="main-and-console" :class="{ 'with-header': $route.meta.hasHeader }">
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
import { provide } from 'vue'


const background_color = "#ffffff"
const border_color = "#8800cc"
const text_color = "#000000"
const kruglik_size = "16px"
const grad_color_left = "#581170"
const grad_color_right = "#1D012A"

provide('background_color', background_color)
provide('border_color', border_color)
provide('text_color', text_color)
provide('kruglik_size', kruglik_size)
provide('grad_color_left', grad_color_left)
provide('grad_color_right', grad_color_right)

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