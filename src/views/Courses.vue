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

<style scoped>
/* 🔹 Главный контейнер */
.app-container {
  display: flex;
  width: 100%;
  height: 100%;
  background: linear-gradient(to bottom right, var(--grad_color_left), var(--grad_color_right));
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
  padding-top: 30px;
}

</style>
