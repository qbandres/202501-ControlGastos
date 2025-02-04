export function formatChartData(data, config) {
    return {
      labels: data.map((item) => item.label),
      datasets: [
        {
          label: config.title || "Datos",
          data: data.map((item) => item.value),
          backgroundColor: config.backgroundColor,
          borderColor: config.borderColor,
          borderWidth: config.borderWidth,
        },
      ],
    };
  }