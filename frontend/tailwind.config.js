/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      colors: {
        'viz-bg': '#0a0a0f',
        'viz-card': '#12121a',
        'viz-border': '#1e1e2e',
        'viz-accent': '#8b5cf6',
        'viz-accent-dim': '#6d28d9',
      }
    }
  },
  plugins: []
};
