<template>
  <div class="tabla-gastos-container">
    <!-- 📌 Título con total de registros y suma total -->
    <h2>Gastos (Total: {{ totalRegistros }} registros, Suma: {{ totalCantidad }})</h2>

    <!-- 🔹 Filtros -->
    <div class="filtros-container">
      <label>
        Usuario:
        <select v-model="filtros.usuario">
          <option value="">Todos</option>
          <option v-for="usuario in usuarios" :key="usuario" :value="usuario">
            {{ usuario }}
          </option>
        </select>
      </label>
      <label>
        Clase:
        <select v-model="filtros.clase">
          <option value="">Todos</option>
          <option v-for="clase in clases" :key="clase" :value="clase">
            {{ clase }}
          </option>
        </select>
      </label>
      <label>
        Desde:
        <input type="date" v-model="filtros.rango_fecha_inicio" />
      </label>
      <label>
        Hasta:
        <input type="date" v-model="filtros.rango_fecha_fin" />
      </label>
      <label>
        Cantidad Mínima:
        <input type="number" v-model="filtros.rango_cantidad_min" />
      </label>
      <label>
        Cantidad Máxima:
        <input type="number" v-model="filtros.rango_cantidad_max" />
      </label>
      <button @click="aplicarFiltros">Aplicar Filtros</button>
      <button @click="restablecerFiltros">Restablecer</button>
    </div>

    <!-- 🔹 Tabla de gastos -->
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
          <td>{{ gasto.user ? gasto.user.username : (gasto.user_id || 'N/A') }}</td>
          <td>{{ gasto.clase }}</td>
          <td>{{ gasto.asignacion }}</td>
          <td>{{ gasto.cantidad }}</td>
          <td>{{ gasto.tipo }}</td>
          <td>{{ gasto.locacion }}</td>
          <td>{{ gasto.fecha ? gasto.fecha.split("T")[0] : '' }}</td>
          <td>{{ gasto.observaciones }}</td>
          <td>{{ gasto.metodo }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import expenseService from "@/services/expenseService";

export default {
  data() {
    return {
      gastos: [], // Datos de la tabla
      totalCantidad: 0, // Suma total de gastos
      totalRegistros: 0, // Cantidad de registros mostrados
      filtros: {
        usuario: "",
        clase: "",
        rango_fecha_inicio: "",
        rango_fecha_fin: "",
        rango_cantidad_min: null,
        rango_cantidad_max: null,
      },
      usuarios: [], // Lista de usuarios para el filtro
      clases: [], // Lista de clases para el filtro
    };
  },
  methods: {
    async cargarGastos() {
      try {
        const response = await expenseService.getExpenses();
        this.gastos = response.data.data;
        this.totalCantidad = response.data.total_cantidad;
        this.totalRegistros = response.data.total_registros;

        this.procesarFiltrosUnicos();
      } catch (error) {
        console.error("Error al cargar los gastos:", error);
      }
    },
    async aplicarFiltros() {
      const payload = {
        usuario: this.filtros.usuario || null,
        clase: this.filtros.clase || null,
        rango_fecha_inicio: this.filtros.rango_fecha_inicio || null,
        rango_fecha_fin: this.filtros.rango_fecha_fin || null,
        rango_cantidad_min:
          this.filtros.rango_cantidad_min !== null
            ? Number(this.filtros.rango_cantidad_min)
            : null,
        rango_cantidad_max:
          this.filtros.rango_cantidad_max !== null
            ? Number(this.filtros.rango_cantidad_max)
            : null,
      };

      console.log("Payload enviado al backend:", payload);

      try {
        const response = await expenseService.filterExpenses(payload);
        this.gastos = response.data.data;
        this.totalCantidad = response.data.total_cantidad;
        this.totalRegistros = response.data.total_registros;
      } catch (error) {
        console.error("Error al aplicar filtros:", error);
      }
    },
    procesarFiltrosUnicos() {
      // 📌 Obtener listas únicas de usuarios y clases en una sola consulta
      const uniqueUsuarios = new Set();
      const uniqueClases = new Set();
      this.gastos.forEach((gasto) => {
        // Adaptar a la nueva estructura: user puede ser un objeto o un ID
        const usuarioNombre = gasto.user ? gasto.user.username : (gasto.user_id ? String(gasto.user_id) : null);
        if (usuarioNombre) uniqueUsuarios.add(usuarioNombre);
        
        if (gasto.clase) uniqueClases.add(gasto.clase);
      });
      this.usuarios = Array.from(uniqueUsuarios);
      this.clases = Array.from(uniqueClases);
    },
    restablecerFiltros() {
      this.filtros = {
        usuario: "",
        clase: "",
        rango_fecha_inicio: "",
        rango_fecha_fin: "",
        rango_cantidad_min: null,
        rango_cantidad_max: null,
      };
      this.cargarGastos();
    },
  },
  async mounted() {
    await this.cargarGastos();
  },
};
</script>

<style scoped>
.tabla-gastos-container {
  width: 100%;
  margin: auto;
}

.filtros-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
}

.filtros-container label {
  display: flex;
  flex-direction: column;
  font-size: 0.9rem;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th, td {
  padding: 10px;
  border: 1px solid #ddd;
  text-align: left;
}

th {
  background-color: #f4f4f4;
}

button {
  padding: 8px 15px;
  border: none;
  background-color: #007bff;
  color: #fff;
  cursor: pointer;
  border-radius: 4px;
  font-size: 0.9rem;
}

button:hover {
  background-color: #0056b3;
}
</style>