import { defineConfig } from 'astro/config';

export default defineConfig({
    output: 'static',
    compressHTML: false,
    devToolbar: { enabled: false },
});
