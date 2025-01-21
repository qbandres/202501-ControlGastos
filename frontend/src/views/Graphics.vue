<template>
  <div>
    <Titulo />
    <Navbar />
    <h2>Gráficos X-Y</h2>

    <!-- Selección de columnas -->
    <div class="selectors">
      <label>X-Axis:</label>
      <select v-model="xAxis">
        <option v-for="column in columns" :key="column" :value="column">{{ column }}</option>
      </select>

      <label>Y-Axis:</label>
      <select v-model="yAxis">
        <option v-for="column in columns" :key="column" :value="column">{{ column }}</option>
      </select>

      <button @click="fetchChartData">Generar Gráfico</button>
    </div>

    <!-- Gráfico -->
    <div v-if="chartData.length">
      <canvas id="chart"></canvas>
    </div>
  </div>
</template>

<script>
import Chart from "chart.js/auto";
import axios from "axios";
import Titulo from "@/components/Titulo.vue";
import Navbar from "@/components/Navbar.vue";

export default {
  components: { Titulo, Navbar },
  data() {
    return {
      columns: ["fecha", "cantidad", "clase"], // Nombres de columnas disponibles
      xAxis: "",
      yAxis: "",
      chartData: [], // Datos para el gráfico
      chartInstance: null,
    };
  },
  methods: {
    async fetchChartData() {
      try {
        const response = await axios.post("http://localhost:8000/graficos/x-y", {
          x_axis: this.xAxis,
          y_axis: this.yAxis,
          filters: {}, // Agrega filtros si es necesario
        });
        this.chartData = response.data.data;
        this.renderChart();
      } catch (error) {
        console.error("Error al generar el gráfico:", error);
      }
    },
    renderChart() {
      if (this.chartInstance) {
        this.chartInstance.destroy(); // Destruye el gráfico previo
      }
      const ctx = document.getElementById("chart").getContext("2d");
      this.chartInstance = new Chart(ctx, {
        type: "line", // Cambia el tipo según el gráfico deseado
        data: {
          labels: this.chartData.map((point) => point.x),
          datasets: [
            {
              label: "Gráfico X-Y",
              data: this.chartData.map((point) => point.y),
              borderColor: "blue",
              backgroundColor: "lightblue",
            },
          ],
        },
      });
    },
  },
};
</script>