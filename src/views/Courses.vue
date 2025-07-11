<template>
  <div class="app-container">
      
   <!-- <TatliStarts />  -->
    <div class="main-content">
  <Shlyapabar />

      <CoursesIcons/>

        <Botinokbar />
    </div>
  </div>
</template>

<script setup>
import Shlyapabar from '@/components/Shlyapabar.vue';
import Botinokbar from '@/components/Botinokbar.vue';
import CoursesIcons from '@/components/CoursesIcons.vue';
// import StarField from '@/components/StarField.vue'
// import TatliStarts from '@/components/TatliStarts.vue'
</script>

<style scoped>

/* 🔹 Основной контент */
.main-content {
  height: 100%; 
  width: 100%;
  display: flex;
  flex-direction: column;
  overflow-y:auto;
  width: 100%;
  padding-top: 100px; 
  padding-left: 100px;
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
