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
            <div class="code-block">{{ element.content }}</div>
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
            <div class="code-block">{{ element.content }}</div>
          </template>
        </draggable>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref, onMounted } from 'vue'
  import draggable from 'vuedraggable'

  const props = defineProps({
    task: Object
  })

  function generateId() {
    return '_' + Math.random().toString(36).substr(2, 9)
  }

  const originalBlocks = ref([])

  onMounted(() => {
    const blocks = props.task?.content?.blocks || []
    // Добавляем id каждому блоку
    originalBlocks.value = blocks.map(block => ({
      ...block,
      id: generateId()
    }))
    shuffledBlocks.value = [...originalBlocks.value].sort(() => Math.random() - 0.5)
  })

  const shuffledBlocks = ref([])
  const answerBlocks = ref([])

  const cloneBlock = (original) => ({ ...original })
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
  gap: 8px;
  min-height: 100px;
  background: transparent;
  padding: 10px;
  border-radius: 8px;
}

.code-block {
  font-family: monospace;
  background: transparent;
  padding: 10px;
  border-radius: 6px;
  border: 1px solid #ccc;
  cursor: grab;
  white-space: pre;
}
</style>
