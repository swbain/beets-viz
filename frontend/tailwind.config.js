/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      colors: {
        'viz-bg': '#111111',
        'viz-card': '#1a1a1a',
        'viz-border': '#2a2a2a',
        'viz-accent': '#666666',
      }
    }
  },
  plugins: []
};
