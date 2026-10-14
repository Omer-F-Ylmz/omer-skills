// @ts-check
import { defineConfig } from 'astro/config';

// three tek paylaşılan parça: bölüm sahneleri ayrı dinamik parçalar, hepsi aynı three'yi yükler
export default defineConfig({
  vite: { build: { rollupOptions: { output: { manualChunks: (id) => (id.includes('node_modules/three/') ? 'three' : undefined) } } } },
});
