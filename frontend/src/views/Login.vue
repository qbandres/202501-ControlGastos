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
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<script>
import axios from "axios";
import { useUserStore } from "@/stores/userStore"; // Importa la tienda del usuario

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
      console.log("Attempting login with username:", this.username);

      try {
        // Llama al backend con las credenciales
        const response = await axios.post("http://localhost:8000/login", {
          username: this.username,
          password: this.password,
        });

        console.log("Response from backend:", response.data);

        // Verifica si la respuesta contiene un username
        if (response.data.username) {
          console.log("Login successful, redirecting to Dashboard...");

          // Guarda el nombre de usuario en el estado global
          const userStore = useUserStore();
          userStore.setUsername(response.data.username);

          // Redirige al Dashboard
          this.$router.push("/dashboard");
        } else {
          console.warn("Login failed, server message:", response.data.message);
          this.errorMessage = response.data.message || "Login failed";
        }
      } catch (error) {
        // Captura errores y muestra mensajes
        console.error("Error during login:", error);
        this.errorMessage =
          error.response?.data?.detail || "Login failed. Please try again.";
      }
    },
  },
};
</script>

<style>
.error {
  color: red;
  font-weight: bold;
  margin-top: 10px;
}
</style>