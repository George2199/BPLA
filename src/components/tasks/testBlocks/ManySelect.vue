<template>
  <div class="question-block">
    <p><strong>{{ question }}</strong></p>
    <label
      v-for="(option, index) in options"
      :key="index"
      class="option"
      :style="{
        '--bg': background_color,
        '--border': border_color,
        '--text': text_color,
        '--kruglik': kruglik_size,
      }"
    >
    <input
      type="checkbox"
      :value="index"
      :checked="modelValue.includes(index)"
      @change="onChange(index, $event)"
    />

      {{ option }}
    </label>
  </div>
  
</template>

<script setup>

import {inject} from 'vue'
const background_color = inject('background_color')
const border_color = inject('border_color')
const text_color = inject('text_color')
const kruglik_size = inject('kruglik_size')

const props = defineProps({
  question: String,
  options: Array, // простой массив строк
  modelValue: Array,

})

const emit = defineEmits(['update:modelValue'])

function onChange(index, event) {
  const wasChecked = props.modelValue.includes(index)
  const checked = event.target.checked

  let newValue = []

  if (checked && !wasChecked) {
    newValue = [...props.modelValue, index]
  } else if (!checked && wasChecked) {
    newValue = props.modelValue.filter(i => i !== index)
  } else {
    newValue = [...props.modelValue] // без изменений
  }

  emit('update:modelValue', newValue)
}

</script>

<style scoped>

.question-block{
  font-family: 'Unbounded', sans-serif;
  font-weight:700 !important;
  margin-bottom: 10px;
  color: var(--text);
  padding: 10px;
  border-radius: 8px;
}
.question-block strong {
  font-weight: 700;
  }

label {
    font-weight: 300;
  }

.option {
  color: var(--text);
  display: flex;
  align-items: baseline;
  gap: 10px;
  font-size: 15px;
  font-weight: 300;
  margin: 8px 0;
  line-height: 1.4;
}

input[type="checkbox"] {
  appearance: none;
  width: var(--kruglik);
  height: var(--kruglik);
  border: 2px solid var(--border);
  border-radius: 50%;
  background-color: var(--bg);
  cursor: pointer;
  position: relative;
  flex-shrink: 0;
  margin-top: 2px; /* ← немного опустить, чтобы ровно совпало с первой строкой */
}

input[type="checkbox"]:checked {
  background-color: var(--border); /* ← вот тут можно менять цвет внутри кружка */
}
</style>