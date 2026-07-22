/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        cream: {
          50: '#FAF7F2',
          100: '#F7F4EF',
          200: '#EFEAE1',
          300: '#E4DDD0',
          400: '#D5C9B7',
        },
        sage: {
          50: '#F2F7F2',
          100: '#E1EBE1',
          200: '#C3D7C3',
          300: '#9EBE9C',
          400: '#759D72',
          500: '#537C50',
          600: '#40633D',
          700: '#2E492C',
          800: '#20341F',
          900: '#162415',
          950: '#0F1A0F',
        },
        peach: {
          50: '#FDF6F4',
          100: '#FBE7E1',
          200: '#F5CABF',
          300: '#EBA08E',
          400: '#DF735A',
          500: '#C95338',
          600: '#AA3B22',
          950: '#4A1B0E',
        },
        honey: {
          50: '#FFFDF0',
          100: '#FEF8D6',
          200: '#FAEA9D',
          300: '#F5D85C',
          400: '#EABF26',
          500: '#D49B11',
          600: '#B07B0A',
          700: '#8A5D05',
          950: '#4A2C04',
        },
        sky: {
          50: '#F2F8F9',
          100: '#E0F0F2',
          200: '#BDE1E5',
          300: '#8BC7CD',
          400: '#52A6AF',
          500: '#34858F',
          600: '#266870',
          950: '#0E3438',
        },
        warmgray: {
          50: '#FAF9F8',
          100: '#F3F1EF',
          200: '#E6E3DF',
          300: '#D0CBC5',
          400: '#99928B',
          500: '#6E6761',
          700: '#453F3A',
          800: '#2C2622',
          900: '#1D1916',
        }
      },
      fontFamily: {
        sans: ['Outfit', 'Plus Jakarta Sans', 'system-ui', 'sans-serif'],
        serif: ['Outfit', 'Georgia', 'serif'],
      },
      boxShadow: {
        'pastel': '0 4px 20px -2px rgba(69, 63, 58, 0.05), 0 2px 6px -1px rgba(69, 63, 58, 0.03)',
        'pastel-hover': '0 12px 28px -4px rgba(69, 63, 58, 0.1), 0 4px 12px -2px rgba(69, 63, 58, 0.05)',
      }
    },
  },
  plugins: [],
}
