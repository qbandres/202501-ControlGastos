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
        <select v-model="selectedGasto.usuario">
          <option v-for="usuario in usuarios" :key="usuario" :value="usuario">
            {{ usuario }}
          </option>
        </select>

        <label>Clase:</label>
        <select v-model="selectedGasto.clase">
          <option v-for="clase in clases" :key="clase" :value="clase">
            {{ clase }}
          </option>
        </select>

        <label>Asignación:</label>
        <select v-model="selectedGasto.asignacion">
          <option v-for="asignacion in asignaciones" :key="asignacion" :value="asignacion">
            {{ asignacion }}
          </option>
        </select>

        <label>Cantidad:</label>
        <input v-model="selectedGasto.cantidad" type="number" step="any" />

        <label>Tipo:</label>
        <select v-model="selectedGasto.tipo">
          <option v-for="tipo in tipos" :key="tipo" :value="tipo">
            {{ tipo }}
          </option>
        </select>

        <label>Método:</label>
        <select v-model="selectedGasto.metodo">
          <option v-for="metodo in metodos" :key="metodo" :value="metodo">
            {{ metodo }}
          </option>
        </select>

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
      selectedGasto: {
        usuario: "YP",
        clase: "",
        asignacion: "",
        cantidad: 0,
        tipo: "",
        metodo: "Efectivo",
        fecha: new Date().toISOString().slice(0, 10), // Fecha actual
        observaciones: "",
      }, // Instancia seleccionada para modificar
      usuarios: ["AQ", "YP"],
      clases: [
        "Educación",
        "Salud",
        "Vestimenta",
        "Alimentos",
        "Recreacion",
        "Sabina",
        "Isaac",
        "Tecnologia",
        "Servicios",
        "Restaurant",
        "transf_YP",
        "centroComercial",
        "Combustible",
        "Gustitos",
      ],
      asignaciones: [
        "Andrés",
        "Yovana",
        "Alonso",
        "Lucia",
        "Claudia",
        "Fam_Andres",
        "Fam_QP",
        "Fam_Yovana",
      ],
      tipos: ["Ingreso", "Egreso"],
      metodos: ["Efectivo", "Tarjeta"],
    };
  },
  methods: {
    async fetchGastos() {
      try {
        // Usamos la variable de entorno para obtener la URL del backend
        const backendUrl = import.meta.env.VITE_BACKEND_URL;

        const response = await axios.get(`${backendUrl}/tabla-gastos`);
        this.gastos = response.data.data;
      } catch (error) {
        console.error("Error al cargar los gastos:", error);
      }
    },
    async applyFilters() {
      try {
        const backendUrl = import.meta.env.VITE_BACKEND_URL;

        const response = await axios.post(`${backendUrl}/tabla-gastos`, this.filters);
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
        const backendUrl = import.meta.env.VITE_BACKEND_URL;

        await axios.put(`${backendUrl}/modificar/${this.selectedGasto.id}`, this.selectedGasto);
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
          const backendUrl = import.meta.env.VITE_BACKEND_URL;

          await axios.delete(`${backendUrl}/modificar/${id}`);
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

<style scoped>
/* Diseño responsivo */
h2 {
  margin-bottom: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th, td {
  padding: 10px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

button {
  margin-top: 10px;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

.filtros {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.filtros label {
  margin-right: 10px;
}

.filtros input, .filtros button {
  padding: 8px;
  margin-bottom: 10px;
}

form {
  display: flex;
  flex-direction: column;
  gap: 15px;
  width: 100%;
  max-width: 500px;
  margin-top: 20px;
}

select, input, textarea {
  padding: 10px;
  border-radius: 4px;
  border: 1px solid #ccc;
}

/* Media Queries */
@media (max-width: 768px) {
  .filtros {
    flex-direction: column;
  }

  table {
    font-size: 0.9rem;
  }

  form {
    width: 100%;
  }

  button {
    width: 100%;
  }
}
</style>