<template>
  <div>
    <Titulo />
    <Navbar />
    <h2>Esta es la página para Modificar</h2>
    <!-- Resto del contenido de la página -->
  </div>
</template>

<script>
import Titulo from "@/components/Titulo.vue";
import Navbar from "@/components/Navbar.vue";

export default {
  components: {
    Titulo,
    Navbar,
  },
};
</script>