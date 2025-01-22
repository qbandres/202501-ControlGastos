<template>
  <div>
    <Titulo />
    <Navbar />
    <h2>Tendencias de Gastos</h2>

    <div>
      <!-- Gráfico de tendencia diaria -->
      <h3>Tendencia Diaria</h3>
      <div id="tendenciaDiaria" style="width: 100%; height: 400px;">
        <canvas id="dailyTrendChart"></canvas>
      </div>

      <!-- Gráfico de tendencia mensual -->
      <h3>Tendencia Mensual</h3>
      <div id="tendenciaMensual" style="width: 100%; height: 400px;">
        <canvas id="monthlyTrendChart"></canvas>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Titulo from "@/components/Titulo.vue";
import Navbar from "@/components/Navbar.vue";
import Chart from "chart.js/auto";

export default {
  components: { Titulo, Navbar },
  methods: {
    // Obtener datos para la tendencia diaria
    async fetchDailyTrend() {
      try {
        const backendUrl = import.meta.env.VITE_BACKEND_URL;  // Obtener la URL del backend desde el archivo .env
        const response = await axios.get(`${backendUrl}/tendencias/diarias`);
        const data = response.data;

        console.log("Datos de tendencia diaria:", data);

        const ctx = document.getElementById("dailyTrendChart").getContext("2d");
        new Chart(ctx, {
          type: "line",
          data: {
            labels: data.map((point) => point.fecha), // Fechas como etiquetas
            datasets: [
              {
                label: "Tendencia diaria",
                data: data.map((point) => point.cantidad), // Cantidades como datos
                borderColor: "rgba(75, 192, 192, 1)",
                backgroundColor: "rgba(75, 192, 192, 0.2)",
                tension: 0.4,
              },
            ],
          },
          options: {
            responsive: true,
            scales: {
              x: { title: { display: true, text: "Fecha" } },
              y: { title: { display: true, text: "Cantidad ($)" } },
            },
          },
        });
      } catch (error) {
        console.error("Error al obtener la tendencia diaria:", error);
      }
    },

    // Obtener datos para la tendencia mensual
    async fetchMonthlyTrend() {
      try {
        const backendUrl = import.meta.env.VITE_BACKEND_URL;  // Obtener la URL del backend desde el archivo .env
        const response = await axios.get(`${backendUrl}/tendencias/mensuales`);
        const data = response.data;

        console.log("Datos de tendencia mensual:", data);

        const ctx = document.getElementById("monthlyTrendChart").getContext("2d");
        new Chart(ctx, {
          type: "bar",
          data: {
            labels: data.map((point) => point.mes), // Meses como etiquetas
            datasets: [
              {
                label: "Tendencia mensual",
                data: data.map((point) => point.cantidad), // Cantidades como datos
                backgroundColor: "rgba(153, 102, 255, 0.6)",
              },
            ],
          },
          options: {
            responsive: true,
            scales: {
              x: { title: { display: true, text: "Mes" } },
              y: { title: { display: true, text: "Cantidad ($)" } },
            },
          },
        });
      } catch (error) {
        console.error("Error al obtener la tendencia mensual:", error);
      }
    },
  },

  // Montar los gráficos al cargar la vista
  async mounted() {
    await this.fetchDailyTrend();
    await this.fetchMonthlyTrend();
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

canvas {
  max-width: 100%;
  height: auto;
}
</style>