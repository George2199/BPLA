
<template>
  
  <!-- <TatliStarts /> -->

  <div class="aerocos">АэроКосмос</div>
    
  <p class="quote">
  «И пусть говорит кто-то: безумцы, мы говорим: гении. Ведь только безумец верит,
  что может изменить мир, — и потому лишь меняет его».

</p>
<div class="auth-wrapper">
  <form @submit.prevent="handleSubmit">
          <h1 class="auth-title">Авторизация</h1>
          <!-- пароль -->
    <div class="form-group">


      <input type="text" placeholder="Логин" id="login" v-model="login" required />
    </div>
          <div class="form-group pw-wrapper">
    <input
      :type="showPwd ? 'text' : 'password'"
      placeholder="Пароль"
      v-model="password"
      required
    />
    <!-- svg-иконка — кликабельная -->
    <span class="pw-toggle" @click="showPwd = !showPwd">
      <!-- 👁 / 🙈 меняем в зависимости от showPwd -->
      <svg
        v-if="!showPwd"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        width="22"
        height="22"
      >
        <path
          fill="currentColor"
          d="M12 5C7 5 2.73 8.11 1 12c1.73 3.89 6 7 11 7s9.27-3.11 11-7c-1.73-3.89-6-7-11-7Zm0 11a4 4 0 1 1 0-8 4 4 0 0 1 0 8Z"
        />
      </svg>

      <svg
        v-else
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        width="22"
        height="22"
      >
        <path
          fill="currentColor"
          d="M2 2 22 22l-1.5 1.5-3.08-3.08A11.43 11.43 0 0 1 12 19c-5 0-9.27-3.11-11-7a11.31 11.31 0 0 1 4-4.73L.5 3.5 2 2Zm10 5a4 4 0 0 1 4 4 3.91 3.91 0 0 1-.44 1.8l-5.36-5.36A4 4 0 0 1 12 7Zm0 10a4 4 0 0 1-4-4 4 4 0 0 1 .44-1.79l5.35 5.35A4 4 0 0 1 12 17Z"
        />
      </svg>
    </span>
    </div>
    <button type="submit">Далее</button>
  </form>
</div>
</template>


<script setup>
import api from '@/api'
import StarField from '@/components/StarField.vue'
import TatliStarts from '@/components/TatliStarts.vue'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const login     = ref('')
const password  = ref('')
const showPwd   = ref(false)   // 👈 состояние «показать/скрыть»
const router = useRouter()

/* 3. сам submit */
async function handleSubmit () {
  const payload = { login: login.value, password: password.value }

  try {
    const { data } = await api.post('/login', payload)

    if (data.success) {
      router.push('/courses')          // ← переход
    } else {
      alert(`Ошибка входа: ${data.message || 'Неверные учётные данные'}`)
    }
  } catch (err) {
    console.error(err)
    alert('Не удалось подключиться к серверу. Попробуйте позже.')
  }
}
</script>



<style scoped>
.auth-wrapper {
  display: inline-block;
  text-align: left;
}

.pw-wrapper {
  position: relative;
}

/* сам input уже прозрачный по вашим правилам */
/* добавим padding-right, чтобы текст не залез под иконку */
.pw-wrapper input {
  padding-right: 50px;
}

/* кнопка-глазик */
.pw-toggle {
  position: absolute;
  right: 16px;          /* внутри поля */
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  color: #CDBDF5;
  opacity: .8;
  transition: opacity .15s;
}

.pw-toggle:hover { opacity: 1; }


.aerocos
{
    font-family: "Unbounded", "Inter", sans-serif;
  font-size: 110px;
 padding-right: 400px;
 margin-top: 150px;
  position:relative;        /* нужно, чтобы ::after позиционировался от заголовка */
  display:inline-block; 
  color: #EDEFFF;

}

.aerocos::after{
  content:"";
  position:absolute;
  left:0;                   /* линия начинается ровно под первой буквой */
  bottom:515px;             /* на 40 px ниже текста — меняй по вкусу */
  width:1150px;             /* длина линии; сделай 600-1200 px как надо */
  height:1px;
  background:rgba(255, 255, 255, 0.842);  /* тонкая полупрозрачная полоса */
}

/* сам текст цитаты */
.quote{
  position:absolute;
  top:290px;          /* вертикаль – подгони по своему макету */
  right:350px;        /* горизонталь – сколько отступить от правого края */
  max-width:700px;
  font-size:20px;
  line-height:1.45;
  font-family: "Unbounded", "Inter", sans-serif;
  color:rgba(237,239,255,.85); /* слегка приглушенный белый */
  transform: scaleX(0.8);
  letter-spacing: 2px;
  text-align:left;
}

/* сам заголовок превращаем во flex-контейнер,
   чтобы текст и линия выстроились в одну строку */
.auth-title{
     font-family: "Unbounded", "Inter", sans-serif;
  font-size:45px;          /* ваш размер */
  font-weight:400;
  margin:0 0 20px;         /* нижний отступ как был */
  color: #EDEFFF;
}

.section-line{
  width:80vw;                 /* растягиваем почти на всю ширину окна */
  max-width:1000px;           /* но не больше 1000 px, чтобы не «упиралась» */
  border:none;
  border-top:1px solid rgba(255,255,255,.35);
  margin:40px 0;              /* отступы сверху/снизу */
  pointer-events:none;        /* линия не перехватывает клики */
}

h1 {
  font-size: 50px;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-size: 20px;
}

.auth-wrapper form {
  width: 100%;
}

.auth-wrapper input,
.auth-wrapper button {
  width: 100%;
}


input {
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  box-sizing: border-box;
  border-color: #0000005b;
  place-content: "Логин";
  font-size: 17px;
  /* margin-top: 2px; */
}

button {
  width: 100%;
  padding: 10px;
  font-size: 20px;
  background-color: #501FD2;
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  margin-top: 0px;
}
:global(body) {
  margin: 0;
  padding-left: 100px;
  height: 100vh;
  background-color:#08000e;
  background-repeat: no-repeat;
  background-size: cover;
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: 'Inter', sans-serif;
  position: relative;
  overflow: hidden;
}

/* Эффект свечения (градиентное пятно) */
/* .glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  opacity: 0.4;
  mix-blend-mode: screen;
  z-index: -1;
  pointer-events: none;
}

.glow-1 {
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, #c4affa 0%, transparent 70%);
  top: 10%;
  left: 10%;
  animation: move1 12s ease-in-out infinite alternate;
}

.glow-2 {
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, #3f14a5 0%, transparent 70%);
  top: 40%;
  left: 70%;
  animation: move2 14s ease-in-out infinite alternate;
}

.glow-3 {
  width: 200px;
  height: 200px;
  background: radial-gradient(circle, #CDBDF5 0%, #4800ff 0%);
  top: 60%;
  left: 30%;
  animation: move3 18s ease-in-out infinite alternate;
}

.glow-4 {
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, #ff0000 30%);
  top: 80%;
  left: 60%;
  animation: move4 3s ease-in-out infinite alternate;
}

@keyframes move1 {
  0%   { transform: translate(0, 0) scale(1); }
  100% { transform: translate(40px, 60px) scale(1.1); }
}

@keyframes move2 {
  0%   { transform: translate(0, 0) scale(1); }
  100% { transform: translate(-60px, 40px) scale(1.2); }
}

@keyframes move3 {
  0%   { transform: translate(0, 0) scale(1); }
  100% { transform: translate(300px, -300px) scale(1.15); }
}

@keyframes move4 {
  0%   { transform: translate(0, 0) scale(1); }
  100% { transform: translate(-200px, -500px) scale(1.05); }
}
 */

button:hover {
  border-color: #ffffff;
  box-shadow: 0 0 10px rgba(205, 189, 245, 0.4);
}

.app {
  display:block;
  padding: 0;
}
/* 🔹 Убираем лишние отступы и прокрутку */
:global(html, body) {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
}


#app {
  padding: 0;
  max-width: fit-content;
}

/* 🔹 Основной контент */
.main-content {
  display: flex;
  flex-direction: column;
  padding: 20px;
}

form {
  width: 100%;
  max-width: 460px; /* совпадает с max-width формы */
  padding-top: 450px;
  display: flex;
  flex-direction: column;
  align-items: stretch;
}

input {
  width: 100%;
  padding: 12px 16px;
  border-radius: 10px;
  border: 1px solid #CDBDF5; /* тонкая светлая рамка */
  background-color: transparent; /* 👈 делает фон прозрачным */
  color: #EDEFFF; /* текст бело-сиреневый */
  font-size: 18px;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}

input::placeholder {
  color: #CDBDF5; /* сиреневый плейсхолдер */
  opacity: 0.7;
}

input:focus {
  border-color: #ffffff;
  box-shadow: 0 0 10px rgba(205, 189, 245, 0.4);
}

</style>
