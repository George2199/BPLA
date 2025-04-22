<template>
    <div class="test-card" :style="{
      '--bg': background_color,
      '--border': border_color,
      '--text': text_color,
      '--kruglik': kruglik_size,
    }">
  
      <h2>{{ task?.title || 'Тест' }}</h2>
      <div class="kunt">

        <ManySelect
          v-for="(q, i) in questions"
          :key="i"
          :question="q.question"
          :options="q.options"
          v-model="answers[i]"
          :background_color="background_color"
          :border_color="border_color"
          :text_color="text_color"
          :kruglik_size="kruglik_size"
        />
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, watch } from 'vue'
  import ManySelect from './testBlocks/ManySelect.vue'
  
  const props = defineProps({
    task: {
      type: Object,
      required: true
    }
  })
  
  const background_color = "#ffffff"
  const border_color = "#8800cc"
  const text_color = "#000000"
  const kruglik_size = "16px"
  
  const visible = ref(true)
  const questions = ref([])
  const answers = ref([])
  
  watch(
    () => props.task,
    (newTask) => {
      if (newTask?.content?.questions) {
        questions.value = newTask.content.questions
        answers.value = Array(questions.value.length).fill([])
      }
    },
    { immediate: true }
  )
  </script>
  
  
<style>

.kunt {
  flex: 1;
  background: var(--bg);
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
  
  background: transparent;
  color: var(--bg);

  padding: 24px 32px;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
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