<template>
  <div>
    <!-- Título de la página -->
    <Titulo />

    <!-- Navbar de navegación -->
    <Navbar />

    <h2>Modificar Gastos</h2>

    <!-- Filtros -->
    <div class="filtros">
      <label>Desde:</label>
      <input v-model="filters.rango_fecha_inicio" type="date" />

      <label>Hasta:</label>
      <input v-model="filters.rango_fecha_fin" type="date" />

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
          <th>Fecha</th>
          <th>Observaciones</th>
          <th>Acciones</th>
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
          <td>{{ new Date(gasto.fecha).toLocaleDateString() }}</td>
          <td>{{ gasto.observaciones }}</td>
          <td>
            <button @click="editGasto(gasto)">Modificar</button>
            <button @click="confirmDelete(gasto.id)">Eliminar</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Formulario de Modificación -->
    <div v-if="selectedGasto">
      <h3>Modificar Gasto</h3>
      <form @submit.prevent="confirmEdit">
        <label>Usuario:</label>
        <input v-model="selectedGasto.usuario" type="text" />

        <label>Clase:</label>
        <input v-model="selectedGasto.clase" type="text" />

        <label>Asignación:</label>
        <input v-model="selectedGasto.asignacion" type="text" />

        <label>Cantidad:</label>
        <input v-model="selectedGasto.cantidad" type="number" step="any" />

        <label>Tipo:</label>
        <input v-model="selectedGasto.tipo" type="text" />

        <label>Fecha:</label>
        <input v-model="selectedGasto.fecha" type="date" />

        <label>Observaciones:</label>
        <textarea v-model="selectedGasto.observaciones"></textarea>

        <button type="submit">Confirmar Cambios</button>
        <button @click="cancelEdit">Cancelar</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Titulo from "@/components/Titulo.vue";
import Navbar from "@/components/Navbar.vue";

export default {
  components: {
    Titulo,
    Navbar,
  },
  data() {
    return {
      gastos: [], // Lista de gastos recibida del backend
      filters: {
        rango_fecha_inicio: "",
        rango_fecha_fin: "",
      },
      selectedGasto: null, // Instancia seleccionada para modificar
    };
  },
  methods: {
    async fetchGastos() {
      try {
        const response = await axios.get("http://localhost:8000/tabla-gastos");
        this.gastos = response.data.data;
      } catch (error) {
        console.error("Error al cargar los gastos:", error);
      }
    },
    async applyFilters() {
      try {
        const response = await axios.post("http://localhost:8000/tabla-gastos", this.filters);
        this.gastos = response.data.data;
      } catch (error) {
        console.error("Error al aplicar filtros:", error);
      }
    },
    resetFilters() {
      this.filters = { rango_fecha_inicio: "", rango_fecha_fin: "" };
      this.fetchGastos();
    },
    editGasto(gasto) {
      this.selectedGasto = { ...gasto }; // Clona el gasto seleccionado
    },
    async confirmEdit() {
      try {
        await axios.put(`http://localhost:8000/modificar/${this.selectedGasto.id}`, this.selectedGasto);
        alert("Gasto modificado exitosamente");
        this.selectedGasto = null;
        this.fetchGastos(); // Actualiza la tabla
      } catch (error) {
        console.error("Error al modificar el gasto:", error);
      }
    },
    cancelEdit() {
      this.selectedGasto = null;
    },
    async confirmDelete(id) {
      if (confirm("¿Está seguro de que desea eliminar este gasto?")) {
        try {
          await axios.delete(`http://localhost:8000/modificar/${id}`);
          alert("Gasto eliminado exitosamente");
          this.fetchGastos();
        } catch (error) {
          console.error("Error al eliminar el gasto:", error);
        }
      }
    },
  },
  async created() {
    await this.fetchGastos();
  },
};
</script>