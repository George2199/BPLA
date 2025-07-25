<template>
  <div class="botinokbar">
    <div class="bot_buttons_kunt">

    <button class="botinokbar-button">Чат с куратором</button>

    <button class="botinokbar-button">Настройки</button>

    </div> 
  </div>
</template>


<script setup>
import { toggleConsole } from '@/store/console'
import { useRoute, onBeforeRouteUpdate } from 'vue-router'
import { computed, ref, watchEffect, inject } from 'vue'
import api from '@/api'

const route = useRoute()
const courseTitle = ref('')


</script>

  <style>

 .botinokbar-button {
  cursor: pointer;
  margin-top: 11px;
  width: 200px;
  padding: 10px;
  margin: 5px;
  border-radius: 13px;
  border: 1px solid #CDBDF5; /* тонкая светлая рамка */
  background-color: transparent; /* 👈 делает фон прозрачным */
  color: #EDEFFF; /* текст бело-сиреневый */
  font-size: 18px;
  /* outline: none; */
  /* transition: border-color 0.2s, box-shadow 0.2s; */
}

  .botinokbar-button:hover{
  background-color: #501FD2;
  border: 1px solid #501FD2; 

  }

  .bot_buttons_kunt{
  padding-right: 130px;
  padding-bottom: 30px;
  /* margin-bottom: 60px; */

  }
  .botinokbar {
    position: fixed;
    bottom: 0;
    right: 0;
    height: 80px;
    background: transparent;
    display: flex;
    align-items: center;
    z-index: -1;
    box-sizing: border-box;
    padding-bottom: 4%;
  }

  </style>