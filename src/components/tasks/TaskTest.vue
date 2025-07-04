<template>
  <div class="test-card">
    <h2>{{ task?.title || 'Тест' }}</h2>
    <div class="kunt">
      <ManySelect
        v-for="(q, i) in questions"
        :key="i"
        :question="q.question_text"
        :options="q.options"
        :model-value="answers[i]"
        @update:model-value="val => answers[i] = val"
      />
      <div class="under_kunt_for_button">
        <button class="submit-btn" :disabled="!canSubmit" @click="submitTest">Сдать</button>
      </div>
    </div>

    <div v-if="result">
      <p class="result_p">Результат: {{ result.score }} из {{ result.total }}</p>
      <p class="result_p">Прогресс: {{ (result.progress * 100).toFixed(0) }}%</p>
      <div class="progress-bar">
        <div class="progress-fill" :style="{ width: (result.progress * 100) + '%' }"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import ManySelect from './testBlocks/ManySelect.vue'
import api from '@/api'

const result = ref(null)

const props = defineProps({
  task: {
    type: Object,
    required: true
  }
})

const questions = ref([])
const answers = ref([])

watch(
  () => props.task,
  (newTask) => {
    if (newTask?.test?.questions) {
      questions.value = newTask.test.questions.map(q => ({
        question_text: q.question_text,
        options: q.options.map(opt => ({ id: opt.id, text: opt.text }))
      }))
      answers.value = questions.value.map(() => [])
    }
  },
  { immediate: true }
)


const canSubmit = computed(() =>
  answers.value.some(a => Array.isArray(a) && a.length > 0)
)

async function submitTest() {
  try {
    const response = await api.post('/submit_test', {
      answers: answers.value,
      task_id: props.task.id
    })
    result.value = response.data
    await refreshCourses()
  } catch (err) {
    alert("Ошибка при отправке теста")
    console.error(err)
  }
}

async function refreshCourses() {
  try {
    const res = await api.get('/courses')
    courses.value = res.data
  } catch (e) {
    console.error('❌ Не удалось обновить курсы:', e)
  }
}
</script>

  
  
<style scoped>

.progress-bar {
  width: 100%;
  height: 12px;
  background: #eee;
  border-radius: 6px;
  overflow: hidden;
  margin-top: 10px;
}

.progress-fill {
  height: 100%;
  background: #7000cc;
  transition: width 0.3s ease;
}


.submit-btn {
  position: absolute;
  bottom: 15px;
  right: 0px;

  background: var(--grad_color_right);
  color: white;
  font-weight: bold;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  padding: 10px 20px;
}

.submit-btn:disabled {
  background: #aaa;       /* посерее фон */
  cursor: not-allowed;    /* курсор с крестиком */
  opacity: 0.7;           /* немного тусклее */
}

.close-button {
  position: absolute;
  top: 12px;
  right: 12px;
  background: #ff3333;
  color: transparent;
  cursor: pointer;
  appearance: none;
  width: var(--kruglik_size);
  height: var(--kruglik_size);
  border: 1px solid var(--background_color);
  border-radius: 50%;
}

.under_kunt_for_button {

  height:20px;
  color: transparent;
  position: relative;
}

.kunt {
  flex: 1;
  background: var(--background_color);
  overflow-y: auto;
  padding-right: 10px;
  scrollbar-gutter: stable;
  position: relative;
}


.kunt::-webkit-scrollbar {
  overflow-y: visible;
  width: 14px;
}

.kunt::-webkit-scrollbar-track {
  background: transparent;
}

.kunt::-webkit-scrollbar-thumb {
  background-color: var(--border_color);
  border-radius: 15px;
  border: 4px solid var(--background_color);
}

.kunt::-webkit-scrollbar-thumb:hover {
  background-color: #aa33ff;
}

.test-card {
  position: relative;
  background: transparent;
  color: var(--background_color);
  padding-top: 24px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

h2 {
  font-weight: 800;
  font-size: 20px;
  margin-bottom: 15px;
  margin-top: 0px;
  text-align: center;
}

.text-input {
  margin-top: 10px;
  width: 100%;
  padding: 6px;
  font-size: 14px;
  border-radius: 5px;
  border: 2px solid var(--border_color);
  outline: none;
}

.text-input:focus {
  border-color: #aa33ff;
  box-shadow: 0 0 0 2px rgba(136, 0, 204, 0.2);
}

.result_p {
  padding-left: 15px;
}
</style>