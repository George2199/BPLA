<template>
  <div class="shlyapabar">
    <button class="sidebar-button">
      <img :src="icons[0]" alt="Меню" class="sidebar-icon" />
    </button>

    <router-link to="/courses" class="sidebar-link">

      <button class="sidebar-button">
        <img :src="icons[1]" alt="Courses" class="sidebar-icon" />
      </button>
    </router-link>

<button class="sidebar-button">
      <img :src="icons[2]" alt="Terminal" class="sidebar-icon" />
    </button>

    <button class="sidebar-button" @click="toggleConsole">
      <img :src="commandIcon" alt="Console" class="sidebar-icon" />
    </button>
    
    <button class="sidebar-button">
      <img :src="icons[4]" alt="Terminal" class="sidebar-icon" />
    </button>

     <button class="sidebar-button">
      <img :src="icons[5]" alt="Terminal" class="sidebar-icon" />
    </button>
    

    <h1 class="shlyapabar-title">{{ pageTitle }}</h1>
  </div>
</template>

<script setup>
import homeIcon from '@/assets/icons/menu.png'
import coursesIcon from '@/assets/icons/courses.png';
import codeIcon from '@/assets/icons/code.png';
import commandIcon from '@/assets/icons/command.png';
import simulatorIcon from '@/assets/icons/simulator.png';
import chatIcon from '@/assets/icons/chat.png';
import { toggleConsole } from '@/store/console'
import { useRoute, onBeforeRouteUpdate } from 'vue-router'
import { computed, ref, watchEffect, inject } from 'vue'
import api from '@/api'

const icons = [homeIcon, coursesIcon, codeIcon, commandIcon, simulatorIcon, chatIcon]
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
    const response = await api.get(`/courses/${id}`)
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
    background: transparent;
    display: flex;
    align-items: center;
    z-index: 0;
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