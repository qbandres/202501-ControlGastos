<template>
  <div>
    <!-- Componente para mostrar el título general de la página -->
    <Titulo />

    <!-- Componente para la barra de navegación -->
    <Navbar />

    <h2>Dashboard</h2>

    <!-- Contenedor principal del Dashboard -->
    <div class="dashboard-container">
      <!-- Columna de tablas -->
      <div class="dashboard-tables">
        <h3>Gastos por Mes</h3>
        <table v-if="gastosPorMes.length">
          <thead>
            <tr>
              <th>Mes</th>
              <th>Total Gastos</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(gasto, index) in gastosPorMes" :key="index">
              <td>{{ gasto.label }}</td>
              <td>{{ gasto.value }}</td>
            </tr>
          </tbody>
        </table>
        <p v-else>No hay datos disponibles para "Gastos por Mes".</p>
        <br>
        <br>

        <hr style="border: 0; height: 0.5px; background: #000; opacity: 0.5;">
        <br>
        


        <h3>Gastos de los Últimos 7 Días</h3>
        <table v-if="gastosUltimos7Dias.length">
          <thead>
            <tr>
              <th>Fecha</th>
              <th>Total Gastos</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(gasto, index) in gastosUltimos7Dias" :key="index">
              <td>{{ gasto.label }}</td>
              <td>{{ gasto.value }}</td>
            </tr>
          </tbody>
        </table>
        <p v-else>No hay datos disponibles para "Gastos de los Últimos 7 Días".</p>
      </div>

      <!-- Columna de gráficos -->
      <div class="dashboard-graphs">
        <h3>Gráfico: Gastos por Mes</h3>
        <div class="graph-container">
          <Graficos2D 
            type="bar" 
            :data="gastosPorMes" 
            :config="{ title: 'Gastos por Mes', borderColor: 'blue' }" 
          />
        </div>

        <h3>Gráfico: Gastos de los Últimos 7 Días</h3>
        <div class="graph-container">
          <Graficos2D 
            type="line" 
            :data="gastosUltimos7Dias" 
            :config="{ title: 'Gastos Últimos 7 Días', borderColor: 'red' }" 
          />
        </div>
      </div>
    </div>

    <!-- Contenedor independiente para la tabla de gastos generales -->
    <div class="general-gastos">
      <h2>Gastos</h2>
      <Tablagastos />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Titulo from "@/components/Titulo.vue";
import Navbar from "@/components/Navbar.vue";
import Tablagastos from "@/components/Tablagastos.vue";
import Graficos2D from "@/components/graficos2D/index.vue";

export default {
  components: { Titulo, Navbar, Tablagastos, Graficos2D },
  data() {
    return {
      gastosPorMes: [], // Datos de gastos por mes
      gastosUltimos7Dias: [] // Datos de gastos por día
    };
  },
  methods: {
    async fetchGastosPorMes() {
      try {
        const backendUrl = import.meta.env.VITE_BACKEND_URL;
        const response = await axios.post(`${backendUrl}/graficos_dinamicos/datos_fecha_mes`);
        console.log("Datos recibidos para gastosPorMes:", response.data.data);
        this.gastosPorMes = response.data.data; // Actualiza los datos
      } catch (error) {
        console.error("Error obteniendo los datos para gastos por mes:", error);
      }
    },
    async fetchGastosUltimos7Dias() {
      try {
        const backendUrl = import.meta.env.VITE_BACKEND_URL;
        const response = await axios.post(`${backendUrl}/graficos_dinamicos/datos_fecha_dia`, {
          x_column: "fecha",
          y_column: "cantidad",
          n_ultimos_dias: 7
        });
        console.log("Datos recibidos para gastosUltimos7Dias:", response.data.data);
        this.gastosUltimos7Dias = response.data.data; // Actualiza los datos
      } catch (error) {
        console.error("Error obteniendo los datos para los últimos 7 días:", error);
      }
    }
  },
  async mounted() {
    await this.fetchGastosPorMes();
    await this.fetchGastosUltimos7Dias();
  }
};
</script>

<style>
/* 📌 Contenedor Principal del Dashboard */
.dashboard-container {
  display: grid;
  grid-template-columns: 1fr 1fr; /* Dos columnas iguales */
  gap: 20px;
  margin-bottom: 50px;
}

/* 📌 Tablas de Gastos */
.dashboard-tables table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

.dashboard-tables th, .dashboard-tables td {
  padding: 10px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.dashboard-tables th {
  background-color: #f0f0f0;
}

/* 📌 Encapsular gráficos */
.dashboard-graphs {
  padding: 10px;
}

.graph-container {
  width: 100%;
  height: 300px;
  overflow: hidden;
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 8px;
  background-color: #f9f9f9;
}

/* 📌 Tabla General de Gastos */
.general-gastos {
  margin-top: 50px;
  padding: 20px;
  border-top: 2px solid #ccc;
}

/* 📌 Placeholder para Gráficos no Implementados */
.placeholder {
  text-align: center;
  padding: 20px;
  border: 1px dashed gray;
  font-size: 1.2em;
  color: gray;
}

/* 📌 Responsividad */
@media (max-width: 768px) {
  .dashboard-container {
    grid-template-columns: 1fr; /* Una sola columna en pantallas pequeñas */
  }
}
</style>