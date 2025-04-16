<template>
  <div class="course-menu">
    <div v-for="(topic, index) in topics" :key="index">
      <button @click="toggleTopic(index)" class="topic-button">
        {{ topic.title }}
        <span>{{ openTopic === index ? '▲' : '▼' }}</span>
      </button>
      <div v-if="openTopic === index" class="lessons-list">
        <button v-for="(lesson, i) in topic.lessons" :key="i" class="lesson-button">
          {{ lesson }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const openTopic = ref(null);

const topics = ref([
  { title: 'Тема 1: Полёт и контроллер', lessons: [] },
  { title: 'Тема 2: Полёт и контроллер', lessons: ['Видеоурок 1: Контроллер', 'Видеоурок 2: Полёт', 'Тест 1: Контроллер и полёт', 'Задание 1: Контроллер'] },
  { title: 'Тема 3: Полёт и контроллер', lessons: [] },
  { title: 'Тема 4: Полёт и контроллер', lessons: [] },
  { title: 'Тема 5: Полёт и контроллер', lessons: [] }
]);

const toggleTopic = (index) => {
  openTopic.value = openTopic.value === index ? null : index;
};
</script>

<style>
/* Контейнер меню */
.course-menu {
  width: 300px;
  border-radius: 8px;
  padding: 15px;
}

/* Кнопки тем */
.topic-button {
  width: 100%;
  background: #6a0dad;
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
  background: #7d1ba5;
}

/* Список уроков */
.lessons-list {
  margin-left: 15px;
  margin-top: 5px;
}

/* Кнопки уроков */
.lesson-button {
  width: 100%;
  background: #802dbb;
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
  background: #9c3ddb;
}
</style>
