<template>
  <nav class="navbar">
    <!-- Contenedor del menú -->
    <div class="navbar-content">
      <!-- Lista de enlaces del navbar -->
      <ul :class="{'navbar-links': true, 'visible': isMenuVisible}">
        <li><router-link to="/dashboard">Inicio</router-link></li>
        <li><router-link to="/modificar">Modificar</router-link></li>
        <li><router-link to="/graficos">Gráficos</router-link></li>
        <li><router-link to="/tendencias">Tendencias</router-link></li>
        <li><router-link to="/agregar-gasto">Agregar Gasto</router-link></li>
        <li><a href="#" @click="logout">Cerrar sesión</a></li>
      </ul>

      <!-- Botón para abrir/cerrar el menú en pantallas pequeñas -->
      <button class="navbar-toggle" @click="toggleMenu">
        ☰
      </button>
    </div>
  </nav>
</template>

<script>
import { useUserStore } from "@/stores/userStore";
import { useRouter } from "vue-router";
import { ref } from "vue"; // Asegúrate de importar `ref`

export default {
  setup() {
    const userStore = useUserStore();
    const router = useRouter();
    const isMenuVisible = ref(false); // Estado que controla si el menú está visible

    const logout = () => {
      // Limpiar el estado del usuario y redirigir al login
      userStore.clearUser();
      localStorage.clear();
      sessionStorage.clear();
      router.push("/");
    };

    // Función para alternar la visibilidad del menú
    const toggleMenu = () => {
      isMenuVisible.value = !isMenuVisible.value;
    };

    return { logout, toggleMenu, isMenuVisible };
  },
};
</script>

<style>
.navbar {
  background-color: #f8f9fa;
  padding: 1rem;
  display: flex;
  justify-content: flex-end; /* Alinea el contenido al lado derecho */
  align-items: center; /* Alinea los elementos verticalmente */
  border-bottom: 1px solid #ddd;
}

.navbar-content {
  display: flex;
  justify-content: flex-end; /* Alinea los enlaces a la derecha */
  align-items: center;
  width: 100%;
}

.navbar-links {
  display: flex;
  gap: 1rem;
  list-style: none;
  margin: 0;
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

.navbar-toggle {
  background-color: transparent;
  border: none;
  font-size: 24px;
  color: #007bff;
  cursor: pointer;
  display: none; /* Ocultar el botón en pantallas grandes */
}

/* Responsividad para pantallas pequeñas */
@media (max-width: 768px) {
  .navbar-links {
    display: none; /* Ocultar los enlaces de menú por defecto */
    flex-direction: column;
    gap: 0.5rem;
    width: 100%;
    background-color: #f8f9fa;
    padding: 1rem;
    border-top: 1px solid #ddd;
  }

  .navbar-links.visible {
    display: flex; /* Mostrar los enlaces cuando se haga clic en el botón */
  }

  .navbar-toggle {
    display: block; /* Mostrar el botón en pantallas pequeñas */
  }
}
</style>