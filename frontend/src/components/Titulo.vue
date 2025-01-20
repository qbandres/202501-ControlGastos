<script>
import { useUserStore } from "@/stores/userStore";

export default {
  setup() {
    const userStore = useUserStore();
    return { username: userStore.username };
  },
};
</script>

<template>
  <div>
    <h1>Bienvenido {{ username }}</h1>
  </div>
</template>