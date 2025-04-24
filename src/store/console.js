// src/store/console.js

import { ref } from 'vue'

export const consoleOutput = ref('')
export const consoleVisible = ref(false)

export function toggleConsole() {
  consoleVisible.value = !consoleVisible.value
}
