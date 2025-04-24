<template>
  <div class="task-block-container">
    <!-- 📄 Описание (над блоками) -->
    <p class="description" v-if="task?.content?.description">
      {{ task.content.description }}
    </p>

    <!-- Блоки: сборка и фрагменты -->
    <div class="blocks-wrapper">

      <!-- Сборка (влево) -->
      <div class="section answer-section">
        <draggable
          v-model="answerBlocks"
          class="block-list highlighted"
          group="blocks"
          item-key="id"
        >
          <template #item="{ element }">
            <div class="code-block yellow-border">{{ element.content }}</div>
          </template>
        </draggable>
      </div>

      <!-- Исходные фрагменты (вправо) -->
      <div class="section">
        <draggable
          :list="shuffledBlocks"
          class="block-list"
          group="blocks"
          item-key="id"
          :clone="cloneBlock"
          :sort="false"
        >
          <template #item="{ element }">
            <div class="code-block white-border">{{ element.content }}</div>
          </template>
        </draggable>
      </div>
    </div>

      <button @click="runCode" class="run-button" :disabled="isRunning">
        ▶ {{ isRunning ? 'Запуск...' : 'Запустить' }}
      </button>
  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import draggable from 'vuedraggable'
import { consoleOutput } from '@/store/console'

const props = defineProps({
  task: Object
})

const originalBlocks = ref([])
const shuffledBlocks = ref([])
const answerBlocks = ref([])
const isRunning = ref(false)

// ✅ Используем глобальный кэш
const pyodide = ref(window.__pyodide || null)
const pyodideReady = ref(!!window.__pyodide)

function generateId() {
  return '_' + Math.random().toString(36).substr(2, 9)
}

const cloneBlock = (original) => ({ ...original })

const initPyodide = async () => {
  if (window.__pyodide) return // 🔁 Уже загружено

  try {
    consoleOutput.value = '⏳ Загружаем Pyodide...'
    const instance = await window.loadPyodide({ indexURL: '/pyodide/' })
    window.__pyodide = instance
    pyodide.value = instance
    pyodideReady.value = true
    consoleOutput.value = '✅ Pyodide готов!'
  } catch (err) {
    consoleOutput.value = '❌ Ошибка загрузки Pyodide: ' + err
  }
}

const runCode = async () => {
  if (!pyodideReady.value) {
    consoleOutput.value = '⚠️ Pyodide ещё не готов.'
    return
  }

  const code = answerBlocks.value.map(b => b.content).join('\n')

  if (!code.trim()) {
    consoleOutput.value = '⚠️ Нет кода для запуска.'
    return
  }

  try {
    isRunning.value = true
    consoleOutput.value = ''

    pyodide.value.setStdout({ batched: (s) => consoleOutput.value += s + '\n' })
    pyodide.value.setStderr({ batched: (s) => consoleOutput.value += '❌ ' + s + '\n' })

    await pyodide.value.runPythonAsync(code)

    if (!consoleOutput.value.trim()) {
      consoleOutput.value = '✅ Код выполнен.'
    }

  } catch (err) {
    consoleOutput.value = `❌ Ошибка:\n${err}`
  } finally {
    isRunning.value = false
  }
}

onMounted(() => {
  const blocks = props.task?.content?.blocks || []
  originalBlocks.value = blocks.map(block => ({
    ...block,
    id: generateId()
  }))
  shuffledBlocks.value = [...originalBlocks.value].sort(() => Math.random() - 0.5)

  // 🔥 Стартуем подгрузку
  initPyodide()
})
</script>


<style scoped>
.task-block-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding: 16px;
}

.blocks-wrapper {
  display: flex;
  justify-content: space-between;
  gap: 40px;
  align-items: stretch;
}

.description {
  font-size: 16px;
  margin-bottom: 12px;
  color: #eee;
  font-style: italic;
}

.section {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.block-list {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
  background: #3a3a3aee;
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #ffffff;
  min-height: 100px;
}


.code-block {
  font-family: monospace;
  background: transparent;
  padding: 10px;
  border-radius: 6px;
  border: 1px solid;
  cursor: grab;
  white-space: pre;
  width: fit-content;
  max-width: 100%;
  box-sizing: border-box;
}

.white-border {
  border-color: #ffffff;
}

.yellow-border {
  border-color: #db9410;
}

.run-button {
  padding: 10px 20px;
  font-size: 16px;
  background: #ffeb3b;
  color: #000;
  border: none;
  /* border: 1px solid #000; */
  border-radius: 6px;
  cursor: pointer;
  width: 100%;
}

.run-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.block-list.highlighted {
  border-color: #db9410; /* Жёлтая рамка только для левой секции */
}
</style>
