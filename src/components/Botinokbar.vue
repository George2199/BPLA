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

  <style scoped>
  .botinokbar {
    width: 100%;
    padding: 20px 0;
    margin-top: 20px; /* Отступ от контента */
  }

  .bot_buttons_kunt {
    display: flex;
    justify-content: flex-end; /* Выравниваем кнопки вправо */
    gap: 10px;
    padding-right: 40px; /* Отступ от правого края */
    padding-bottom: 90px; /* Отступ от правого края */
  }

  .botinokbar-button {
    cursor: pointer;
    width: 200px;
    padding: 10px;
    border-radius: 13px;
    border: 1px solid #CDBDF5;
    background-color: transparent;
    color: #EDEFFF;
    font-size: 18px;
  }

  .botinokbar-button:hover {
    background-color: #501FD2;
    border: 1px solid #501FD2; 
  }

    </style>