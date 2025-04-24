<template>
  <Shlyapabar />
  <div class="app-container">
    <div class="main-content">
      <CoursesIcons/>
    </div>
  </div>
</template>

<script setup>
import Shlyapabar from '@/components/Shlyapabar.vue';
import CoursesIcons from '@/components/CoursesIcons.vue';
</script>

<style>


/* 🔹 Главный контейнер */
.app-container {
  display: flex;
  width: 100%;
  height: 100%;
  background: linear-gradient(to bottom right, #581170, #1D012A);
  color: white;
  margin-top: 0;
}

/* 🔹 Основной контент */
.main-content {
  height: 100%; 
  display: flex;
  flex-direction: column;
  overflow-y:auto;
  width: 100%;
}

</style>
