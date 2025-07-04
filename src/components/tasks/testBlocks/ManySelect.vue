<template>
  <div class="question-block">
    <p><strong>{{ question }}</strong></p>
    <label
      v-for="(option, index) in options"
      :key="option.id"
      class="option"
    >
    <input
      type="checkbox"
      :value="option.id"
      :checked="modelValue.includes(option.id)"
      @change="onChange(option.id, $event)"
    />

      {{ option.text }}
    </label>
  </div>
  
</template>

<script setup>
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
  color: var(--text_color);
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
  color: var(--text_color);
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
  width: var(--kruglik_size);
  height: var(--kruglik_size);
  border: 2px solid var(--border_color);
  border-radius: 50%;
  background-color: var(--background_color);
  cursor: pointer;
  position: relative;
  flex-shrink: 0;
  margin-top: 2px; /* ← немного опустить, чтобы ровно совпало с первой строкой */
}

input[type="checkbox"]:checked {
  background-color: var(--border_color); /* ← вот тут можно менять цвет внутри кружка */
}
</style>