<template>
  <ManySelect
    question="Что такое БВС?"
    :options="[
      'Беспилотное воздушное средство',
      'Беспилотное водное средство',
      'Беспилотное ветряное средство',
      'Беспилотное вкусное средство'
    ]"
    v-model="answer1"
  />

  <test1/>
</template>

<script setup>
import test1 from './components/Tests.vue';
</script>./components/ManySelect.vue
