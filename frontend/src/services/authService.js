import axios from "axios";

const backendUrl = import.meta.env.VITE_BACKEND_URL;

export default {
    login(credentials) {
        return axios.post(`${backendUrl}/login`, credentials);
    },
};
