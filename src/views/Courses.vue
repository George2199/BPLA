<template>
  <Shlyapabar />
  <div class="app-container">
    <Sidebar />
    <div class="main-content">
      <CoursesIcons/>
    </div>
  </div>
</template>

<script setup>
import Shlyapabar from '@/components/Shlyapabar.vue';
import Sidebar from '@/components/Sidebar.vue';
import CoursesIcons from '@/components/CoursesIcons.vue';
</script>

<style>


/* 🔹 Главный контейнер */
.app-container {
  display: flex;
  width: 100%;
  height: 100vh;
  background: linear-gradient(to bottom right, #581170, #1D012A);
  color: white;
}

/* 🔹 Основной контент */
.main-content {
  margin-top: 60px; /* высота .shlyapabar */
  margin-left: 60px;  /* Учитываем ширину Sidebar */
  width: calc(100vw - 60px); /* Вычитаем Sidebar */
  height: calc(100vh - 120px); 
  display: flex;
  flex-direction: column;
  padding: 20px;
  overflow: hidden;
}

</style>
