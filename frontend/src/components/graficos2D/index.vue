<template>
  <div class="chart-container">
    <!-- Título del gráfico -->
    <h3>{{ config.title }}</h3>

    <!-- Componente dinámico según el tipo de gráfico -->
    <component
      :is="chartComponent"
      :chart-data="chartData"
      :options="chartOptions"
      class="chart"
    />
  </div>
</template>

<script>
import { defineComponent, computed } from "vue";
import Bar from "./tipos/Bar.vue";
import Line from "./tipos/Line.vue";
import Scatter from "./tipos/Scatter.vue";
import defaultConfig from "./config.js";
import { formatChartData } from "./utils.js";

export default defineComponent({
  components: { Bar, Line, Scatter },
  props: {
    type: { type: String, required: true }, // "bar", "line", "scatter"
    data: { type: Array, required: true },  // [{ label, value }]
    config: { type: Object, default: () => defaultConfig }, // Configuración personalizada
  },
  setup(props) {
    // 📌 Elegir el componente según el tipo de gráfico
    const chartComponent = computed(() => {
      const charts = { bar: Bar, line: Line, scatter: Scatter };
      return charts[props.type] || Bar;
    });

    // 📌 Transformar los datos para Chart.js
    const chartData = computed(() => formatChartData(props.data, props.config));

    // 📌 Opciones del gráfico (puede extenderse)
    const chartOptions = computed(() => ({
      responsive: true,
      maintainAspectRatio: false, // Permitir que se ajuste al contenedor
      plugins: {
        legend: {
          display: true,
          position: "top",
        },
      },
      scales: {
        x: {
          title: {
            display: !!props.config.xAxisTitle, // Mostrar solo si está definido
            text: props.config.xAxisTitle || "Eje X",
          },
          grid: {
            display: props.config.showXAxisGrid || false, // Mostrar cuadrícula si está configurado
          },
          ticks: {
            autoSkip: true, // Omitir etiquetas automáticamente si son muchas
            maxRotation: props.config.maxRotation || 45, // Rotación máxima para etiquetas
            minRotation: props.config.minRotation || 0, // Rotación mínima para etiquetas
          },
        },
        y: {
          title: {
            display: !!props.config.yAxisTitle, // Mostrar solo si está definido
            text: props.config.yAxisTitle || "Eje Y",
          },
          grid: {
            color: "rgba(200, 200, 200, 0.2)",
          },
        },
      },
    }));

    return { chartComponent, chartData, chartOptions };
  },
});
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

.chart {
  width: 100%;
  height: 100%;
}
</style>