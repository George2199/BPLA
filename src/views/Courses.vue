<template>
  <div class="app-container">
    <Sidebar />
    <div class="main-content">
      <h1 class="course-title">Ваши курсы</h1>
      <CoursesIcons/>
    </div>
  </div>
</template>

<script setup>
import Sidebar from '@/components/Sidebar.vue';
import CoursesIcons from '@/components/CoursesIcons.vue';
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

.course-title {
  font-size: 24px;
  margin-bottom: 20px;
  color: white;
}
</style>
