export function formatChartData(data, config) {
  return {
    labels: data.map((item) => item.label || ""), // Asegúrate de manejar etiquetas vacías
    datasets: [
      {
        label: config.title || "Datos", // Usa el título de la configuración o un valor predeterminado
        data: data.map((item) => item.value || null), // Maneja valores nulos
        backgroundColor: config.backgroundColor || "rgba(75, 192, 192, 0.2)", // Color predeterminado
        borderColor: config.borderColor || "rgba(75, 192, 192, 1)", // Color de borde predeterminado
        borderWidth: config.borderWidth || 2, // Ancho de borde predeterminado
      },
    ],
  };
}