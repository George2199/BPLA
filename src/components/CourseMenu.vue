<template>
  <div class="course-menu">
    <div
      v-for="(theme, index) in themes"
      :key="theme.id"
      class="tab-wrapper"
    >
      <div
        class="topic-button"
        :class="{ active: openedTopics.includes(index) }"
        @click="toggleTopic(index)"
      >
        {{ theme.title }}
        <div class="triangle" v-if="openedTopics.includes(index)" />
      </div>

      <div v-if="openedTopics.includes(index)" class="lessons-list">
        <button
          v-for="task in theme.tasks"
          :key="task.id"
          class="lesson-button"
          :class="{ active: activeTaskId === task.id }"
          @click="selectTask(task)"
        >
          {{ task.title }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  themes: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['select-task'])

const openedTopics = ref([])
const activeTaskId = ref(null) // Храним ID активной задачи

const toggleTopic = (index) => {
  const idx = openedTopics.value.indexOf(index)
  if (idx === -1) {
    openedTopics.value = [index]
  } else {
    openedTopics.value = []
  }
}

const selectTask = (task) => {
  activeTaskId.value = task.id // Устанавливаем активную задачу
  emit('select-task', task)
}
</script>

<style scoped>

.course-menu {
  display: flex;
  gap: 10px;
  padding: 0 60px;
  margin-top: 1px;
}

.tab-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}

.topic-button {
  background: transparent;
  border: none;
  color: #EDEFFF; /* 👈 всегда светлый текст */
  cursor: pointer;
  font-size: 18px;
  padding-bottom: 24px;
  position: relative;
  width: 350px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
}



/* Подчеркивание */
.topic-button::after {
  content: "";
  position: absolute;
  bottom: 12px;
  left: 0;
  width: 350px;
  height: 2px;
  background-color: #CDBDF5;
}

.topic-button.active::after {
  background-color: #501FD2; /* активный — фиолетовый */
}

/* Треугольник один — внизу */
.topic-button::before {
  content: "";
  position: absolute;
  bottom: -6px;
  left: 50%;
  transform: translateX(-50%);
  border-left: 40px solid transparent;
  border-right: 40px solid transparent;
}

.topic-button.active::before {
  border-bottom: 15px solid #501FD2; /* нормальный треугольник */
}

.topic-button:not(.active)::before {
  border-top: 15px solid #CDBDF5; /* перевёрнутый */
}

/* Выпадающий список заданий */
.lessons-list {
  position: absolute;
  top: calc(100% + 12px);
  background-color: transparent;
  padding: 6px;
  display: flex;
  overflow-y: auto;
  flex-direction: column;
  z-index: 100;
  width: 340px;
  left: 0px;
  height: 80px;
}

.lessons-list::-webkit-scrollbar {
  height: 8px;
  width: 6px;
}
.lessons-list::-webkit-scrollbar-thumb {
  background: transparent;
  border: 1PX SOLID #d6cbf3af;
  border-radius: 6px;
}
.lessons-list::-webkit-scrollbar-track {
  background: transparent;
}

.lesson-button {
  background: transparent;
  border: none;
  color: white;
  text-align: left;
  padding: 6px 24px 6px 12px; /* Добавим правый отступ для точки */
  border-radius: 4px;
  cursor: pointer;
  position: relative; /* Для позиционирования псевдоэлемента */
}

.lesson-button.active::after {
  content: "";
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  width: 6px;
  height: 6px;
  background-color: white;
  border-radius: 50%;
}

.lesson-button:hover {
  background: #501FD2;
}

</style>
