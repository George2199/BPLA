<template>
    <div class="question-block">
      <p><strong>{{ question }}</strong></p>
      <label
        v-for="(option, i) in options"
        :key="i"
        class="option"
        :style="{
          '--bg': background_color,
          '--border': border_color,
          '--text': text_color,
          }"
      >
        <input
          type="checkbox"
          :value="option"
          :checked="(modelValue || []).includes(option)"
          @change="onChange(option, $event)"
          class="option"
        />
        {{ option }}
      </label>
    </div>
  </template>
  
  <script setup>
  const props = defineProps({
    question: String,
    options: Array,
    modelValue: Array,
    background_color: {
      type: String,
      default: '#ffffff'
    },
    border_color: {
      type: String,
      default: '#8800cc'
    },
    text_color: {
      type: String,
      default: '#000000'
    },
  })
  
  const emit = defineEmits(['update:modelValue'])
  
  function onChange(option, event) {
    const newValue = [...props.modelValue]
    if (event.target.checked) {
      newValue.push(option)
    } else {
      const index = newValue.indexOf(option)
      if (index > -1) newValue.splice(index, 1)
    }
    emit('update:modelValue', newValue)
  }
  </script>
<style scoped>

.question-block{
  font-family: 'Unbounded', sans-serif;
  font-weight:700 !important;
  margin-bottom: 20px;
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
  width: 16px;
  height: 16px;
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