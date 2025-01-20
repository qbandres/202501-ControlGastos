import { createRouter, createWebHistory } from "vue-router";
import { useUserStore } from "@/stores/userStore";
import Login from "@/views/Login.vue";
import Dashboard from "@/views/Dashboard.vue";
import Modificar from "@/views/Modificar.vue";

// Función para verificar si el usuario está autenticado
const requireAuth = (to, from, next) => {
  const userStore = useUserStore();
  console.log("UserStore username:", userStore.username); // Log para depuración
  if (!userStore.username) {
    next("/"); // Redirige al login si no hay usuario logueado
  } else {
    next(); // Permite el acceso si hay usuario
  }
};

const routes = [
  { path: "/", component: Login }, // Login no requiere autenticación
  {
    path: "/dashboard",
    component: Dashboard,
    beforeEnter: requireAuth, // Aplica la función de autenticación
  },
  {
    path: "/modificar",
    component: Modificar,
    beforeEnter: requireAuth, // Aplica la función de autenticación
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;