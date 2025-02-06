<template>
  <div class="chart-container">
    <canvas ref="chart"></canvas>
  </div>
</template>

<script>
import { Chart, registerables } from "chart.js";

// Registra los elementos necesarios de Chart.js
Chart.register(...registerables);

export default {
  props: {
    type: {
      type: String,
      required: true,
    },
    data: {
      type: Array,
      required: true,
    },
    config: {
      type: Object,
      default: () => ({}),
    },
  },
  data() {
    return {
      chartInstance: null, // Referencia al gráfico actual
    };
  },
  mounted() {
    this.createChart(); // Crear gráfico al montar el componente
  },
  watch: {
    data: {
      immediate: true,
      handler(newData) {
        if (newData && newData.length > 0) {
          this.createChart();
        }
      },
    },
  },
  methods: {
    createChart() {
      // Destruir gráfico existente si ya está creado
      if (this.chartInstance) {
        this.chartInstance.destroy();
      }

      const ctx = this.$refs.chart.getContext("2d");

      // Filtrar valores nulos para evitar errores en el gráfico
      const labels = this.data.map((point) => point.label || "");
      const originalValues = this.data.map((point) =>
        point.value !== null ? point.value : NaN
      );
      const movingAverage = this.data.map((point) =>
        point.promedio !== null ? point.promedio : NaN
      );
      const forecastValues = this.data.map((point) =>
        point.forecast !== null ? point.forecast : NaN
      );

      // Crear el gráfico
      this.chartInstance = new Chart(ctx, {
        type: this.type,
        data: {
          labels: labels,
          datasets: [
            {
              label: "Valor Original",
              data: originalValues,
              borderColor: "blue",
              backgroundColor: "rgba(0, 0, 255, 0.1)",
              tension: 0.4,
            },
            {
              label: "Promedio Móvil",
              data: movingAverage,
              borderColor: "green",
              borderDash: [5, 5],
              backgroundColor: "rgba(0, 255, 0, 0.1)",
              tension: 0.4,
            },
            {
              label: "Proyección",
              data: forecastValues,
              borderColor: "red",
              borderDash: [10, 5],
              backgroundColor: "rgba(255, 0, 0, 0.1)",
              tension: 0.4,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            title: {
              display: true,
              text: this.config.title || "Gráfico",
            },
          },
          scales: {
            x: {
              title: {
                display: true,
                text: "Tiempo",
              },
            },
            y: {
              title: {
                display: true,
                text: "Cantidad",
              },
            },
          },
        },
      });
    },
  },
};
</script>

<style scoped>
.chart-container {
  position: relative;
  height: 400px;
  width: 100%;
}
</style>