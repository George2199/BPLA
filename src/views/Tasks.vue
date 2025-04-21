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

const API_URL = import.meta.env.VITE_API_URL

const route = useRoute()
const courseId = route.params.id
const course = ref(null)
const selectedTask = ref(null)

const componentsMap = {
  video: TaskVideo,
  test: TaskTest,
  practical: TaskPractical,
  summary: TaskSummary
}

const setSelectedTask = (task) => {
  selectedTask.value = task
}

onMounted(async () => {
  try {
    const res = await axios.get(`${API_URL}/courses/${courseId}`)
    course.value = res.data

    // автозагрузка первой задачи
    const first = course.value?.themes[0]?.tasks[0]
    if (first) setSelectedTask(first)
  } catch (err) {
    console.error('❌ Ошибка при загрузке курса:', err)
  }
})
</script>


<style>
/* 🔹 Главный контейнер */
.app-container {
  margin-top: 60px;
  display: flex;
  width: 100vw;
  height: 100vh;
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

/* 🔹 Контейнер для меню и контента */
.content-wrapper {
  display: flex;
  flex-grow: 1;
  gap: 20px;
  width: 100%;
  overflow: hidden;
}

/* 🔹 Контентная область */
.content-box {
  flex-grow: 1;
  background: #8D06C3;
  border-radius: 8px;
  padding: 20px;
  min-width: 300px; /* Минимальная ширина */
}
</style>
