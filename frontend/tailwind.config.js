/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        saga: {
          purple: "#8B5CF6",
          gold: "#F59E0B",
          sky: "#38BDF8",
          ink: "#0F172A",
          cloud: "#F8FAFC"
        }
      },
      fontFamily: {
        display: ["var(--font-space-grotesk)", "sans-serif"],
        body: ["var(--font-inter)", "sans-serif"]
      },
      boxShadow: {
        glow: "0 10px 40px rgba(139, 92, 246, 0.25)"
      }
    }
  },
  plugins: []
};
