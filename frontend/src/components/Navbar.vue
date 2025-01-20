<template>
    <nav class="navbar">
      <ul>
        <li><router-link to="/dashboard">Inicio</router-link></li>
        <li><router-link to="/modificar">Modificar</router-link></li>
        <li><a href="#" @click="logout">Cerrar sesión</a></li>
      </ul>
    </nav>
  </template>
  
  <script>
  import { useUserStore } from "@/stores/userStore";
  import { useRouter } from "vue-router";
  
  export default {
    setup() {
      const userStore = useUserStore();
      const router = useRouter();
  
      const logout = () => {
        // Limpia el estado del usuario y redirige al login
        userStore.clearUser();
        localStorage.clear();
        sessionStorage.clear();
        router.push("/");
      };
  
      return { logout };
    },
  };
  </script>
  
  <style>
  .navbar {
    background-color: #f8f9fa;
    padding: 1rem;
    display: flex;
    justify-content: space-around;
    list-style: none;
    border-bottom: 1px solid #ddd;
  }
  
  .navbar ul {
    margin: 0;
    padding: 0;
    display: flex;
    gap: 1rem;
  }
  
  .navbar li {
    list-style: none;
  }
  
  .navbar a {
    text-decoration: none;
    color: #007bff;
    font-weight: bold;
  }
  
  .navbar a:hover {
    text-decoration: underline;
  }
  </style>