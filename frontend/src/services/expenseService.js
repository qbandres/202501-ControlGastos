import axios from "axios";

const backendUrl = import.meta.env.VITE_BACKEND_URL;

export default {
    /**
     * Obtiene todos los gastos sin filtros
     * @returns {Promise} Respuesta de axios con los datos
     */
    getExpenses() {
        return axios.get(`${backendUrl}/tabla-gastos`);
    },

    /**
     * Filtra los gastos según los criterios proporcionados
     * @param {Object} payload - Objeto con los filtros (usuario, clase, fechas, etc.)
     * @returns {Promise} Respuesta de axios con los datos filtrados
     */
    filterExpenses(payload) {
        return axios.post(`${backendUrl}/tabla-gastos`, payload);
    },

    addExpense(expense) {
        return axios.post(`${backendUrl}/agregar-gasto`, expense);
    },

    updateExpense(id, expense) {
        return axios.put(`${backendUrl}/modificar/${id}`, expense);
    },

    deleteExpense(id) {
        return axios.delete(`${backendUrl}/modificar/${id}`);
    },

    getDailyTrends(params) {
        return axios.post(`${backendUrl}/tendencias/tendencias_diarias`, params);
    },

    getMonthlyTrends(params) {
        return axios.post(`${backendUrl}/tendencias/tendencias_mensuales`, params);
    },

    getXYChartData(params) {
        return axios.post(`${backendUrl}/graficos/x-y`, params);
    },

    getDynamicDateMonthData(params) {
        return axios.post(`${backendUrl}/graficos_dinamicos/datos_fecha_mes`, params);
    },

    getDynamicDateDayData(params) {
        return axios.post(`${backendUrl}/graficos_dinamicos/datos_fecha_dia`, params);
    },
};
