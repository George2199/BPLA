<template>
 <div class="container">
  <router-link :to="{ name: 'tasks' }" class="card">
    <img class="card-image" :src="pythonImg" alt="Python">
    <div class="card-text">Python. Введение</div>
  </router-link>

  <div class="card">
    <img class="card-image" :src="cosmosImg" alt="Cosmos">
    <div class="card-text">Аэрокосмос</div>
  </div>

  <div class="card">
    <img class="card-image" :src="dronImg" alt="Dron">
    <div class="card-text">Управление БПЛА</div>
  </div>
 </div>
</template>

<script setup>
import pythonImg from '@/components/pics/Питон.png';
import cosmosImg from '@/components/pics/Космос.png';
import dronImg from '@/components/pics/Дрон.png';
</script>

<style>
.container {
    display: flex;
    flex-wrap: wrap;
    gap: 80px; /* Расстояние между блоками */
    max-width: 2000px; /* Ограничение ширины, чтобы влезало 3 блока */
    margin-left:  50px; 
    margin-top:  30px;
}

.card {
    width: 370px; /* или под нужный размер */
    border: 1px solid #9c9c9c;
    border-radius: 8px;
    overflow: hidden; /* чтобы изображение не выходило за границы */
    font-family: Arial, sans-serif;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* легкая тень */
    cursor: pointer;
    transition: transform 0.2s;
    text-decoration: none;
    color: inherit;
}
.card:hover {
    transform: scale(1.02);
}

.card-image {
    width: 100%;
    height: auto;
    display: block;
}

.card-text {
    padding: 4px;
    font-size: 22px;
    letter-spacing: 2px;
    font-weight:lighter;
    text-align: center;
    color: #333;
    background: #D8D7FF;
    border-top: 1px solid #000000;
}
</style>