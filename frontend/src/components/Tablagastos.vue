<template>
    <div>
      <h2>Tabla de Gastos</h2>
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
            <td>{{ gasto.fecha }}</td>
            <td>{{ gasto.observaciones }}</td>
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
        gastos: [],
      };
    },
    async created() {
      try {
        const response = await axios.get("http://localhost:8000/tabla-gastos");
        this.gastos = response.data.data;
      } catch (error) {
        console.error("Error al cargar los gastos:", error);
      }
    },
  };
  </script>