<template>
  <div class="task-block-container" @keydown="handleKey" tabindex="0">
    <p class="description" v-if="task?.content?.description">
      {{ task.content.description }}
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
import { ref, onMounted } from 'vue'
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
    indentLevel: level
  }
  if (block.type === 'container' && Array.isArray(block.children)) {
    newBlock.children = block.children.map(child => prepareBlock(child, level + 1))
  }
  return newBlock
}

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

// ====== ЛОГИЧЕСКИЕ ======
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

  console.log('👉 handleKey', {
    key: event.key,
    alt: isAlt,
    shift: isShift,
    ctrl: event.ctrlKey,
    selectedBlockId: selectedBlockId.value,
    selectedFromAnswer: selectedFromAnswer.value,
    currentList,
  })

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

    console.log('💣 TRANSFER START')
    console.log('source:', source)
    console.log('target:', target)
    console.log('selected index:', index)
    console.log('selected id:', selectedBlockId.value)

    if (!Array.isArray(source) || !Array.isArray(target)) {
      console.error('🔥 source или target НЕ массивы', { source, target })
      return
    }

    const [moved] = source.splice(index, 1)
    if (!moved) {
      console.error('❌ НИЧЕГО НЕ ПЕРЕМЕСТИЛОСЬ')
      return
    }

    target.push(moved)
    selectedBlockId.value = moved.id
    selectedFromAnswer.value = toAnswer

    console.log('✅ TRANSFER SUCCESS')
    console.log('new source:', source)
    console.log('new target:', target)
  }

  // =================== ALT-логика ===================
  if (isAlt) {
    if (event.key === 'ArrowUp') {
      event.preventDefault()
      moveBlock(-1)
      return
    }
    if (event.key === 'ArrowDown') {
      event.preventDefault()
      moveBlock(1)
      return
    }
    if (event.key === 'ArrowRight') {
      event.preventDefault()
      if (fromAnswer) transferBlock(false)
      return
    }
    if (event.key === 'ArrowLeft') {
      event.preventDefault()
      if (!fromAnswer) transferBlock(true)
      return
    }
  }

  // =================== Навигация ===================
  if (event.key === 'ArrowUp') {
    event.preventDefault()
    moveSelection(-1)
    return
  }
  if (event.key === 'ArrowDown') {
    event.preventDefault()
    moveSelection(1)
    return
  }
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

  // =================== Tabulation (только для ответа) ===================
  if (event.key === 'Tab' && fromAnswer) {
    event.preventDefault()
    const block = currentList[index]
    if (block) {
      if (isShift) {
        decreaseIndent(block)
      } else {
        increaseIndent(block)
      }
    }
  }

  // =================== ENTER — Запуск кода ===================
  if (event.key === 'Enter') {
    event.preventDefault()
    runCode()
    return
  }
}

const increaseIndent = (block) => {
  if (block.indentLevel < 10) block.indentLevel++
}
const decreaseIndent = (block) => {
  if (block.indentLevel > 0) block.indentLevel--
}

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

// ====== INIT ======
onMounted(async () => {
  const blocks = props.task?.content?.blocks || []
  originalBlocks.value = blocks.map(b => prepareBlock(b))
  shuffledBlocks.value = [...originalBlocks.value].sort(() => Math.random() - 0.5)
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

.code-block-wrapper.selected,
.code-block.selected {
  background: #535c70;
}

</style>
