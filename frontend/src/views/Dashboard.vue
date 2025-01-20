<template>
  <div>
    <Titulo />
    <Navbar />
    <TablaGastos />
  </div>
</template>

<script>
import Titulo from "@/components/Titulo.vue";
import Navbar from "@/components/Navbar.vue";
import TablaGastos from "@/components/TablaGastos.vue";

export default {
  components: {
    Titulo,
    Navbar,
    TablaGastos,
  },
};
</script>