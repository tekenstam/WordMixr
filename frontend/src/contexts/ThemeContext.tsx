import React, { createContext, useContext, useState, ReactNode } from 'react'
import { BrandTheme, themes, ThemeName, sophisticatedTheme } from '../themes/brandThemes'

interface ThemeContextType {
  theme: BrandTheme
  themeName: ThemeName
  setTheme: (themeName: ThemeName) => void
  availableThemes: Record<ThemeName, BrandTheme>
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined)

interface ThemeProviderProps {
  children: ReactNode
  defaultTheme?: ThemeName
}

export const ThemeProvider: React.FC<ThemeProviderProps> = ({ 
  children, 
  defaultTheme = 'sophisticated' 
}) => {
  const [themeName, setThemeName] = useState<ThemeName>(defaultTheme)
  const theme = themes[themeName]

  const setTheme = (newThemeName: ThemeName) => {
    setThemeName(newThemeName)
  }

  return (
    <ThemeContext.Provider value={{
      theme,
      themeName,
      setTheme,
      availableThemes: themes
    }}>
      {children}
    </ThemeContext.Provider>
  )
}

export const useTheme = (): ThemeContextType => {
  const context = useContext(ThemeContext)
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider')
  }
  return context
} 