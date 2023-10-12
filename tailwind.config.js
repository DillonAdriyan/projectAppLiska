/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./*.{html,js}"],
  theme: {
   container: {
      center: true,
      padding: '16px'
    },
    extend: {
     colors: {
      primary: '#06b6d4',
      secondary: '#f4f5f5',
      transparent: 'transparent',
      dark: '#0c0a09',
      dark2: '#141212'
     }
    },
  },
  plugins: [],
}

