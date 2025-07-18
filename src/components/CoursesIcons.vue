<template>
<svg width="0" height="0">
  <defs>
    <mask id="cutout-mask" maskContentUnits="objectBoundingBox">
      <!-- Показываем всё -->
      <rect x="0" y="0" width="1" height="1" fill="white" />
      
      <!-- Сглаженный вырез -->
     <path
        d="
          M 0 0
          Q 0 0.18, 0 0.28
          Q 0 0.18, 0.05 0.18
          L 0.46 0.18
          Q 0.50 0.18, 0.50 0.13
          L 0.50 0.05
          Q 0.50 0, 0.55 0
          L 0 0
          Z
        "
        fill="black"
      />

    </mask>
  </defs>
</svg>

  <div class="container">
    <router-link
  v-for="course in courses"
  :key="course.id"
  class="card"
  :to="`/courses/${course.id}`"
>


<div class="card-image-wrapper">
  <img
    class="card-image"
    :alt="course.title"
    :src="`${API_BASE_URL}${course.image_url}`"
    
  />
   <div class="card-arrow">
    <svg
      xmlns="http://www.w3.org/2000/svg"
      class="arrow-icon"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
      stroke-width="2"
    >
      <circle cx="12" cy="12" r="10" fill="white" />
      <path stroke="#7C6EF2" d="M8 16l8-8M10 8h6v6" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </div>
</div>
  <div class="card-text">{{ course.title }}</div>

  <div class="progress-wrapper">
  <div
    class="progress-bar"
    :class="course.progress, 'progress-bar-gradient'"
    :style="{ width: (course.progress * 100) + '%' }"
  ></div>
</div>

</router-link>


  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import api, { API_BASE_URL } from '@/api'

const courses = ref([])

onMounted(async () => {
  try {
    const res = await api.get('/courses')
    courses.value = res.data
  } catch (e) {
    console.error('❌ Не удалось загрузить курсы:', e)
  }
})
</script>


<style>
.card-arrow {
  position: absolute;
  bottom: 12px;
  right: 12px;
  width: 40px;
  height: 40px;
  background-color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 3;
  box-shadow: 0 0 10px rgba(0,0,0,0.2);
  transition: transform 0.3s ease;
}

.card-arrow:hover {
  transform: scale(1.1);
}

.arrow-icon {
  width: 24px;
  height: 24px;
  color: #7C6EF2;
}

.container::-webkit-scrollbar {
  height: 8px;
  width: 8px;
}
.container::-webkit-scrollbar-thumb {
  background: #d6cbf3af;
  border-radius: 6px;
}
.container::-webkit-scrollbar-track {
  background: transparent;
}


.progress-wrapper {
  height: 10px;
  width: 99%;
  background-color: transparent;
  border-radius: 4px;
  overflow: hidden;
  margin-top: 6px;
  margin-bottom: 10px;
  border: 1px solid #CDBDF5; 
  
}

.progress-bar {
  height: 100%;
  background: linear-gradient(to right, #CDBDF5);
  transition: width 0.3s ease-in-out;  
    clip-path: polygon(
    0 0,             /* top-left */
    calc(100% - 10px) 0,  /* top-right before slant */
    100% 100%,       /* bottom-right tip of slant */
    0 100%           /* bottom-left */
  );
}

.card-image{
  border-radius: 30px;
}

.card-image-wrapper {
  position: relative;
  overflow: hidden;
  mask: url(#cutout-mask);
  -webkit-mask: url(#cutout-mask);
}


/* .progress-wrapper {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 100%;
  height: 12px;
  background: transparent;
  border-radius: 0 16px 16px 0;
  overflow: hidden;
  z-index: 2;

  display: flex;
  align-items: flex-end; 
}


.progress-bar-gradient {
  width: 100%;
  background: #b8c0f1; 
  transition: height 0.3s ease-in-out;


} */

.container {
  margin-left: 300px;
  scroll-behavior: smooth;
  display: flex;
  flex-wrap: wrap;
   overflow-y: auto;
  gap: 50px; /* Расстояние между блоками */
  max-width: 1600px; /* Ограничение ширины, чтобы влезало 3 блока */
  margin-left:  50px; 
   height: 65vh; 
}

.card {
    position: relative; 
    width: 460px; /* или под нужный размер */
    height: 340px; /* или под нужный размер */
    font-family: Arial, sans-serif;
    cursor: pointer;
    transition: box-shadow 0.4s ease;
    text-decoration: none;
    color: inherit;
}



.card-image {
    width: 100%;
    height: auto;
    display: block;
}

.card-text {
  position: absolute;
  top: 2%;
  left: 3%;
  font-size: 1.5em;
  font-style: italic;
  font-weight: 300;
  color: white;
  /* text-shadow: 0 0 4px rgba(0, 0, 0, 0.6); */
  z-index: 2;
  text-align: center;
}
</style>