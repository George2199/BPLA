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
  margin-left: 60px;  /* Учитываем ширину Sidebar */
  height: calc(100vh - 60px); 
  display: flex;
  flex-direction: column;
  padding: 20px;
  overflow-y:auto;
  width: calc(100vw - 60px);
}

</style>
