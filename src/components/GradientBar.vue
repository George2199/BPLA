<template>
  <div class="gradientbar">
    <h2>Аэрокосмос</h2>
    <button v-for="(icon, index) in icons" :key="index" class="gradientbar-button">
      <img :src="icon" alt="Icon" class="gradientbar-icon" />
    </button>
  </div>
</template>

<script setup>
</script>

<style>
/* 📌 Sidebar */
.gradientbar {
  width: 55vw;
  height: 100vh;
  background: linear-gradient(0deg, #5F0F7A, #000000);
  display: flex;
  float: left;
  flex-direction: column;
  align-items: center;
  padding: 15px 0;
  position: fixed;
  z-index: -1;
  top: 0;
  left: 0;
}
h2 {
  font-size: 60px;
  margin-top: 290px;
  margin-right: 30px;
  color: white;
}
</style>
