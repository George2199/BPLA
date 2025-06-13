<template>
<div class="glow glow-1"></div>
  <div class="glow glow-2"></div>
  <div class="glow glow-3"></div>
  <div class="glow glow-4"></div>
  <div class="aerocos">Аэрокосмос</div>
    
      <h1>Авторизация</h1>
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="login">Логин</label>
          <input type="text" placeholder="Логин" id="login" v-model="login" required />
        </div>
        <div class="form-group">
          <label for="password">Пароль</label>
          <input type="password" placeholder="Пароль" id="password" v-model="password" required />
        </div>
        <button type="submit">Далее</button>
      </form>
</template>


<script setup>
import { toDisplayString } from 'vue';
import api from '@/api'
</script>


<script>
export default {
  data() {
    return {
      login: '',
      password: '',
    };
  },
  methods: {
    async handleSubmit() { // Make the method async to use await
      const loginData = {
        login: this.login,
        password: this.password
      };

      try {
        const response = await api.post('/login', loginData)
        const result = response.data

        if (result.success) {
          // Login successful
          console.log('Login successful, navigating to /courses'); // Path is /courses
          this.$router.push('/courses'); // Navigate back to /courses
        } else {
          // Login failed or other error from backend
          alert(`Ошибка входа: ${result.message || 'Неверные учетные данные'}`);
        }
      } catch (error) {
        // Network error or other issue with the fetch call
        console.error('Ошибка при отправке запроса:', error);
        alert('Не удалось подключиться к серверу. Пожалуйста, попробуйте позже.');
      }
    },

    // change: function(){ ... } // Removed unused methods
    // change1: function(){ ... } // Removed unused methods
    // cost1: function(){ ... } // Removed unused methods
  }
};
</script>

<style>

.aerocos
{
  font-size: 100px;
 padding-right: 200px;
 margin-top: 150px;
}

h1 {
  font-size: 40px;
  margin-top: 80px;
  margin-bottom: 220px;
}

.form-group {
  margin-bottom: 15px;
  max-width: 400px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-size: 20px;
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
  align-self: flex-end; /* Выравнивание кнопки по правому краю */
  width: 140px;
  padding: 10px;
  font-size: 20px;
  background-color: #000000;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 30px;
}

body {
  margin: 0;
  height: 100vh;
  background-color:#08000e;
  background-repeat: no-repeat;
  background-size: cover;
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: 'Inter', sans-serif;
  color: #EDEFFF;
  position: relative;
  overflow: hidden;
}

/* Эффект свечения (градиентное пятно) */
.glow-1 {
  content: "";
  position: absolute;
  width: 1900px;
  height: 1200px;
  background: radial-gradient(circle at center, #c4affa 20%,transparent 100%);
  top: 20%;
  right: 5%;
  transform: translate(30%, -55%);
  filter: blur(150px);
  opacity: 0.6;
  z-index: -1;
}

.glow-2 {
  content: "";
  position: absolute;
  width: 900px;
  height: 500px;
  background: radial-gradient(circle at center, #3f14a5 40%, transparent 100%);
  top: 20%;
  right: 10%;
  transform: translate(60%, -80%);
  filter: blur(100px);
  z-index: -1;
}

.glow-3 {
  content: "";
  position: absolute;
  width: 400px;
  height: 500px;
  background: radial-gradient(circle at center, #CDBDF5 40%, transparent 100%);
  top: 20%;
  right: 10%;
  transform: translate(-100%, -80%);
  filter: blur(100px);
  z-index: -1;
}

.glow-4 {
  content: "";
  position: absolute;
  width: 200px;
  height: 300px;
  background: radial-gradient(circle at center, #CDBDF5 40%, transparent 100%);
  top: 20%;
  right: 10%;
  transform: translate(60%, -30%);
  filter: blur(100px);
  z-index: -1;
}


button:hover {
  background-color: #282828;
}

.app {
  display:block;
  padding: 0;
}
/* 🔹 Убираем лишние отступы и прокрутку */
html, body {
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
  max-width: 400px; /* совпадает с max-width формы */
  display: flex;
  flex-direction: column;
  align-items: stretch;
}

</style>
