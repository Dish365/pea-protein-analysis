// Configuration file for chart-related settings and defaults

export const chartConfig = {
  // Default chart dimensions
  defaultWidth: 800,
  defaultHeight: 400,

  // Chart margins
  margin: {
    top: 20,
    right: 30,
    bottom: 40,
    left: 50,
  },

  // Default chart colors
  colors: {
    primary: "#4C9AFF",
    secondary: "#FF5630",
    tertiary: "#36B37E",
  },

  // Animation settings
  animation: {
    duration: 750,
    easing: "cubic-bezier(0.4, 0, 0.2, 1)",
  },

  // Axis configuration
  axis: {
    tickSize: 5,
    tickPadding: 5,
    strokeWidth: 1,
  },
};

export default chartConfig;
