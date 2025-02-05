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
        <h3>Gastos por Mes (Tabla)</h3>
        <table v-if="gastosPorMesTabla.length">
          <thead>
            <tr>
              <th>Mes</th>
              <th>Total Gastos</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(gasto, index) in gastosPorMesTabla" :key="index">
              <td>{{ gasto.label }}</td>
              <td>{{ gasto.value }}</td>
            </tr>
          </tbody>
        </table>
        <p v-else>No hay datos disponibles para "Gastos por Mes".</p>

        <br>
        <hr style="border: 0; height: 0.5px; background: #000; opacity: 0.5;">
        <br>

        <h3>Gastos de los Últimos 7 Días (Tabla)</h3>
        <table v-if="gastosUltimos7DiasTabla.length">
          <thead>
            <tr>
              <th>Fecha</th>
              <th>Total Gastos</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(gasto, index) in gastosUltimos7DiasTabla" :key="index">
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
            :data="gastosPorMesGrafico" 
            :config="{ title: 'Gastos por Mes', borderColor: 'blue' }" 
          />
        </div>

        <h3>Gráfico: Gastos de los Últimos 7 Días</h3>
        <div class="graph-container">
          <Graficos2D 
            type="line" 
            :data="gastosUltimos7DiasGrafico" 
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
      gastosPorMesTabla: [],      // Datos de gastos por mes para la tabla (orden DESC)
      gastosPorMesGrafico: [],    // Datos de gastos por mes para el gráfico (orden ASC)
      gastosUltimos7DiasTabla: [], // Datos de gastos últimos 7 días para la tabla (orden DESC)
      gastosUltimos7DiasGrafico: [] // Datos de gastos últimos 7 días para el gráfico (orden ASC)
    };
  },
  methods: {
    // 🔹 Obtener datos para la tabla de "Gastos por Mes"
    async fetchGastosPorMesTabla() {
      try {
        const backendUrl = import.meta.env.VITE_BACKEND_URL;
        const response = await axios.post(`${backendUrl}/graficos_dinamicos/datos_fecha_mes`, {
          order: "desc", // Las tablas deben mostrar los datos en orden descendente
          n_ultimos_meses: 10 // Mostramos los últimos 6 meses
        });
        console.log("Datos recibidos para gastosPorMesTabla:", response.data.data);
        this.gastosPorMesTabla = response.data.data; 
      } catch (error) {
        console.error("Error obteniendo los datos para gastos por mes (Tabla):", error);
      }
    },

    // 🔹 Obtener datos para el gráfico de "Gastos por Mes"
    async fetchGastosPorMesGrafico() {
      try {
        const backendUrl = import.meta.env.VITE_BACKEND_URL;
        const response = await axios.post(`${backendUrl}/graficos_dinamicos/datos_fecha_mes`, {
          order: "asc", // Los gráficos deben mostrar los datos en orden ascendente
          n_ultimos_meses: 10 // Mostramos los últimos 6 meses
        });
        console.log("Datos recibidos para gastosPorMesGrafico:", response.data.data);
        this.gastosPorMesGrafico = response.data.data; 
      } catch (error) {
        console.error("Error obteniendo los datos para gastos por mes (Gráfico):", error);
      }
    },

    // 🔹 Obtener datos para la tabla de "Gastos últimos 7 días"
    async fetchGastosUltimos7DiasTabla() {
      try {
        const backendUrl = import.meta.env.VITE_BACKEND_URL;
        const response = await axios.post(`${backendUrl}/graficos_dinamicos/datos_fecha_dia`, {
          order: "desc", // Las tablas deben mostrar los datos en orden descendente
          n_ultimos_dias: 10
        });
        console.log("Datos recibidos para gastosUltimos7DiasTabla:", response.data.data);
        this.gastosUltimos7DiasTabla = response.data.data; 
      } catch (error) {
        console.error("Error obteniendo los datos para gastos últimos 7 días (Tabla):", error);
      }
    },

    // 🔹 Obtener datos para el gráfico de "Gastos últimos 7 días"
    async fetchGastosUltimos7DiasGrafico() {
      try {
        const backendUrl = import.meta.env.VITE_BACKEND_URL;
        const response = await axios.post(`${backendUrl}/graficos_dinamicos/datos_fecha_dia`, {
          order: "asc", // Los gráficos deben mostrar los datos en orden ascendente
          n_ultimos_dias: 7
        });
        console.log("Datos recibidos para gastosUltimos7DiasGrafico:", response.data.data);
        this.gastosUltimos7DiasGrafico = response.data.data; 
      } catch (error) {
        console.error("Error obteniendo los datos para gastos últimos 7 días (Gráfico):", error);
      }
    }
  },
  
  // 🔹 Llamamos a los métodos de obtención de datos al montar la vista
  async mounted() {
    await this.fetchGastosPorMesTabla();
    await this.fetchGastosPorMesGrafico();
    await this.fetchGastosUltimos7DiasTabla();
    await this.fetchGastosUltimos7DiasGrafico();
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