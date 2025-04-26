<template>
    <div v-if="element.type === 'code'"
      class="code-block"
      :class="[
        fromAnswer ? 'yellow-border' : 'white-border',
        { selected: selectedBlockId === element.id && (fromAnswer ? selectedFromAnswer : !selectedFromAnswer) }
      ]"
      @click="() => selectBlock(element.id, fromAnswer)"
    >
      <div class="code-text">
        {{ '\u00A0\u00A0\u00A0\u00A0'.repeat(element.indentLevel) + element.content }}
      </div>
    </div>
  
    <div v-else-if="element.type === 'container'" class="container-block">
        <div
            class="container-header"
            :class="{ selected: selectedBlockId === element.id && (fromAnswer ? selectedFromAnswer : !selectedFromAnswer) }"
            @click="() => selectBlock(element.id, fromAnswer)"
        >
            {{ '\u00A0\u00A0\u00A0\u00A0'.repeat(element.indentLevel) + element.label }}
        </div>
        <draggable
            v-model="element.children"
            group="blocks"
            item-key="id"
            class="inner-draggable"
        >
            <template #item="{ element: child }">
            <BlockItem
                :element="child"
                :selectedBlockId="selectedBlockId"
                :selectedFromAnswer="selectedFromAnswer"
                @selectBlock="selectBlock"
                :fromAnswer="fromAnswer"
            />
            </template>
        </draggable>
    </div>

  </template>
  
  <script setup>
  import { defineProps, defineEmits } from 'vue'
  import draggable from 'vuedraggable'
  
  const props = defineProps({
    element: Object,
    selectedBlockId: Object,
    selectedFromAnswer: Object,
    fromAnswer: {
      type: Boolean,
      default: false
    }
  })
  
  const emit = defineEmits(['selectBlock'])
  
  const selectBlock = (id, fromAnswer) => {
    emit('selectBlock', id, fromAnswer)
  }
  </script>
  
  <style scoped>
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
}

.white-border {
  border-color: #ffffff;
}

.yellow-border {
  border-color: #db9410;
}

.container-block {
  background: #444;
  border: 2px dashed #aaa;
  border-radius: 12px;
  margin: 10px 0;
  padding: 10px;
}

.container-header {
  font-weight: bold;
  font-size: 14px;
  margin-bottom: 8px;
  pointer-events: none; /* ЧТОБЫ ЗАГОЛОВОК НЕ БЫЛ DRAGGABLE */
  user-select: none;
}

.inner-draggable {
  display: flex;
  flex-direction: column;
  gap: 8px; /* <<< ЭТО margin между вложенными блоками */
  min-height: 50px;
  background: #555;
  border-radius: 8px;
  padding: 10px;
}

</style>
  