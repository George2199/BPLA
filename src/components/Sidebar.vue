<template>
  <div class="sidebar">
    <!-- Книга (router-link) -->
    <router-link to="/courses" class="sidebar-link">
      <button class="sidebar-button">
        <img :src="icons[0]" alt="Courses" class="sidebar-icon" />
      </button>
    </router-link>

    <button class="sidebar-button">
      <img :src="icons[1]" alt="Terminal" class="sidebar-icon" />
    </button>

    <button class="sidebar-button" @click="toggleConsole">
      <img :src="commandIcon" alt="Console" class="sidebar-icon" />
    </button>


    <!-- Остальные кнопки -->
    <button
      v-for="(icon, index) in icons.slice(3)"
      :key="index"
      class="sidebar-button"
    >
      <img :src="icon" alt="Icon" class="sidebar-icon" />
    </button>
  </div>
</template>


<script setup>
import coursesIcon from '@/assets/icons/courses.png';
import codeIcon from '@/assets/icons/code.png';
import commandIcon from '@/assets/icons/command.png';
import simulatorIcon from '@/assets/icons/simulator.png';
import chatIcon from '@/assets/icons/chat.png';
import { toggleConsole } from '@/store/console'

const icons = [coursesIcon, codeIcon, commandIcon, simulatorIcon, chatIcon];
</script>


<style>
.sidebar {
  width: 60px;
  height: 100%;
  background: #8D06C3;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 15px 0;
  box-sizing: border-box;
}

.sidebar-button,
.sidebar-button:link,
.sidebar-button:visited {
  background: none;
  border: none;
  cursor: pointer;
  padding: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 50px;
  height: 50px;
} 

.sidebar a.sidebar-button {
  padding: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 50px;
  height: 50px;
}


/* 📌 Иконки */
.sidebar-icon {
  width: 32px; /* ✅ Уменьшаем размер иконки */
  height: 32px;
  object-fit: contain; /* ✅ Сохраняем пропорции */
}

</style>
