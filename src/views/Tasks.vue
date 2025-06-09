<template>
  <div class="app-container">
    <Shlyapabar />

    <div class="main-content">
      <div class="content-wrapper">
        <CourseMenu
          :themes="course?.themes || []"
          @select-task="setSelectedTask"
        />

        <div class="content-box">
          <!-- Кнопка закрытия -->
          <button
            v-show="selectedTask"
            class="close-task"
            @click="clearSelectedTask"
          >
            ×
          </button>

          <!-- Контент таска -->
          <component
            v-if="selectedTask"
            :is="componentsMap[selectedTask?.type]"
            :task="selectedTask"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/api'

import Shlyapabar from '@/components/Shlyapabar.vue'
import CourseMenu from '@/components/CourseMenu.vue'

import TaskVideo from '@/components/tasks/TaskVideo.vue'
import TaskConspect from '@/components/tasks/TaskConspect.vue'
import TaskTest from '@/components/tasks/TaskTest.vue'
import TaskPractical from '@/components/tasks/TaskPractical.vue'
import TaskSummary from '@/components/tasks/TaskSummary.vue'
import TaskBlock from '@/components/tasks/TaskBlock.vue'



const route = useRoute()
const courseId = route.params.id
const course = ref(null)
const selectedTask = ref(null)

const componentsMap = {
  video: TaskVideo,
  test: TaskTest,
  practical: TaskPractical,
  summary: TaskSummary,
  block: TaskBlock,
  conspect: TaskConspect,
}

const setSelectedTask = (task) => {
  selectedTask.value = task
}

const clearSelectedTask = () => {
  selectedTask.value = null
}

onMounted(async () => {
  try {
    const res = await api.get(`/courses/${courseId}`)
    course.value = res.data
  } catch (err) {
    console.error('❌ Ошибка при загрузке курса:', err)
  }
})
</script>



<style scoped>
.h2 {
  margin-top: 0;
}

.close-task {
  position: absolute;
  top: 12px;
  right: 12px;
  background: #ff3333;
  color: transparent;
  font-size: 24px;
  font-weight: bold;
  cursor: pointer;
  appearance: none;
  width: var(--kruglik_size);
  height: var(--kruglik_size);
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
  transition: transform 0.2s ease;
}

/* 🔹 Главный контейнер */
.app-container {
  flex-grow: 1;
  display: flex;
  min-height: 100vh; /* 👈 вместо height: 100vh */
  background: linear-gradient(to bottom right, var(--grad_color_left), var(--grad_color_right));
  color: white;
}


/* 🔹 Основной контент */
.main-content {
  flex-grow: 1;
  min-width: 0;
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 20px;
  overflow: hidden;
}


.content-wrapper {
  display: flex;
  gap: 20px;
  width: 100%;
  align-items: flex-start; /* важный момент! */
}

.content-box {
  position: relative;
  background: var(--border_color);
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
