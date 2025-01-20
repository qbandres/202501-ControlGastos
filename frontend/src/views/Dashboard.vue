<template>
  <div>
    <!-- Componente para mostrar el título general de la página -->
    <Titulo />
    
    <!-- Componente para la barra de navegación -->
    <Navbar />
    
    <!-- Incluye GastosPage, que gestiona la tabla y los filtros -->
    <GastosPage />
  </div>
</template>

<script>
import Titulo from "@/components/Titulo.vue";
import Navbar from "@/components/Navbar.vue";
import GastosPage from "@/components/GastosPage.vue";

export default {
  components: {
    Titulo, // Registra el componente de título
    Navbar, // Registra el componente de navegación
    GastosPage, // Registra GastosPage, que incluye la tabla y los filtros
  },
};
</script>