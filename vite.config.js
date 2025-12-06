import { resolve } from 'path'
import { defineConfig } from 'vite'

export default defineConfig({
  build: {
    rollupOptions: {
      input: {
        // Aquí listamos todas las páginas de tu sitio
        main: resolve(__dirname, 'index.html'),
        circuits: resolve(__dirname, 'circuits.html'),
        about: resolve(__dirname, 'about.html'),
        login: resolve(__dirname, 'login.html'),
        sumergete: resolve(__dirname, 'sumergete.html'),
        
        // Agrega aquí tus mapas (puedes copiar y pegar estas líneas para cada mapa)
        mapabeni: resolve(__dirname, 'mapa-beni.html'),
        mapachuquisaca: resolve(__dirname, 'mapa-chuquisaca.html'),
        mapacochabamba: resolve(__dirname, 'mapa-cochabamba.html'),
        mapalapaz: resolve(__dirname, 'mapa-lapaz.html'),
        mapaoruro: resolve(__dirname, 'mapa-oruro.html'),
        mapapando: resolve(__dirname, 'mapa-pando.html'),
        mapapotosi: resolve(__dirname, 'mapa-potosi.html'),
        mapasantacruz: resolve(__dirname, 'mapa-santacruz.html'),
        mapatarija: resolve(__dirname, 'mapa-tarija.html'),
      }
    }
  }
})