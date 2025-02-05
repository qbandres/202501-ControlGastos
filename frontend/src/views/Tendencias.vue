<template>
  <div>
    <Titulo />
    <Navbar />
    <h2>Tendencias de Gastos</h2>

    <div>
      <!-- Gráfico de tendencia diaria -->
      <h3>Tendencia Diaria (Promedio y Proyección)</h3>
      <Graficos4D 
        type="line" 
        :data="tendenciaDiaria" 
        :config="{ title: 'Tendencia Diaria (Promedio y Proyección)' }" 
      />

      <!-- Gráfico de tendencia mensual -->
      <h3>Tendencia Mensual (Promedio y Proyección)</h3>
      <Graficos4D 
        type="line" 
        :data="tendenciaMensual" 
        :config="{ title: 'Tendencia Mensual (Promedio y Proyección)' }" 
      />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Titulo from "@/components/Titulo.vue";
import Navbar from "@/components/Navbar.vue";
import Graficos4D from "@/components/Graficos4D.vue";

export default {
  components: { Titulo, Navbar, Graficos4D },
  data() {
    return {
      tendenciaDiaria: [], // Datos para la tendencia diaria
      tendenciaMensual: [] // Datos para la tendencia mensual
    };
  },
  methods: {
    // Obtener datos para la tendencia diaria
    async fetchTendenciaDiaria() {
      try {
        const backendUrl = import.meta.env.VITE_BACKEND_URL;
        const response = await axios.post(`${backendUrl}/tendencias/tendencias_diarias`, {
          order: "asc",
          n_ultimos_dias: 300
        });
        this.tendenciaDiaria = response.data.data;
        console.log("Datos recibidos para tendencia diaria:", this.tendenciaDiaria);
      } catch (error) {
        console.error("Error al obtener la tendencia diaria:", error);
      }
    },
    // Obtener datos para la tendencia mensual
    async fetchTendenciaMensual() {
      try {
        const backendUrl = import.meta.env.VITE_BACKEND_URL;
        const response = await axios.post(`${backendUrl}/tendencias/tendencias_mensuales`, {
          order: "asc",
          n_ultimos_meses: 12
        });
        this.tendenciaMensual = response.data.data;
        console.log("Datos recibidos para tendencia mensual:", this.tendenciaMensual);
      } catch (error) {
        console.error("Error al obtener la tendencia mensual:", error);
      }
    }
  },
  async mounted() {
    // Llamar a los métodos para obtener los datos al cargar el componente
    await this.fetchTendenciaDiaria();
    await this.fetchTendenciaMensual();
  }
};
</script>

<style>
h2 {
  margin-bottom: 20px;
}

h3 {
  margin-top: 30px;
}

.chart-container {
  width: 100%;
  max-width: 100%;
  height: 400px;
  margin-bottom: 30px;
}

canvas {
  width: 100% !important;
  height: 100% !important;
}

@media (max-width: 768px) {
  h2 {
    font-size: 1.5rem;
  }

  h3 {
    font-size: 1.2rem;
  }

  .chart-container {
    height: 300px; /* Ajuste para pantallas pequeñas */
  }

  canvas {
    height: 300px !important; /* Ajuste para pantallas pequeñas */
  }
}
</style>