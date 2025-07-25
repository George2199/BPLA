<template>
  <div class="question-block">
    <p><strong>{{ question }}</strong></p>
    <div class="options-container">
      <label
        v-for="(option, index) in options"
        :key="option.id"
        class="option"
        :class="{ 'selected': modelValue.includes(option.id) }"
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
  </div>
</template>

<script setup>
const props = defineProps({
  question: String,
  options: Array,
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
    newValue = [...props.modelValue]
  }

  emit('update:modelValue', newValue)
}
</script>

<style scoped>
.question-block {
  font-family: 'Unbounded', sans-serif;
  font-weight: 700;
  font-size: 100;
  padding: 10px;
  max-width: 300px; /* Ограничиваем ширину блока */
}

.options-container {
  display: flex;
  width:120%;
  flex-direction: column; /* Варианты вертикально */
  gap: 10px; /* Отступ между вариантами */
}

.option {
  color: white;
  display: flex;
  align-items: center;
  font-size: 15px;
  font-weight: 300;
  padding: 10px;
  border: 1px solid white;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.option:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.option.selected {
  border-color: #CDBDF5;
  background-color: rgba(205, 189, 245, 0.1);
}

input[type="checkbox"] {
  appearance: none;
  width: 1px;
  height: 1px;
  margin-right: 8px; /* Отступ от текста */
}
</style>