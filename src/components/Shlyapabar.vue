<template>
  <div class="shlyapabar">
    <button class="sidebar-button">
      <img :src="icons[0]" alt="Меню" class="sidebar-icon" />
    </button>
    <h1 class="shlyapabar-title">{{ pageTitle }}</h1>
  </div>
</template>

<script setup>
import homeIcon from '@/assets/icons/menu.png'
import { useRoute, onBeforeRouteUpdate } from 'vue-router'
import { computed, ref, watchEffect, inject } from 'vue'
import axios from 'axios'

const icons = [homeIcon]
const route = useRoute()
const courseTitle = ref('')


// Заголовок по умолчанию из meta
const pageTitle = computed(() => {
  if (route.name === 'course' && courseTitle.value) {
    return courseTitle.value
  }
  return route.meta.title || ''
})

// Загружаем название курса по ID
const fetchCourseTitle = async (id) => {
  try {
    const response = await axios.get(`http://localhost:5000/courses/${id}`)
    courseTitle.value = response.data.title
  } catch (err) {
    console.error('Ошибка при загрузке курса:', err)
    courseTitle.value = 'Курс'
  }
}

// Когда маршрут меняется — проверяем, надо ли загружать курс
watchEffect(() => {
  if (route.name === 'course' && route.params.id) {
    fetchCourseTitle(route.params.id)
  }
})
</script>

  
  <style>
  .shlyapabar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 60px;
    background: linear-gradient(90deg, var(--shlyapabar_left_color), var(--shlyapabar_right_color));
    display: flex;
    align-items: center;
    z-index: 9999;
    box-sizing: border-box;
  }

  
  .shlyapabar-title {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    color: white;
    font-size: 28px;
    font-weight: bold;
    letter-spacing: 1px;
    margin: 0;
  }

  .sidebar-button {
    background: none;
    border: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .sidebar-icon {
    width: 32px;
    height: 32px;
  }

  </style>