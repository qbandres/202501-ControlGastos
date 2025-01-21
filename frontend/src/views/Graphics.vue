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

    <!-- Contenedor del gráfico -->
    <div style="width: 100%; height: 400px;">
      <canvas id="chartCanvas"></canvas>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Titulo from "@/components/Titulo.vue";
import Navbar from "@/components/Navbar.vue";
import Chart from "chart.js/auto";
import "chartjs-adapter-date-fns"; // Importa el adaptador de fechas

export default {
  components: { Titulo, Navbar },
  data() {
    return {
      chart: null, // Instancia del gráfico
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
          start: "", // Rango de fecha inicial
          end: "", // Rango de fecha final
        },
      },
    };
  },
  methods: {
    async generateChart() {
      try {
        const response = await axios.post("http://localhost:8000/graficos/x-y", {
          x_axis: this.selectedAxis.x,
          y_axis: this.selectedAxis.y,
          filters: this.filters,
        });

        const { data } = response.data;

        console.log("Datos recibidos del backend:", data);

        // Si ya existe un gráfico, destrúyelo
        if (this.chart) {
          this.chart.destroy();
        }

        // Crear un nuevo gráfico con los datos recibidos
        const ctx = document.getElementById("chartCanvas").getContext("2d");
        this.chart = new Chart(ctx, {
          type: "bar", // Cambiado a gráfico de barras
          data: {
            labels: data.map((point) => point.x), // Usa los valores de X como etiquetas
            datasets: [
              {
                label: `Gráfico de ${this.selectedAxis.y} vs ${this.selectedAxis.x}`,
                data: data.map((point) => point.y), // Usa los valores de Y como datos
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
                beginAtZero: true, // Asegura que el eje Y comience en 0
                title: {
                  display: true,
                  text: this.selectedAxis.y,
                },
              },
            },
          },
        });
      } catch (error) {
        console.error("Error al generar el gráfico:", error);
      }
    },
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