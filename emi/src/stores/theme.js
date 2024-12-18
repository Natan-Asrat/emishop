import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  const theme = ref(localStorage.getItem('theme') || 'system')
  
  const systemDarkMode = window.matchMedia('(prefers-color-scheme: dark)')
  
  function updateTheme(newTheme) {
    theme.value = newTheme
    localStorage.setItem('theme', newTheme)
    
    if (newTheme === 'dark' || (newTheme === 'system' && systemDarkMode.matches)) {
      document.documentElement.classList.add('dark')
    } else if (newTheme === 'light' || (newTheme === 'system' && !systemDarkMode.matches)) {
      document.documentElement.classList.remove('dark')
    }
  }

  updateTheme(theme.value)

  systemDarkMode.addEventListener('change', (e) => {
    if (theme.value === 'system') {
      updateTheme('system')
    }
  })

  return {
    theme,
    updateTheme
  }
})
