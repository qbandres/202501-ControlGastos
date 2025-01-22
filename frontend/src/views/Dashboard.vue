<template>
  <div>
    <!-- Componente para mostrar el título general de la página -->
    <Titulo />
    
    <!-- Componente para la barra de navegación -->
    <Navbar />
    
    <h2>Dashboard</h2>

    <!-- Tabla con los gastos de los últimos 3 meses -->
    <h3>Gastos por Mes</h3>
    <table>
      <thead>
        <tr>
          <th>Mes</th>
          <th>Total Gastos</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(gasto, index) in gastosPorMes" :key="index">
          <td>{{ gasto.mes }}</td>
          <td>{{ gasto.total_gastos }}</td>
        </tr>
      </tbody>
    </table>

    <!-- Tabla con los gastos de los últimos 7 días -->
    <h3>Gastos de los Últimos 7 Días</h3>
    <table>
      <thead>
        <tr>
          <th>Fecha</th>
          <th>Total Gastos</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(gasto, index) in gastosUltimos7Dias" :key="index">
          <td>{{ gasto.fecha }}</td>
          <td>{{ gasto.total_gastos }}</td>
        </tr>
      </tbody>
    </table>
    
    <!-- Componente Tablagastos.vue para manejar la tabla de gastos con filtros -->
    <Tablagastos />
  </div>
</template>

<script>
import axios from "axios";
import Titulo from "@/components/Titulo.vue";
import Navbar from "@/components/Navbar.vue";
import Tablagastos from "@/components/Tablagastos.vue"; // Importamos el componente Tablagastos.vue

export default {
  components: { Titulo, Navbar, Tablagastos }, // Registramos el componente
  data() {
    return {
      gastosPorMes: [],
      gastosUltimos7Dias: [],
    };
  },
  methods: {
    async fetchMonthlyData() {
      try {
        // Usar la URL del backend desde la variable de entorno
        const backendUrl = import.meta.env.VITE_BACKEND_URL;
        const response = await axios.get(`${backendUrl}/resumen-gastos/gastos-ultimos-3-meses`);
        this.gastosPorMes = response.data;
      } catch (error) {
        console.error("Error al obtener los datos mensuales:", error);
      }
    },
    async fetchLast7DaysData() {
      try {
        // Usar la URL del backend desde la variable de entorno
        const backendUrl = import.meta.env.VITE_BACKEND_URL;
        const response = await axios.get(`${backendUrl}/resumen-gastos/gastos-ultimos-7-dias`);
        this.gastosUltimos7Dias = response.data.data;
      } catch (error) {
        console.error("Error al obtener los datos de los últimos 7 días:", error);
      }
    },
  },
  async mounted() {
    await this.fetchMonthlyData(); // Llamada a los datos mensuales
    await this.fetchLast7DaysData(); // Llamada a los datos de los últimos 7 días
  },
};
</script>

<style>
h2 {
  margin-bottom: 20px;
}

h3 {
  margin-top: 30px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 10px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}
</style>