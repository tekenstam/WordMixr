import React from 'react'
import { useTheme } from '../contexts/ThemeContext'
import { ThemeName } from '../themes/brandThemes'

const ThemeSwitcher: React.FC = () => {
  const { theme, themeName, setTheme, availableThemes } = useTheme()

  return (
    <div style={{
      position: 'fixed',
      top: '20px',
      right: '20px',
      background: theme.colors.background,
      border: `2px solid ${theme.colors.border}`,
      borderRadius: theme.borderRadius.medium,
      padding: '15px',
      boxShadow: `0 4px 12px ${theme.colors.shadow}`,
      zIndex: 1000
    }}>
      <div style={{
        color: theme.colors.text.primary,
        fontSize: '0.9rem',
        fontWeight: '600',
        marginBottom: '10px',
        fontFamily: theme.fonts.primary
      }}>
        🎨 Try Both Brands:
      </div>
      
      <div style={{
        display: 'flex',
        gap: '8px'
      }}>
        {Object.entries(availableThemes).map(([key, themeOption]) => (
          <button
            key={key}
            onClick={() => setTheme(key as ThemeName)}
            style={{
              padding: '8px 12px',
              borderRadius: theme.borderRadius.small,
              border: themeName === key 
                ? `2px solid ${theme.colors.primary}` 
                : `1px solid ${theme.colors.border}`,
              background: themeName === key 
                ? theme.colors.primary 
                : 'transparent',
              color: themeName === key 
                ? '#fff' 
                : theme.colors.text.primary,
              cursor: 'pointer',
              fontSize: '0.8rem',
              fontWeight: '500',
              fontFamily: theme.fonts.primary,
              transition: 'all 0.2s ease'
            }}
            onMouseEnter={(e) => {
              if (themeName !== key) {
                e.currentTarget.style.background = theme.colors.secondary
              }
            }}
            onMouseLeave={(e) => {
              if (themeName !== key) {
                e.currentTarget.style.background = 'transparent'
              }
            }}
          >
            {themeOption.name}
          </button>
        ))}
      </div>
      
      <div style={{
        marginTop: '8px',
        fontSize: '0.7rem',
        color: theme.colors.text.light,
        fontFamily: theme.fonts.primary
      }}>
        Current: {theme.name}
      </div>
    </div>
  )
}

export default ThemeSwitcher 