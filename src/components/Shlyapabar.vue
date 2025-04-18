<template>
    <div class="shlyapabar">
        <button class="sidebar-button">
             <img :src="icons[0]" alt="Меню" class="sidebar-icon" />
         </button>
      <h1 class="shlyapabar-title">Ваши курсы</h1>
    </div>
  </template>
  
  <script setup>
import homeIcon from '@/assets/icons/menu.png';
const icons = [homeIcon];
  </script>
  
  <style>
  .shlyapabar {
    position: fixed;
    top: 0;
    height: 60px;
    width: 100%;
    background: linear-gradient(90deg, #8D06C3, #1D012A);
    display: flex;
    align-items: center;
    z-index: 1000;
  }
  
  .shlyapabar-title {
    padding-left: 30px;
    color: white;
    font-size: 22px;
    font-weight: bold;
    letter-spacing: 1px;
    margin: 0;
  }
  </style>