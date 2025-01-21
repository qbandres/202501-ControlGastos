<template>
  <div>
    <!-- Componente para mostrar el título general de la página -->
    <Titulo />
    
    <!-- Componente para la barra de navegación -->
    <Navbar />
    
    <!-- Incluye Tablagastos, que gestiona la tabla y los filtros -->
    <Tablagastos />
  </div>
</template>

<script>
import Titulo from "@/components/Titulo.vue";
import Navbar from "@/components/Navbar.vue";
import Tablagastos from "@/components/Tablagastos.vue";

export default {
  components: {
    Titulo, // Registra el componente de título
    Navbar, // Registra el componente de navegación
    Tablagastos, // Registra Tablagastos, que incluye la tabla y los filtros
  },
};
</script>