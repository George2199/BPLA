<template>
  <div class="app-container">
    <!-- Sidebar -->
    <Sidebar />

    <!-- Основной контент -->
    <div class="main-content">
      <h1 class="course-title">Курс 1: Управление БПЛА</h1>
      <div class="content-wrapper">
        <!-- Меню курса -->
        <CourseMenu />

        <!-- Контентная область -->
        <div class="content-box">
          <Video />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import Sidebar from '@/components/Sidebar.vue';
import CourseMenu from '@/components/CourseMenu.vue';
import Video from '@/components/video.vue';
</script>

<style>
/* 🔹 Главный контейнер */
.app-container {
  display: flex;
  width: 100vw;
  height: 100vh;
  background: linear-gradient(to bottom right, #6a0dad, #2d033b);
  color: white;
}

/* 🔹 Основной контент */
.main-content {
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
}
</style>
