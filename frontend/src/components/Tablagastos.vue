<template>
  <div>
    <h2>Gastos</h2>

    <!-- Filtros -->
    <div class="filtros">
      <label for="usuario">Usuario:</label>
      <select v-model="filters.usuario" id="usuario">
        <option v-for="option in filterOptions.usuario" :key="option.value" :value="option.value">
          {{ option.label }}
        </option>
      </select>

      <label for="clase">Clase:</label>
      <select v-model="filters.clase" id="clase">
        <option v-for="option in filterOptions.clase" :key="option.value" :value="option.value">
          {{ option.label }}
        </option>
      </select>

      <label>Desde:</label>
      <input v-model="filters.rango_fecha_inicio" type="date" />

      <label>Hasta:</label>
      <input v-model="filters.rango_fecha_fin" type="date" />

      <label>Cantidad Mínima:</label>
      <input v-model="filters.rango_cantidad_min" type="number" placeholder="Mínima" />

      <label>Cantidad Máxima:</label>
      <input v-model="filters.rango_cantidad_max" type="number" placeholder="Máxima" />

      <button @click="applyFilters">Aplicar Filtros</button>
      <button @click="resetFilters">Restablecer</button>
    </div>

    <!-- Tabla de Resultados -->
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Usuario</th>
          <th>Clase</th>
          <th>Asignación</th>
          <th>Cantidad</th>
          <th>Tipo</th>
          <th>Locación</th>
          <th>Fecha</th>
          <th>Observaciones</th>
          <th>Método</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="gasto in gastos" :key="gasto.id">
          <td>{{ gasto.id }}</td>
          <td>{{ gasto.usuario }}</td>
          <td>{{ gasto.clase }}</td>
          <td>{{ gasto.asignacion }}</td>
          <td>{{ gasto.cantidad }}</td>
          <td>{{ gasto.tipo }}</td>
          <td>{{ gasto.locacion }}</td>
          <td>{{ new Date(gasto.fecha).toLocaleDateString() }}</td>
          <td>
            <button @click="toggleObservacion(gasto.id)">
              {{ showObservacion[gasto.id] ? "Ocultar" : "Mostrar" }}
            </button>
            <div v-if="showObservacion[gasto.id]">{{ gasto.observaciones }}</div>
          </td>
          <td>{{ gasto.metodo }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      gastos: [], // Lista de gastos recibida del backend
      filters: {
        usuario: "",
        clase: "",
        rango_fecha_inicio: "",
        rango_fecha_fin: "",
        rango_cantidad_min: null,
        rango_cantidad_max: null,
      },
      filterOptions: {
        usuario: [
          { value: "", label: "Todos" },
          { value: "YP", label: "Yovana" },
          { value: "AQ", label: "Andrés" },
        ],
        clase: [
          { value: "", label: "Todos" },
          { value: "Educación", label: "Educación" },
          { value: "Salud", label: "Salud" },
          { value: "Vestimenta", label: "Vestimenta" },
          { value: "Alimentos", label: "Alimentos" },
          { value: "Recreación", label: "Recreación" },
          { value: "Tecnología", label: "Tecnología" },
        ],
      },
      showObservacion: {}, // Estado para controlar qué observaciones están visibles
    };
  },
  methods: {
    async fetchGastos() {
      try {
        const backendUrl = import.meta.env.VITE_BACKEND_URL;  // Obtener la URL del backend desde el archivo .env
        const response = await axios.get(`${backendUrl}/tabla-gastos`);
        this.gastos = response.data.data; // Carga los últimos 20 gastos por defecto

        // Inicializa el estado de observaciones para todas las filas
        this.showObservacion = this.gastos.reduce((acc, gasto) => {
          acc[gasto.id] = false; // Por defecto, todas las observaciones están ocultas
          return acc;
        }, {});
      } catch (error) {
        console.error("Error al cargar los gastos:", error);
      }
    },
    toggleObservacion(id) {
      // Alterna la visibilidad de la observación para la fila específica
      this.showObservacion[id] = !this.showObservacion[id];
    },
    async applyFilters() {
      // Procesa y limpia los datos antes de enviarlos
      const cleanedFilters = {
        usuario: this.filters.usuario || null, // Si está vacío, lo envía como null
        clase: this.filters.clase || null,
        rango_fecha_inicio: this.filters.rango_fecha_inicio || null,
        rango_fecha_fin: this.filters.rango_fecha_fin || null,
        rango_cantidad_min:
          this.filters.rango_cantidad_min !== null
            ? Number(this.filters.rango_cantidad_min)
            : null,
        rango_cantidad_max:
          this.filters.rango_cantidad_max !== null
            ? Number(this.filters.rango_cantidad_max)
            : null,
      };

      try {
        const backendUrl = import.meta.env.VITE_BACKEND_URL;  // Obtener la URL del backend desde el archivo .env
        const response = await axios.post(
          `${backendUrl}/tabla-gastos`,
          cleanedFilters
        );
        this.gastos = response.data.data; // Actualiza la tabla con los resultados filtrados

        // Actualiza el estado de observaciones después de aplicar los filtros
        this.showObservacion = this.gastos.reduce((acc, gasto) => {
          acc[gasto.id] = false;
          return acc;
        }, {});
      } catch (error) {
        console.error("Error al aplicar filtros:", error);
      }
    },
    resetFilters() {
      this.filters = {
        usuario: "",
        clase: "",
        rango_fecha_inicio: "",
        rango_fecha_fin: "",
        rango_cantidad_min: null,
        rango_cantidad_max: null,
      };
      this.fetchGastos(); // Recarga los últimos 20 gastos
    },
  },
  async created() {
    await this.fetchGastos(); // Carga inicial de los últimos 20 gastos
  },
};
</script>