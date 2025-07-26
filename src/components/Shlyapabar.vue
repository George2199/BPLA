<template>
  <div class="shlyapabar">
    <div class="buttons_kunt">

      <router-link to="/courses" class="sidebar-link">

        <button class="shlyapa-button">Курсы</button>
      </router-link>

        <button class="shlyapa-button">IDE</button>

        <button class="shlyapa-button" @click="toggleConsole">Консоль</button>
      
        <button class="shlyapa-button">Симулятор</button>
      
    </div>
                <div class="custom-slot-right">
                      <slot name="course-menu"></slot>

    </div> 
  </div>
</template>

<script setup>
import { toggleConsole } from '@/store/console'
import { useRoute, onBeforeRouteUpdate } from 'vue-router'
import { computed, ref, watchEffect, inject } from 'vue'
import api from '@/api'

const route = useRoute()
const courseTitle = ref('')



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

  .shlyapa-button {
  cursor: pointer;
  /* margin-top: 15px; */
  width: 200px;
  padding: 10px;
  margin: 5px;
  border-radius: 13px;
  border: 1px solid #CDBDF5; /* тонкая светлая рамка */
  background-color: transparent; /* 👈 делает фон прозрачным */
  color: #EDEFFF; /* текст бело-сиреневый */
  font-size: 18px;
  /* outline: none; */
  /* transition: border-color 0.2s, box-shadow 0.2s; */
}

  .shlyapa-button:hover{
  background-color: #501FD2;
  border: 1px solid #501FD2; 

  }

  .buttons_kunt{
  padding-left: 75px;
  padding-top: 50px;
   padding-bottom: 10px;
  display: flex;
  flex-direction: row;


  }
  .shlyapabar {
    position: relative;
    width: 100%;
    height: 80px;
    background: transparent;
    display: flex;
    align-items: center;
    z-index: 0;
    box-sizing: border-box;
  }


  .custom-slot-right {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-top: 25px;
  }

  </style>