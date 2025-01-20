// Importa funciones del módulo vue-router
import { createRouter, createWebHistory } from "vue-router";

// Importa el store global para manejar el estado del usuario
import { useUserStore } from "@/stores/userStore";

// Importa las vistas que se utilizarán en las rutas
import Login from "@/views/Login.vue";
import Dashboard from "@/views/Dashboard.vue";
import Modificar from "@/views/Modificar.vue";

// Función para verificar si el usuario está autenticado
const requireAuth = (to, from, next) => {
  const userStore = useUserStore(); // Obtiene el estado del usuario desde el store
  console.log("UserStore username:", userStore.username); // Log para depuración
  if (!userStore.username) {
    // Si no hay usuario en el store
    next("/"); // Redirige al login
  } else {
    // Si el usuario está autenticado
    next(); // Permite continuar con la navegación
  }
};

// Definición de las rutas de la aplicación
const routes = [
  { path: "/", component: Login }, // Ruta para el Login, no requiere autenticación
  {
    path: "/dashboard", // Ruta para el Dashboard
    component: Dashboard, // Componente que se renderizará
    beforeEnter: requireAuth, // Aplica la función de autenticación
  },
  {
    path: "/modificar", // Ruta para Modificar
    component: Modificar, // Componente que se renderizará
    beforeEnter: requireAuth, // Aplica la función de autenticación
  },
];

// Crea una instancia del router con las rutas definidas
const router = createRouter({
  history: createWebHistory(), // Usa el historial del navegador para navegación limpia
  routes, // Aplica las rutas definidas
});

// Exporta la instancia del router para usarla en la aplicación
export default router;