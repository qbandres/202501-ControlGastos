<template>
  <div class="container">
    <h1>Login</h1>
    <form @submit.prevent="handleLogin" class="content__form">
      <div class="content__inputs">
        <label>
          <select v-model="username" required>
            <option value="Andres">Andres</option>
            <option value="Yovana">Yovana</option>
          </select>
          <span>Username</span>
        </label>
        <label>
          <input
            v-model="password"
            type="password"
            required
            placeholder=" "
          />
          <span>Password</span>
        </label>
      </div>
      <button type="submit">Login</button>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </form>
  </div>
</template>

<script>
import axios from "axios";
import { useUserStore } from "@/stores/userStore";

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
        const backendUrl = import.meta.env.VITE_BACKEND_URL;
        const response = await axios.post(`${backendUrl}/login`, {
          username: this.username,
          password: this.password,
        });

        if (response.data.username) {
          const userStore = useUserStore();
          userStore.setUsername(response.data.username);
          this.$router.push("/dashboard");
        } else {
          this.errorMessage = response.data.message || "Login failed";
        }
      } catch (error) {
        this.errorMessage =
          error.response?.data?.detail || "Login failed. Please try again.";
      }
    },
  },
};
</script>

<style scoped>
/* Adapted styles */
.container {
  border-radius: 1px;
  padding: 50px 40px 20px 40px;
  box-sizing: border-box;
  font-family: sans-serif;
  color: #737373;
  border: 1px solid rgb(219, 219, 219);
  text-align: center;
  background: white;
  max-width: 400px;
  margin: 50px auto;
}

h1 {
  margin-bottom: 20px;
  font-size: 24px;
  color: #333;
}

.content__form {
  display: flex;
  flex-direction: column;
  row-gap: 14px;
}

.content__inputs {
  display: flex;
  flex-direction: column;
  row-gap: 8px;
}

label {
  border: 1px solid rgb(219, 219, 219);
  display: flex;
  align-items: center;
  position: relative;
  min-width: 268px;
  height: 38px;
  background: rgb(250, 250, 250);
  border-radius: 3px;
}

select,
input {
  width: 100%;
  background: inherit;
  border: 0;
  outline: none;
  padding: 9px 8px 7px 8px;
  font-size: 16px;
  vertical-align: middle;
}

select:required:invalid {
  color: gray;
}

option[value=""][disabled] {
  display: none;
}

span {
  position: absolute;
  text-overflow: ellipsis;
  transform-origin: left;
  font-size: 12px;
  left: 8px;
  pointer-events: none;
  transition: transform ease-out 0.1s;
}

input:valid + span,
select:valid + span {
  transform: scale(calc(10 / 12)) translateY(-10px);
}

input:valid,
select:valid {
  padding: 14px 0 2px 8px;
  font-size: 12px;
}

button {
  background: rgb(0, 149, 246);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 700;
  font-size: 14px;
  padding: 7px 16px;
  cursor: pointer;
  transition: all 0.3s ease;
}

button:hover {
  background: rgb(24, 119, 242);
}

button:active:not(:hover) {
  background: rgb(0, 149, 246);
  opacity: 0.7;
}

.error {
  color: red;
  font-weight: bold;
  margin-top: 10px;
}
</style>
