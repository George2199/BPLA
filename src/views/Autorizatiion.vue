<template>
   <GradientBar />
  <div class="app-container">
    <div class="main-content">
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
        </div>
      </div>
      
 

</template>

<script setup>
import { toDisplayString } from 'vue';
import GradientBar from '@/components/GradientBar.vue';
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
        const response = await fetch('http://127.0.0.1:5000/login', { // URL of your Flask backend
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(loginData), // Send data as JSON string
        });

        const result = await response.json(); // Parse the JSON response from Flask

        if (response.ok && result.success) {
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

<style scoped>

h1 {
  font-size: 40px;
  margin-top: 80px;
  margin-bottom: 70px;
  margin-left: 60px;
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
  width: 140px;
  padding: 10px;
  font-size: 20px;
  background-color: #000000;
  color: white;
  border: none;
  border-radius: 5px;
  margin-left: 250px;
  cursor: pointer;
  
  margin-top: 70px;
}

body {
  font-family: 'CustomFontName', Arial, sans-serif;
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

/* 🔹 Главный контейнер */
.app-container {
  display: flex;
  width: 500px;
  height: 600px;
  margin-left: 940px;
  margin-top: 50px;
  background: #ffffff;
  color: rgb(0, 0, 0);
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
</style>
