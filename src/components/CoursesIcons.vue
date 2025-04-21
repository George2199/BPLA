<template>
  <div class="container">
    <router-link
  v-for="course in courses"
  :key="course.id"
  class="card"
  :to="`/courses/${course.id}`"
>
  <div class="progress-wrapper">
    <div
      class="progress-bar"
      :style="{ height: (course.progress * 100) + '%' }"
    ></div>
  </div>

  <img
    class="card-image"
    :src="`${API_URL}${course.image_url}`"
    :alt="course.title"
  />
  <div class="card-text">{{ course.title }}</div>
</router-link>

  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL
const courses = ref([])

onMounted(async () => {
  try {
    const res = await axios.get(`${API_URL}/courses`)
    courses.value = res.data
  } catch (e) {
    console.error('❌ Не удалось загрузить курсы:', e)
  }
})
</script>


<style>

.card {
  position: relative;
  width: 370px;
  border: 1px solid #9c9c9cb6;
  border-radius: 16px;
  overflow: hidden;
  font-family: Arial, sans-serif;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.2s;
  text-decoration: none;
  color: inherit;
}

.progress-wrapper {
  position: absolute;
  top: 0;
  right: 0;
  width: 12px;
  height: 100%;
  background: transparent;
  border-radius: 0 16px 16px 0;
  overflow: hidden;
  z-index: 2;

  display: flex;
  align-items: flex-end; /* 👈 ВАЖНО: чтобы fill шёл снизу */
}

.progress-bar {
  width: 100%;
  background: linear-gradient(
    to bottom,
    rgba(0, 238, 255, 0) 2%,
    rgba(0, 240, 255, 1) 25%,
    rgb(153, 0, 255) 80%
  );
  transition: height 0.3s ease-in-out;
  /* box-shadow: 0 0 10px #00f0ff, 0 0 20px #9a00ff; */

}

.container {
  margin-top:90px;
    display: flex;
    flex-wrap: wrap;
    gap: 80px; /* Расстояние между блоками */
    max-width: 2000px; /* Ограничение ширины, чтобы влезало 3 блока */
    margin-left:  50px; 
}

.card {
    position: relative; 
    width: 370px; /* или под нужный размер */
    border: 1px solid #9c9c9cb6; 
    border-radius: 16px;
    overflow: hidden; /* чтобы изображение не выходило за границы */
    font-family: Arial, sans-serif;
    box-shadow:
    0 0 10px 2px rgba(154, 0, 255, 0.2),
    0 0 20px 4px rgba(0, 240, 255, 0.2),
    inset 0 0 10px rgba(154, 0, 255, 0.1);
    cursor: pointer;
    transition: box-shadow 0.4s ease;
    text-decoration: none;
    color: inherit;
}

.card:hover {
    box-shadow:
    0 0 10px 2px rgba(153, 0, 255, 0.753),
    0 0 20px 4px rgba(0, 238, 255, 0.623),
    inset 0 0 10px rgba(153, 0, 255, 0.459);
}

.card-image {
    width: 100%;
    height: auto;
    display: block;
}

.card-text {
    padding: 4px;
    font-size: 22px;
    letter-spacing: 2px;
    font-weight:lighter;
    text-align: center;
    color: #333;
    background: #D8D7FF;
}
</style>