<template>
  <div>
    <Titulo />
    <Navbar />
    <h2>Gráficos X-Y</h2>

    <!-- Selección de ejes -->
    <div>
      <label for="x-axis">X-Axis:</label>
      <select v-model="selectedAxis.x" id="x-axis">
        <option v-for="option in axisOptions.x" :key="option.value" :value="option.value">
          {{ option.label }}
        </option>
      </select>

      <label for="y-axis">Y-Axis:</label>
      <select v-model="selectedAxis.y" id="y-axis">
        <option v-for="option in axisOptions.y" :key="option.value" :value="option.value">
          {{ option.label }}
        </option>
      </select>

      <!-- Filtro de rango de fechas -->
      <label>Desde:</label>
      <input v-model="filters.fecha.start" type="date" />

      <label>Hasta:</label>
      <input v-model="filters.fecha.end" type="date" />

      <button @click="generateChart">Generar Gráfico</button>
    </div>

    <!-- Gráfico principal -->
    <div style="width: 100%; height: 400px;">
      <canvas id="chartCanvas"></canvas>
    </div>

    <h2>Gráfico secundario: Clase vs Cantidad</h2>

    <!-- Gráfico secundario -->
    <div style="width: 100%; height: 400px;">
      <canvas id="secondaryChartCanvas"></canvas>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Titulo from "@/components/Titulo.vue";
import Navbar from "@/components/Navbar.vue";
import Chart from "chart.js/auto";
import "chartjs-adapter-date-fns";

export default {
  components: { Titulo, Navbar },
  data() {
    return {
      chart: null, // Instancia del gráfico principal
      secondaryChart: null, // Instancia del gráfico secundario
      axisOptions: {
        x: [
          { value: "fecha", label: "Fecha" },
          { value: "clase", label: "Clase" },
          { value: "asignacion", label: "Asignación" },
          { value: "usuario", label: "Usuario" },
        ],
        y: [{ value: "cantidad", label: "Cantidad" }],
      },
      selectedAxis: {
        x: "fecha", // Valor por defecto para X
        y: "cantidad", // Valor por defecto para Y
      },
      filters: {
        fecha: {
          start: "2024-11-01", // Rango de fecha inicial predefinido
          end: "2025-04-30",   // Rango de fecha final predefinido
        },
      },
    };
  },
  methods: {
    async generateChart() {
      try {
        // Obtener la URL del backend desde las variables de entorno
        const backendUrl = import.meta.env.VITE_BACKEND_URL;
        
        // Obtener datos para el gráfico principal
        const response = await axios.post(`${backendUrl}/graficos/x-y`, {
          x_axis: this.selectedAxis.x,
          y_axis: this.selectedAxis.y,
          filters: this.filters,
        });

        const { data } = response.data;

        console.log("Datos del gráfico principal:", data);

        // Si ya existe un gráfico principal, destrúyelo
        if (this.chart) {
          this.chart.destroy();
        }

        // Crear el gráfico principal
        const ctx = document.getElementById("chartCanvas").getContext("2d");
        this.chart = new Chart(ctx, {
          type: "bar",
          data: {
            labels: data.map((point) => point.x),
            datasets: [
              {
                label: `Gráfico de ${this.selectedAxis.y} vs ${this.selectedAxis.x}`,
                data: data.map((point) => point.y),
                backgroundColor: "rgba(75, 192, 192, 0.6)",
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              x: {
                type: this.selectedAxis.x === "fecha" ? "time" : "category",
                time: {
                  unit: "day",
                  tooltipFormat: "yyyy-MM-dd",
                  displayFormats: {
                    day: "MMM dd, yyyy",
                  },
                },
                title: {
                  display: true,
                  text: this.selectedAxis.x,
                },
              },
              y: {
                beginAtZero: true,
                title: {
                  display: true,
                  text: this.selectedAxis.y,
                },
              },
            },
          },
        });

        // Generar el gráfico secundario con "clase" como X
        await this.generateSecondaryChart();
      } catch (error) {
        console.error("Error al generar el gráfico:", error);
      }
    },
    async generateSecondaryChart() {
      try {
        // Obtener la URL del backend desde las variables de entorno
        const backendUrl = import.meta.env.VITE_BACKEND_URL;

        // Obtener datos para el gráfico secundario
        const response = await axios.post(`${backendUrl}/graficos/x-y`, {
          x_axis: "clase", // Eje X fijo en "clase"
          y_axis: this.selectedAxis.y,
          filters: this.filters,
        });

        const { data } = response.data;

        console.log("Datos del gráfico secundario:", data);

        // Si ya existe un gráfico secundario, destrúyelo
        if (this.secondaryChart) {
          this.secondaryChart.destroy();
        }

        // Crear el gráfico secundario
        const ctx = document.getElementById("secondaryChartCanvas").getContext("2d");
        this.secondaryChart = new Chart(ctx, {
          type: "bar",
          data: {
            labels: data.map((point) => point.x),
            datasets: [
              {
                label: `Gráfico de ${this.selectedAxis.y} vs Clase`,
                data: data.map((point) => point.y),
                backgroundColor: "rgba(153, 102, 255, 0.6)",
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              x: {
                type: "category",
                title: {
                  display: true,
                  text: "Clase",
                },
              },
              y: {
                beginAtZero: true,
                title: {
                  display: true,
                  text: this.selectedAxis.y,
                },
              },
            },
          },
        });
      } catch (error) {
        console.error("Error al generar el gráfico secundario:", error);
      }
    },
  },
  async mounted() {
    // Generar los gráficos al cargar la página
    await this.generateChart();
  },
};
</script>

<style>
h2 {
  margin-top: 20px;
  margin-bottom: 20px;
}

label {
  margin-right: 10px;
}

button {
  margin-left: 10px;
}

canvas {
  max-width: 100%;
  height: auto;
}
</style>