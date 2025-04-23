<template>
  <div class="task-block-container">
    <div class="blocks-wrapper">
      <!-- Сборка (влево) -->
      <div class="section">
        <p class="description" v-if="task?.content?.description">{{ task.content.description }}</p>
        <draggable
          v-model="answerBlocks"
          class="block-list"
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
        <h3>Фрагменты кода</h3>
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

    <!-- Кнопка запуска -->
    <button @click="runCode" class="run-button" :disabled="isRunning">
      ▶ {{ isRunning ? 'Запуск...' : 'Запустить' }}
    </button>

    <!-- Вывод результата -->
    <pre class="output">{{ output }}</pre>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import draggable from 'vuedraggable'

const props = defineProps({
  task: Object
})

const originalBlocks = ref([])
const shuffledBlocks = ref([])
const answerBlocks = ref([])
const output = ref('')
const isRunning = ref(false)
const pyodide = ref(null)

function generateId() {
  return '_' + Math.random().toString(36).substr(2, 9)
}

const cloneBlock = (original) => ({ ...original })

const runCode = async () => {
  if (!pyodide.value) {
    try {
      pyodide.value = await window.loadPyodide({
        indexURL: '/pyodide/'
      })
    } catch (err) {
      output.value = '❌ Ошибка загрузки Pyodide: ' + err
      return
    }
  }

  const code = answerBlocks.value.map(b => b.content).join('\n')

  if (!code.trim()) {
    output.value = '⚠️ Нет кода для запуска.'
    return
  }

  try {
    isRunning.value = true
    output.value = '' // очистим вывод

    // 🔄 Перенаправляем stdout и stderr
    pyodide.value.setStdout({ batched: (s) => output.value += s + '\n' })
    pyodide.value.setStderr({ batched: (s) => output.value += '❌ ' + s + '\n' })

    await pyodide.value.runPythonAsync(code)

    if (!output.value.trim()) {
      output.value = '✅ Код выполнен.'
    }

  } catch (err) {
    output.value = `❌ Ошибка:\n${err}`
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
})
</script>

<style scoped>
.task-block-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.blocks-wrapper {
  display: flex;
  justify-content: space-between;
  gap: 40px;
  align-items: flex-start;
}

.description {
  font-size: 16px;
  margin-bottom: 12px;
  color: #eee;
  font-style: italic;
}

.section {
  flex: 1;
  background: transparent;
  padding: 16px;
  border-radius: 8px;
}

.block-list {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 8px;
  min-height: 100px;
  background: #3a3a3aee;
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #ffffff;
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
  border-radius: 6px;
  cursor: pointer;
  margin-top: 16px;
}

.run-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.output {
  background: #222;
  color: #0f0;
  padding: 12px;
  border-radius: 8px;
  margin-top: 12px;
  min-height: 60px;
  white-space: pre-wrap;
}
</style>
