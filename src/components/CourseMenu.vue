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

const toggleTopic = (index) => {
  const idx = openedTopics.value.indexOf(index)
  if (idx === -1) {
    openedTopics.value = [index] // 👈 открываем только одну тему
  } else {
    openedTopics.value = []
  }
}

const selectTask = (task) => {
  emit('select-task', task)
}
</script>

<style scoped>

.course-menu {
  display: flex;
  gap: 15px;
  padding: 0 60px;
  margin-top: 30px;
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
  width: 250px;
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
  width: 250px;
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
  top: calc(100% + 16px);
  background-color: var(--lesson_button);
  padding: 10px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  z-index: 100;
  min-width: 260px;
}

.lesson-button {
  background: transparent;
  border: none;
  color: white;
  text-align: left;
  padding: 8px;
  border-radius: 4px;
  cursor: pointer;
}

.lesson-button:hover {
  background: var(--lesson_button_hover);
}

</style>
