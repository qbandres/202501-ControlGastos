<template>
  <div>
    <!-- Componente para mostrar el título general de la página -->
    <Titulo />
    
    <!-- Componente para la barra de navegación -->
    <Navbar />
    
    <h2>Agregar Gasto</h2>

    <!-- Formulario para agregar un nuevo gasto -->
    <form @submit.prevent="addExpense">
      <div>
        <label for="usuario">Usuario:</label>
        <select v-model="newExpense.usuario" id="usuario" required>
          <option v-for="usuario in usuarios" :key="usuario" :value="usuario">
            {{ usuario }}
          </option>
        </select>
      </div>

      <div>
        <label for="clase">Clase:</label>
        <select v-model="newExpense.clase" id="clase" required>
          <option v-for="clase in clases" :key="clase" :value="clase">
            {{ clase }}
          </option>
        </select>
      </div>

      <div>
        <label for="asignacion">Asignación:</label>
        <select v-model="newExpense.asignacion" id="asignacion" required>
          <option v-for="asignacion in asignaciones" :key="asignacion" :value="asignacion">
            {{ asignacion }}
          </option>
        </select>
      </div>

      <div>
        <label for="cantidad">Cantidad:</label>
        <input v-model="newExpense.cantidad" type="number" id="cantidad" step="any" required />
      </div>

      <div>
        <label for="tipo">Tipo:</label>
        <select v-model="newExpense.tipo" id="tipo" required>
          <option v-for="tipo in tipos" :key="tipo" :value="tipo">
            {{ tipo }}
          </option>
        </select>
      </div>

      <div>
        <label for="locacion">Locación:</label>
        <input v-model="newExpense.locacion" type="text" id="locacion" required />
      </div>

      <div>
        <label for="fecha">Fecha:</label>
        <input v-model="newExpense.fecha" type="date" id="fecha" required />
      </div>

      <div>
        <label for="metodo">Método:</label>
        <select v-model="newExpense.metodo" id="metodo" required>
          <option v-for="metodo in metodos" :key="metodo" :value="metodo">
            {{ metodo }}
          </option>
        </select>
      </div>

      <div>
        <label for="observaciones">Observaciones:</label>
        <textarea v-model="newExpense.observaciones" id="observaciones"></textarea>
      </div>

      <!-- Botón para confirmar el gasto -->
      <button type="submit">Confirmar Gasto</button>
    </form>
  </div>
</template>

<script>
import axios from "axios";
import Titulo from "@/components/Titulo.vue";
import Navbar from "@/components/Navbar.vue";

export default {
  components: { Titulo, Navbar },
  data() {
    return {
      newExpense: {
        usuario: 'YP', // Valor por defecto
        clase: '',
        asignacion: '',
        cantidad: '',
        tipo: 'Egreso', // Valor por defecto
        locacion: 'Lima', // Valor por defecto
        fecha: '',
        metodo: 'Efectivo',
        observaciones: ''
      },
      // Opciones para los selectores
      usuarios: ["AQ", "YP"],
      clases: [
        "Educación", "Salud", "Vestimenta", "Alimentos", "Recreación", "Tecnología", 
        "Sabina", "Isaac", "Servicios", "Restaurant", "transf_YP", "centroComercial", 
        "Combustible", "Gustitos"
      ],
      asignaciones: [
        "Andrés", "Yovana", "Alonso", "Lucia", "Claudia", "Fam_Andres", 
        "Fam_QP", "Fam_Yovana"
      ],
      tipos: ["Ingreso", "Egreso"],
      metodos: ["Efectivo", "Tarjeta"]
    };
  },
  methods: {
    async addExpense() {
      // Validar que todos los campos requeridos están completos
      if (!this.newExpense.usuario || !this.newExpense.clase || !this.newExpense.cantidad) {
        alert('Por favor, complete todos los campos obligatorios.');
        return;
      }

      try {
        console.log("Datos enviados al backend:", this.newExpense); // Ver los datos antes de enviarlos

        // Obtener la URL del backend desde la variable de entorno
        const backendUrl = import.meta.env.VITE_BACKEND_URL;

        // Enviar el gasto al backend
        const response = await axios.post(`${backendUrl}/agregar-gasto`, this.newExpense);
        console.log("Gasto agregado:", response.data);

        // Limpiar el formulario después de confirmar
        this.newExpense = {
          usuario: 'YP', // Valor por defecto
          clase: '',
          asignacion: '',
          cantidad: '',
          tipo: 'Egreso', // Valor por defecto
          locacion: 'Lima', // Valor por defecto
          fecha: '',
          metodo: 'Efectivo',
          observaciones: ''
        };
      } catch (error) {
        console.error("Error al confirmar el gasto:", error.response ? error.response.data : error);
      }
    }
  }
};
</script>

<style>
/* Aquí puedes agregar tu CSS personalizado */
</style>