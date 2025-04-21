<template>
  <div id="app">
    <router-view :key="$route.fullPath" v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </div>
</template>

<script setup>
</script>

<style>
/* 🔹 Убираем лишние отступы и прокрутку */
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  overflow-x: hidden;
}

#app {
  width: 100%;
  height: 100%;
  padding: 0;
}

/* Анимация перехода */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.1s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Общий контейнер скроллбара */
::-webkit-scrollbar {
  width: 8px; /* ширина вертикального */
  height: 8px; /* высота горизонтального */
}

/* Фон скроллбара */
::-webkit-scrollbar-track {
  background: transparent; /* подложка */
  border-radius: 10px;
}

/* Сам ползунок */
::-webkit-scrollbar-thumb {
  background:  rgba(0, 240, 255, 1); /* цвет */
  border-radius: 10px;
}

/* При наведении */
::-webkit-scrollbar-thumb:hover {
  background: #b42ee6;
}

</style> 