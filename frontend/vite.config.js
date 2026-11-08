import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// O proxy manda tudo que começa com /api para o Flask (porta 5000).
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: { "/api": "http://127.0.0.1:5000" },
  },
});
