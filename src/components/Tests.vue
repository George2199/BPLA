<template>
    <div class="test-card" :style="{
        '--bg': background_color,
        '--border': border_color,
        '--text': text_color,
        '--kruglik': kruglik_size,
        }">
     
     <button class="close-button" @click="visible = false">×</button>

        <h2>Тест: Контроллер и полёт</h2>
        <div class="kunt">
        <ManySelect
            v-for="(questionBlock, index) in questions"
            :key="index"
            :question="questionBlock.question"
            :options="questionBlock.options"
            v-model="answers[index]"
            :background_color=background_color
            :border_color=border_color
            :text_color=text_color
            :kruglik_size=kruglik_size
        />
        </div>
    </div>
</template>
  
<script setup>
  import { ref } from 'vue'
  import ManySelect from './testBlocks/ManySelect.vue' // путь подстрой под свою структуру
  const background_color = "#ffffff"
  const border_color = "#8800cc"
  const text_color = "#000000"

const kruglik_size = "16px"
  const questions = ref([
    {
      question: 'Что такое БВС?',
      options: [
        'Беспилотное воздушное средство',
        'Беспилотное водное средство',
        'Беспилотное ветряное средство',
        'Беспилотное вкусное средство'
      ]
    },
    {
      question: 'Для чего применяют БВС?',
      options: [
        'Разведка',
        'Фото- и видеосъёмка',
        'Бои и шпионаж',
        'Прогулка с собакой'
      ]
    },
    {
      question: 'Где нельзя запускать БВС?',
      options: [
        'Над военными объектами',
        'Вблизи аэропортов',
        'В закрытых помещениях',
        'На Юпитере'
      ]
    },
    {
      question: 'Что такое БВС?',
      options: [
        'Беспилотное воздушное средство',
        'Беспилотное водное средство',
        'Беспилотное ветряное средство',
        'Беспилотное вкусное средство'
      ]
    },
    {
      question: 'Что такое БВС?',
      options: [
        'Беспилотное воздушное средство',
        'Беспилотное водное средство',
        'Беспилотное ветряное средство',
        'Беспилотное вкусное средство'
      ]
    },
    {
      question: 'Что такое БВС?',
      options: [
        'Беспилотное воздушное средство',
        'Беспилотное водное средство',
        'Беспилотное ветряное средство',
        'Беспилотное вкусное средство'
      ]
    }
  ])
  
  // Ответы будут храниться в массиве (по индексу совпадают с вопросами)
  const answers = ref(Array(questions.value.length).fill([]))
</script>
  
<style>

.close-button {
  position: absolute;
  top: 12px;
  right: 12px;
  background: #ff3333;
  color: transparent;
  cursor: pointer;
  appearance: none;
  width: var(--kruglik);
  height: var(--kruglik);
  border: 1px solid var(--bg);
  border-radius: 50%;
}

.kunt {
  background: var(--bg);
  max-height: 75vh;
  overflow-y: auto;
  padding-right: 10px;
  scrollbar-gutter: stable;
}

.kunt::-webkit-scrollbar {
  overflow-y: visible;
  width: 14px;
}

.kunt::-webkit-scrollbar-track {
  background: transparent;
}

.kunt::-webkit-scrollbar-thumb {
  background-color: var(--border);
  border-radius: 15px;
  border: 4px solid var(--bg);
}

.kunt::-webkit-scrollbar-thumb:hover {
  background-color: #aa33ff;
}

.test-card {
  position: relative;
  font-family: 'Unbounded', sans-serif;
  background: var(--border);
  color: var(--bg);
  border-radius: 12px;
  padding: 20px;
  /* width: 100%;  */
  /* max-height: 90vh; */
}

h2 {
  font-weight: 800;
  font-size: 20px;
  margin-bottom: 15px;
}

.text-input {
  margin-top: 10px;
  width: 100%;
  padding: 6px;
  font-size: 14px;
  border-radius: 5px;
  border: 2px solid var(--border);
  outline: none;
}

.text-input:focus {
  border-color: #aa33ff;
  box-shadow: 0 0 0 2px rgba(136, 0, 204, 0.2);
}

</style>