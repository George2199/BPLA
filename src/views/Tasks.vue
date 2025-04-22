<template>
  <div class="app-container">
    <Shlyapabar/>
    <!-- Sidebar -->
    <Sidebar />

    <!-- Основной контент -->
    <div class="main-content">
      <div class="content-wrapper">
        <!-- Меню курса -->
        <CourseMenu
          :themes="course?.themes || []"
          @select-task="setSelectedTask"
        />

        <!-- Контентная область -->
        <div class="content-box">
          <button
            v-if="selectedTask"
            class="close-task"
            @click="selectedTask = null"
          >×</button>
        
          <component
            :is="componentsMap[selectedTask?.type]"
            v-if="selectedTask"
            :task="selectedTask"
          />
        </div>

    
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

import Shlyapabar from '@/components/Shlyapabar.vue';
import Sidebar from '@/components/Sidebar.vue'
import CourseMenu from '@/components/CourseMenu.vue'

import TaskVideo from '@/components/tasks/TaskVideo.vue'
import TaskTest from '@/components/tasks/TaskTest.vue'
import TaskPractical from '@/components/tasks/TaskPractical.vue'
import TaskSummary from '@/components/tasks/TaskSummary.vue'
import TaskBlock from '@/components/tasks/TaskBlock.vue'

const API_URL = import.meta.env.VITE_API_URL

const route = useRoute()
const courseId = route.params.id
const course = ref(null)
const selectedTask = ref(null)

const componentsMap = {
  video: TaskVideo,
  test: TaskTest,
  practical: TaskPractical,
  summary: TaskSummary,
  block: TaskBlock, // 🆕 Добавили!
}

const setSelectedTask = (task) => {
  selectedTask.value = task
}

onMounted(async () => {
  try {
    const res = await axios.get(`${API_URL}/courses/${courseId}`)
    course.value = res.data
  } catch (err) {
    console.error('❌ Ошибка при загрузке курса:', err)
  }
})
</script>


<style>
.h2 {
  margin-top: 0;
}

.close-task {
  position: absolute;
  top: 5px;
  right: 6px;
  font-size: 26px;
  color: white;
  background: transparent;
  border: none;
  cursor: pointer;
  z-index: 5;
  transition: transform 0.2s ease;
}

/* 🔹 Главный контейнер */
.app-container {
  display: flex;
  width: 100vw;
  min-height: 100vh; /* 👈 вместо height: 100vh */
  background: linear-gradient(to bottom right, #6a0dad, #2d033b);
  color: white;
}


/* 🔹 Основной контент */
.main-content {
  margin-left: 70px;  /* Учитываем ширину Sidebar */
  width: calc(100vw - 70px); /* Вычитаем Sidebar */
  display: flex;
  flex-direction: column;
  padding: 20px;
  overflow: hidden;
}

.content-wrapper {
  margin-top: 60px;
  display: flex;
  gap: 20px;
  width: 100%;
  align-items: flex-start; /* важный момент! */
}

.content-box {
  position: relative;
  background: #8D06C3;
  border-radius: 8px;
  min-width: 300px;
  width: 100%;
  max-width: 100%;
  display: block;
  overflow: hidden; /* 👈 блокируем всё лишнее */
  margin: 0 auto;
  max-height: calc(100vh - 120px); /* 👈 (примерно: 60px шляпа + 60px отступы) */
  box-sizing: border-box;
}

.content-box > * {
  flex-grow: 1; /* компонент внутри займет всё пространство */
}

</style>
