<template>
  <div class="course-menu">
    <div class="topic-container" v-for="(theme, index) in themes" :key="theme.id" >
      <button @click="toggleTopic(index)" class="topic-button">
        {{ theme.title }}
        <span>{{ openedTopics.includes(index) ? '▲' : '▼' }}</span>
      </button>

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
    openedTopics.value.push(index)
  } else {
    openedTopics.value.splice(idx, 1)
  }
}

const selectTask = (task) => {
  emit('select-task', task)
}
</script>


<style>
/* Контейнер меню */
.course-menu {
  width: 300px;
  border-radius: 8px;
}

/* Кнопки тем */
.topic-button {
  width: 100%;
  background: var(--topic_button_color);
  color: white;
  padding: 10px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  text-align: left;
  font-size: 16px;
  margin-bottom: 5px;
  display: flex;
  justify-content: space-between;
}

.topic-button:hover {
  background: var(--topic_button_color_hover);
}

/* Список уроков */
.lessons-list {
  margin-left: 15px;
  margin-top: 5px;
}

/* Кнопки уроков */
.lesson-button {
  width: 100%;
  background: var(--lesson_button);
  color: white;
  padding: 8px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  text-align: left;
  font-size: 14px;
  margin-top: 3px;
}

.lesson-button:hover {
  background: var(--lesson_button_hover);
}

.topic-container {
  margin-bottom: 5px; /* или сколько нужно */
}

</style>
