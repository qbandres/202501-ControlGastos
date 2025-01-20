<template>
    <div class="login">
      <h1>Login</h1>
      <form @submit.prevent="handleLogin">
        <div>
          <label for="username">Username:</label>
          <input v-model="username" id="username" type="text" required />
        </div>
        <div>
          <label for="password">Password:</label>
          <input v-model="password" id="password" type="password" required />
        </div>
        <button type="submit">Login</button>
      </form>
      <p v-if="errorMessage">{{ errorMessage }}</p>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        username: "",
        password: "",
        errorMessage: "",
      };
    },
    methods: {
      async handleLogin() {
        try {
          const response = await axios.post(
            "http://localhost:8000/login",
            {
              username: this.username,
              password: this.password,
            }
          );
          // Redirige al Dashboard si el login es exitoso
          this.$router.push("/dashboard");
        } catch (error) {
          this.errorMessage = error.response?.data?.detail || "Login failed";
        }
      },
    },
  };
  </script>