<template>
  <div class="app-container">
    <header class="course-header">
      Курс 1: Управление БПЛА
    </header>
    <!-- Sidebar -->
    <Sidebar />

    <!-- Основной контент -->
    <div class="main-content">
      <div class="content-wrapper">
        <!-- Меню курса -->
        <CourseMenu />

        <!-- Контентная область -->
        <div class="content-box"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import Sidebar from './components/Sidebar.vue';
import CourseMenu from './components/CourseMenu.vue';
</script>

<style>
/* 🔹 Убираем лишние отступы и прокрутку */
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
}

/* 🔹 Главный контейнер */
.app-container {
  display: flex;
  width: 100vw;
  height: 100vh;
  background: linear-gradient(137deg, #581170 37%, #1D012A 100%);
  color: white;
}

#app {
  padding: 0;
  max-width: fit-content;
}

/* 🔹 Основной контент */
.main-content {
  margin-top: 70px;
  margin-left: 70px;  /* Учитываем ширину Sidebar */
  width: calc(100vw - 70px); /* Вычитаем Sidebar */
  display: flex;
  flex-direction: column;
  padding: 20px;
  overflow: hidden;
}

/* 🔹 Контейнер для меню и контента */
.content-wrapper {
  display: flex;
  flex-grow: 1;
  gap: 20px;
  width: 100%;
  overflow: hidden;
}

/* 🔹 Контентная область */
.content-box {
  flex-grow: 1;
  background: #8D06C3;
  border-radius: 8px;
  padding: 20px;
  min-width: 300px; /* Минимальная ширина */
  margin-right: 5px;
}

.course-header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 70px;
  background: linear-gradient(90deg, #8D06C3 37%, #2B053A 100%);
  color: white;
  font-size: 32px;
  font-weight: 500;
  text-align: left;
  line-height: 70px;
  z-index: 0;
  padding-top: 0px;
  padding-left: 75px;
}
</style>
