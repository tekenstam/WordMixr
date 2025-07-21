import React from 'react'
import { ThemeProvider } from './contexts/ThemeContext'
import WordSolver from './components/WordSolver'
import ThemeSwitcher from './components/ThemeSwitcher'
import { useTheme } from './contexts/ThemeContext'

const AppContent: React.FC = () => {
  const { theme, themeName } = useTheme()

  return (
    <div
      style={{
        minHeight: '100vh',
        background: theme.colors.background,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '20px',
        boxSizing: 'border-box',
        fontFamily: theme.fonts.primary,
      }}
    >
      <ThemeSwitcher />

      <div
        style={{
          background: 'rgba(255, 255, 255, 0.7)',
          borderRadius: theme.borderRadius.large,
          padding: '40px',
          boxShadow: `0 20px 40px ${theme.colors.shadow}`,
          maxWidth: '800px',
          width: '100%',
          backdropFilter: 'blur(10px)',
          border: `1px solid ${theme.colors.border}`,
        }}
      >
        <header
          style={{
            textAlign: 'center',
            marginBottom: '30px',
          }}
        >
          {themeName === 'original' ? (
            // Original theme header
            <>
              <h1
                style={{
                  color: theme.colors.text.primary,
                  fontSize: '3rem',
                  margin: '0 0 10px 0',
                  fontWeight: '700',
                  background: theme.colors.button.primary,
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  fontFamily: theme.fonts.primary,
                }}
              >
                🎯 WordMixr
              </h1>
              <p
                style={{
                  color: theme.colors.text.secondary,
                  fontSize: '1.1rem',
                  margin: 0,
                  fontFamily: theme.fonts.primary,
                }}
              >
                Solve word puzzles by finding all possible words from scrambled
                letters
              </p>
            </>
          ) : (
            // Branded themes header (vibrant & sophisticated)
            <>
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '20px',
                  marginBottom: '15px',
                }}
              >
                <img
                  src='/wordmixr_logo_transparent.png'
                  alt='WordMixr Logo'
                  style={{
                    width: '80px',
                    height: '80px',
                    objectFit: 'contain',
                    filter: `drop-shadow(0 4px 12px ${theme.colors.shadow})`,
                  }}
                />
                <h1
                  style={{
                    color: theme.colors.text.primary,
                    fontSize: '3rem',
                    margin: '0',
                    fontWeight: '700',
                    fontFamily: theme.fonts.primary,
                    textShadow: `2px 2px 4px ${theme.colors.shadow}`,
                  }}
                >
                  WordMixr
                </h1>
              </div>

              <div
                style={{
                  display: 'flex',
                  justifyContent: 'center',
                  gap: '8px',
                  marginBottom: '15px',
                }}
              >
                {['W', 'O', 'R', 'D'].map((letter, index) => (
                  <div
                    key={letter}
                    style={{
                      width: '40px',
                      height: '40px',
                      background:
                        index === 1 || index === 2
                          ? theme.colors.primary
                          : theme.colors.secondary,
                      color:
                        index === 1 || index === 2
                          ? '#fff'
                          : theme.colors.text.primary,
                      border: `2px solid ${theme.colors.border}`,
                      borderRadius: theme.borderRadius.small,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      fontWeight: '700',
                      fontSize: '1.2rem',
                      fontFamily: theme.fonts.primary,
                      boxShadow: `0 2px 6px ${theme.colors.shadow}`,
                      transform:
                        index % 2 === 0 ? 'rotate(-2deg)' : 'rotate(2deg)',
                    }}
                  >
                    {letter}
                  </div>
                ))}
              </div>

              <p
                style={{
                  color: theme.colors.text.secondary,
                  fontSize: '1.1rem',
                  margin: 0,
                  fontFamily: theme.fonts.primary,
                  fontWeight: '500',
                }}
              >
                🔥 Cook up words from scrambled letters! Perfect for Word
                Cookies and word puzzles.
              </p>
            </>
          )}
        </header>

        <WordSolver />

        <footer
          style={{
            textAlign: 'center',
            marginTop: '30px',
            color: theme.colors.text.light,
            fontSize: '0.9rem',
            fontFamily: theme.fonts.primary,
          }}
        >
          🎯 Enter letters and click "Solve" to find all possible words!
        </footer>
      </div>
    </div>
  )
}

const App: React.FC = () => {
  return (
    <ThemeProvider defaultTheme='sophisticated'>
      <AppContent />
    </ThemeProvider>
  )
}

export default App
