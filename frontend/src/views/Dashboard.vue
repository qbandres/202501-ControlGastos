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
        <table>
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
        <div class="placeholder">🚧 Próxima implementación</div>

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
      gastosPorMes: [],        // No se modifica la lógica de esta propiedad
      gastosUltimos7Dias: []  // Datos del gráfico y tabla de últimos 7 días
    };
  },
  methods: {
    async fetchGastosUltimos7Dias() {
      try {
        const backendUrl = import.meta.env.VITE_BACKEND_URL;

        // 🔹 Cargar datos para "Gastos de los Últimos 7 Días"
        const response = await axios.post(`${backendUrl}/graficos_dinamicos/datos_fecha_dia`, {
          x_column: "fecha",
          y_column: "cantidad",
          n_ultimos_dias: 7
        });
        console.log("Datos recibidos para gastosUltimos7Dias:", response.data.data);
        this.gastosUltimos7Dias = response.data.data; // Actualiza el arreglo con los datos
      } catch (error) {
        console.error("Error obteniendo los datos para los últimos 7 días:", error);
      }
    }
  },
  async mounted() {
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
  margin-bottom: 50px; /* Espaciado adicional con respecto a la tabla general */
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