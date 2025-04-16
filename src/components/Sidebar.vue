<template>
  <div class="sidebar">
    <button v-for="(icon, index) in icons" :key="index" class="sidebar-button">
      <img :src="icon" alt="Icon" class="sidebar-icon" />
    </button>
  </div>
</template>

<script setup>
import homeIcon from '@/assets/icons/menu.png';
import coursesIcon from '@/assets/icons/courses.png';
import codeIcon from '@/assets/icons/code.png';
import commandIcon from '@/assets/icons/command.png';
import simulatorIcon from '@/assets/icons/simulator.png';
import chatIcon from '@/assets/icons/chat.png';

const icons = [homeIcon, coursesIcon, codeIcon, commandIcon, simulatorIcon, chatIcon];
</script>

<style>
/* 📌 Sidebar */
.sidebar {
  width: 70px;
  height: 100vh;
  background: #8D06C375;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 15px 0;
  position: fixed;
  top: 0;
  left: 0;
}

/* 📌 Кнопки */
.sidebar-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 50px; /* ✅ Фиксируем размер кнопки */
  height: 50px;
}

/* 📌 Иконки */
.sidebar-icon {
  width: 32px; /* ✅ Уменьшаем размер иконки */
  height: 32px;
  object-fit: contain; /* ✅ Сохраняем пропорции */
}
</style>
