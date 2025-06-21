<template>
  <div class="app-container">
      
  <!-- <TatliStarts /> -->
    <div class="main-content">
  <Shlyapabar />

      <CoursesIcons/>
    </div>
  </div>
</template>

<script setup>
import Shlyapabar from '@/components/Shlyapabar.vue';
import CoursesIcons from '@/components/CoursesIcons.vue';
import StarField from '@/components/StarField.vue'
import TatliStarts from '@/components/TatliStarts.vue'
</script>

<style scoped>
/* 🔹 Главный контейнер */
.app-container {
  display: flex;
  width: 100%;
  height: 100%;
  /* background: linear-gradient(to bottom right, var(--grad_color_left), var(--grad_color_right)); */
  color: white;
  margin-top: 0;
}

/* 🔹 Основной контент */
.main-content {
  height: 100%; 
  width: 100%;
  display: flex;
  flex-direction: column;
  overflow-y:auto;
  width: 100%;
  padding-top: 30px;
}

:global(body) {
  margin: 0;
  padding-left: 0;
  height: 100vh;
  background-color:#08000e;
  background-repeat: no-repeat;
  background-size: cover;
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: 'Inter', sans-serif;
  position: relative;
  overflow: hidden;
}

</style>
