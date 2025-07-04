<template>
  <div class="task-block-container" @keydown="handleKey" tabindex="0">
    <p class="description" v-if="task?.block_task?.description">
      {{ task.block_task.description }}
    </p>

    <div class="blocks-wrapper">
      <!-- ОТВЕТ -->
      <div class="section answer-section">
        <draggable
          v-model="answerBlocks"
          class="block-list highlighted"
          group="blocks"
          item-key="id"
        >
          <template #item="{ element }">
            <BlockItem
              :element="element"
              :selectedBlockId="selectedBlockId"
              :selectedFromAnswer="selectedFromAnswer"
              @selectBlock="selectBlock"
              fromAnswer
            />
          </template>
        </draggable>
      </div>

      <!-- ИСХОДНИКИ -->
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
            <BlockItem
              :element="element"
              :selectedBlockId="selectedBlockId"
              :selectedFromAnswer="selectedFromAnswer"
              @selectBlock="selectBlock"
            />
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
import api from '@/api'
import { ref, watch } from 'vue'
import draggable from 'vuedraggable'
import { consoleOutput, showConsole } from '@/store/console'
import BlockItem from './blockBlocks/BlockItem.vue'

// ====== ПЕРЕМЕННЫЕ ======
const props = defineProps({ task: Object })
const originalBlocks = ref([])
const shuffledBlocks = ref([])
const answerBlocks = ref([])
const selectedBlockId = ref(null)
const selectedFromAnswer = ref(true)
const isRunning = ref(false)

// ====== ВСПОМОГАТЕЛЬНЫЕ ======
function generateId() {
  return '_' + Math.random().toString(36).substr(2, 9)
}

const cloneBlock = (original) => {
  const clone = {
    ...original,
    id: generateId(),
    indentLevel: original.indentLevel ?? 0
  }

  if (clone.type === 'container' && Array.isArray(clone.children)) {
    clone.children = clone.children.map(child => cloneBlock(child))
  }

  return clone
}

const prepareBlock = (block, level = 0) => {
  const newBlock = {
    ...block,
    id: generateId(),
    indentLevel: level,
    type: block.type,
    content: block.type === 'code' ? block.cat : undefined,
    label: block.type === 'container' ? block.cat : undefined,
    children: []
  }
  return newBlock
}

const buildTree = (flatBlocks) => {
  const idToBlock = {}
  flatBlocks.forEach(raw => {
    const block = prepareBlock(raw)
    idToBlock[raw.id] = block
  })

  const rootBlocks = []

  flatBlocks.forEach(raw => {
    const block = idToBlock[raw.id]
    const parent = raw.parent_id ? idToBlock[raw.parent_id] : null
    if (parent && parent.type === 'container') {
      parent.children = parent.children || []
      parent.children.push(block)
    } else {
      rootBlocks.push(block)
    }
  })

  return rootBlocks
}

// ====== РЕАКТИВНАЯ ЗАГРУЗКА БЛОКОВ ======
watch(
  () => props.task,
  (newTask) => {
    const rawBlocks = newTask?.block_task?.blocks || []
    const tree = buildTree(rawBlocks)
    originalBlocks.value = tree
    shuffledBlocks.value = [...tree].sort(() => Math.random() - 0.5)
    answerBlocks.value = []
    selectedBlockId.value = null
    selectedFromAnswer.value = true
  },
  { immediate: true }
)

// ====== ОБРАБОТКА ВЫБОРА ======
const selectBlock = (id, fromAnswer = true) => {
  selectedBlockId.value = id
  selectedFromAnswer.value = fromAnswer
}

const findBlockAndParent = (blocks, id) => {
  for (let i = 0; i < blocks.length; i++) {
    const block = blocks[i]
    if (block.id === id) {
      return { parent: blocks, index: i }
    }
    if (block.type === 'container' && block.children) {
      const res = findBlockAndParent(block.children, id)
      if (res) return res
    }
  }
  return null
}

// ====== КЛАВИШИ И НАВИГАЦИЯ ======
const handleKey = (event) => {
  if (!selectedBlockId.value) return

  const fromAnswer = selectedFromAnswer.value
  const blocksRoot = fromAnswer ? answerBlocks.value : shuffledBlocks.value
  const result = findBlockAndParent(blocksRoot, selectedBlockId.value)

  if (!result) return

  const { parent: currentList, index } = result

  if (index === -1) return

  const isAlt = event.altKey
  const isShift = event.shiftKey

  const moveSelection = (direction) => {
    const newIndex = index + direction
    if (newIndex >= 0 && newIndex < currentList.length) {
      selectedBlockId.value = currentList[newIndex].id
    }
  }

  const moveBlock = (direction) => {
    const newIndex = index + direction
    if (newIndex >= 0 && newIndex < currentList.length) {
      const temp = currentList[index]
      currentList.splice(index, 1)
      currentList.splice(newIndex, 0, temp)
      selectedBlockId.value = temp.id
    }
  }

  const transferBlock = (toAnswer) => {
    const source = fromAnswer ? answerBlocks.value : shuffledBlocks.value
    const target = fromAnswer ? shuffledBlocks.value : answerBlocks.value

    const [moved] = source.splice(index, 1)
    if (!moved) return

    target.push(moved)
    selectedBlockId.value = moved.id
    selectedFromAnswer.value = toAnswer
  }

  // ALT + стрелки: перенос и перемещение
  if (isAlt) {
    if (event.key === 'ArrowUp') return event.preventDefault(), moveBlock(-1)
    if (event.key === 'ArrowDown') return event.preventDefault(), moveBlock(1)
    if (event.key === 'ArrowRight' && fromAnswer) return event.preventDefault(), transferBlock(false)
    if (event.key === 'ArrowLeft' && !fromAnswer) return event.preventDefault(), transferBlock(true)
  }

  // Просто навигация
  if (event.key === 'ArrowUp') return event.preventDefault(), moveSelection(-1)
  if (event.key === 'ArrowDown') return event.preventDefault(), moveSelection(1)
  if (event.key === 'ArrowLeft') {
    event.preventDefault()
    if (!fromAnswer && answerBlocks.value.length > 0) {
      selectedBlockId.value = answerBlocks.value[0].id
      selectedFromAnswer.value = true
    }
    return
  }
  if (event.key === 'ArrowRight') {
    event.preventDefault()
    if (fromAnswer && shuffledBlocks.value.length > 0) {
      selectedBlockId.value = shuffledBlocks.value[0].id
      selectedFromAnswer.value = false
    }
    return
  }

  // Tab/Shift+Tab для отступов
  if (event.key === 'Tab' && fromAnswer) {
    event.preventDefault()
    const block = currentList[index]
    if (block) {
      isShift ? decreaseIndent(block) : increaseIndent(block)
    }
  }

  // ENTER = запуск
  if (event.key === 'Enter') {
    event.preventDefault()
    runCode()
  }
}

const increaseIndent = (block) => {
  if (block.indentLevel < 10) block.indentLevel++
}
const decreaseIndent = (block) => {
  if (block.indentLevel > 0) block.indentLevel--
}

// ====== ЗАПУСК КОДА ======
const runCode = async () => {
  const buildCode = (blocks, baseIndent = 0) => {
    let lines = []
    for (const block of blocks) {
      if (block.type === 'code') {
        lines.push('    '.repeat(baseIndent + (block.indentLevel || 0)) + block.content)
      } else if (block.type === 'container') {
        lines.push('    '.repeat(baseIndent + (block.indentLevel || 0)) + block.label)
        if (Array.isArray(block.children)) {
          lines.push(...buildCode(block.children, baseIndent + 1))
        }
      }
    }
    return lines
  }

  const code = buildCode(answerBlocks.value).join('\n')

  if (!code.trim()) {
    consoleOutput.value = '⚠️ нет кода для запуска.'
    return
  }

  try {
    isRunning.value = true
    consoleOutput.value = ''
    const response = await api.post('/execute', { code, task_id: props.task.id })
    const { output, tests_output } = response.data
    consoleOutput.value = (output || '') + (tests_output ? '\n' + tests_output : '') || '✅ код выполнен.'
  } catch (error) {
    consoleOutput.value = `❌ ошибка:\n${error.response?.data?.error || error.message}`
  } finally {
    isRunning.value = false
    showConsole()
  }
}
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

.code-block-wrapper.selected,
.code-block.selected {
  background: #535c70;
}

</style>