import { createApp } from "vue"; // Importa la función para crear una aplicación Vue
import { createPinia } from "pinia"; // Importa la función para crear una nueva instancia de Pinia, el sistema de gestión de estado
import App from "./App.vue";  // Importa el componente raíz de la aplicación (App.vue)
import router from "./router"; // Importa la configuración del router (rutas definidas en router/index.js)

const app = createApp(App); // Crea una instancia de la aplicación Vue, usando el componente raíz App.vue
const pinia = createPinia();  // Crea una nueva instancia de Pinia para la gestión del estado global

app.use(pinia);  // Registra Pinia como un plugin de la aplicación Vue para que esté disponible en toda la aplicación
app.use(router);  // Registra el router como un plugin de la aplicación para habilitar la navegación y manejo de rutas

// Monta la aplicación en el elemento HTML con el id "app"
// Este id debe estar definido en el archivo index.html, por ejemplo: <div id="app"></div>
app.mount("#app");