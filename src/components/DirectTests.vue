<template>
  <div class="test-card">
    <h2>Тест 1: Контроллер и полёт</h2>
    <div class="kunt">
      <div class="question-block">
        <p><strong>Что такое БВС?</strong></p>
        <label
          v-for="(option, i) in question1"
          :key="'q1' + i"
          class="option"
        >
          <input
            type="checkbox"
            :value="option"
            v-model="answer1"
          />
          {{ option }}
        </label>
      </div>

      <div class="question-block">
        <p><strong>Что такое БВС?</strong></p>
        <label
          v-for="(option, i) in question2"
          :key="'q2' + i"
          class="option"
        >
          <input
            type="checkbox"
            :value="option"
            v-model="answer2"
          />
          {{ option }}
        </label>
      </div>

      <div class="question-block">
        <p><strong>Как расшифровывается “БВС”?</strong></p>
        <input v-model="textAnswer" type="text" class="text-input" />
      </div>
    </div>
  </div>
</template>


  
<script setup>
  import { ref } from 'vue';
  
  const question1 = [
    'Беспилотное воздушное средство',
    'Беспилотное водное средство',
    'Беспилотное ветряное средство',
    'Беспилотное вкусное средство',
  ];
  
  const question2 = [...question1]; // можно поменять на другие при желании
  
  const answer1 = ref([]);
  const answer2 = ref([]);
  const textAnswer = ref('');
  </script>

<style scoped>
/* убрала scoped */
.kunt {
  background: #ffffff;
  max-height: 75vh;
  overflow-y: auto;
  padding-right: 5px;
}

/* скроллбар — ширина 20px */
.kunt::-webkit-scrollbar {
  overflow-y: visible;
  width: 20px;
}

.kunt::-webkit-scrollbar-track {
  background: #f0f0f0;
}

.kunt::-webkit-scrollbar-thumb {
  background-color: #8800cc;
  border-radius: 10px;
}

.kunt::-webkit-scrollbar-thumb:hover {
  background-color: #aa33ff;
}

.kunt::-webkit-scrollbar-thumb:hover {
  background-color: #aa33ff; /* ← Цвет при наведении */
}

.test-card {
  font-family: 'Unbounded', sans-serif;
  background: #8800cc;
  color: white;
  border-radius: 12px;
  padding: 20px;
  width: 360px;
  max-height: 90vh;
}

h2 {
  font-family: 'Unbounded', sans-serif;
  font-weight: 800;
  font-size: 20px;
  margin-bottom: 15px;
}

/* .question-block{   
  font-family: 'Unbounded', sans-serif;
  font-weight:700 !important;
  margin-bottom: 20px;
  color: black;
  padding: 10px;
  border-radius: 8px;
} */

/* .option {
  display: flex;
  align-items: flex-start; 
  gap: 10px;
  font-size: 15px;
  font-weight: 300;
  margin: 8px 0;
  line-height: 1.4;
}
  
input[type="checkbox"] {
  appearance: none;
  width: 16px;
  height: 16px;
  border: 2px solid #8800cc;
  border-radius: 50%;
  background-color: #fff;
  cursor: pointer;
  position: relative;
  flex-shrink: 0;
  margin-top: 2px; 
}


input[type="checkbox"]:checked {
  background-color: #8800cc;
} */



.text-input {
  margin-top: 10px;
  width: 100%;
  padding: 6px;
  font-size: 14px;
  border-radius: 5px;
  border: 2px solid #8800cc;
  outline: none;
}

.text-input:focus {
  border-color: #aa33ff;
  box-shadow: 0 0 0 2px rgba(136, 0, 204, 0.2);
}
/* 
  .question-block strong {
  font-weight: 700;
  }

  label {
    font-weight: 300;
  } */

  </style>
  