<template>
  <div class="app-container">
    <Shlyapabar>
      <template #course-menu>
        <CourseMenu
          :themes="course?.themes || []"
          @select-task="setSelectedTask"
        />
      </template>
    </Shlyapabar>

    <div class="course_bar">
      <!-- Ваш курс меню -->
    </div>
    
    <div class="main-content">
      <div class="content-wrapper">
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
      
      <!-- Botinokbar теперь внутри main-content, но после content-wrapper -->
      <div class="botinokbar-container">
        <Botinokbar />
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
import Botinokbar from '@/components/Botinokbar.vue';

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
  blocks: TaskBlock,
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
.botinokbar-container {
  width: 100%;
  padding: 20px 0;
  margin-top: auto; /* Это прижмет контейнер к низу */
}

/* Обновляем стили для main-content */
.main-content {
  flex-grow: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  padding: 20px;
  padding-top: 0; /* 👈 Убираем лишний отступ, так как шляпа уже в потоке */
  overflow: visible;
}


.content-wrapper {
  flex-grow: 1; /* Занимает все доступное пространство */
  display: flex;
  gap: 20px;
  width: 83%;
  align-items: flex-start;
  margin-left: auto;
  margin-right: auto;
}


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

.course_bar {
  display: flex;
  justify-content: flex-start;
  padding: 0 40px;
  /* margin-top: 16px; */
  right: 0px;
  top: 0px;
  height: 100px;
}


/* 🔹 Главный контейнер */
.app-container {
  background-color:transparent;
  /* padding-top: 50px; */
  flex-grow: 1;
  display: flex;
  flex-direction: column; /* 👈 теперь контент идёт сверху вниз */
  flex-grow: 1;
  min-height: 100vh;
  color: white;
}


.content-wrapper {
  display: flex;
  gap: 20px;
  width: 83%;
  align-items: flex-start; /* важный момент! */
  margin-left: auto;
  margin-right: auto;
}

.content-box {
  position: relative;
  border-radius: 8px;
  min-width: 300px;
  width: 100%;
  max-width: 100%;
  display: block;
  overflow: hidden; /* 👈 блокируем всё лишнее */
  max-height: calc(100vh - 120px); /* 👈 (примерно: 60px шляпа + 60px отступы) */
  box-sizing: border-box;
}

.content-box > * {
  flex-grow: 1; /* компонент внутри займет всё пространство */
}

</style>
