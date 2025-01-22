<template>
  <div class="login-container">
    <div class="login-form">
      <h1>Login</h1>
      <form @submit.prevent="handleLogin">
        <div>
          <label for="username">Username:</label>
          <select v-model="username" id="username" required class="input-field">
            <option value="Andres">Andres</option>
            <option value="Yovana">Yovana</option>
          </select>
        </div>
        <div>
          <label for="password">Password:</label>
          <input v-model="password" id="password" type="password" required class="input-field" />
        </div>
        <button type="submit" class="login-btn">Login</button>
      </form>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useUserStore } from "@/stores/userStore"; // Importa la tienda del usuario

export default {
  data() {
    return {
      username: "Yovana",  // Valor predeterminado
      password: "",
      errorMessage: "",
    };
  },
  methods: {
    async handleLogin() {
      console.log("Attempting login with username:", this.username);

      try {
        // Obtiene la URL del backend desde la variable de entorno
        const backendUrl = import.meta.env.VITE_BACKEND_URL;

        // Llama al backend con las credenciales
        const response = await axios.post(`${backendUrl}/login`, {
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

<style scoped>
/* Diseño minimalista centrado con fondo blanco humo */
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100vh;
  background-color: #f5f5f5; /* Fondo blanco humo */
}

.login-form {
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  text-align: center;
}

h1 {
  margin-bottom: 20px;
  color: #333;
}

form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

label {
  text-align: left;
  margin-bottom: 5px;
}

.input-field {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 100%; /* Asegura que ambos campos tengan el mismo ancho */
}

.login-btn {
  background-color: #007bff;  /* Azul */
  color: white;
  border: none;
  padding: 10px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.login-btn:hover {
  background-color: #0056b3;  /* Azul más oscuro al pasar el mouse */
}

.login-btn:active {
  transform: scale(0.98);  /* Efecto de clic */
}

.error {
  color: red;
  font-weight: bold;
  margin-top: 10px;
}

/* Responsividad */
@media (max-width: 600px) {
  .login-form {
    width: 90%;
    padding: 20px;
  }

  h1 {
    font-size: 1.5rem;
  }

  input,
  select,
  .login-btn {
    font-size: 1rem;
  }
}
</style>