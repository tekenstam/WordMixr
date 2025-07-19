import React from 'react'
import WordSolver from './components/WordSolver'

const App: React.FC = () => {
  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '20px',
      boxSizing: 'border-box'
    }}>
      <div style={{
        background: 'rgba(255, 255, 255, 0.95)',
        borderRadius: '20px',
        padding: '40px',
        boxShadow: '0 20px 40px rgba(0, 0, 0, 0.1)',
        maxWidth: '800px',
        width: '100%',
        backdropFilter: 'blur(10px)'
      }}>
        <header style={{
          textAlign: 'center',
          marginBottom: '30px'
        }}>
          <h1 style={{
            color: '#4a5568',
            fontSize: '3rem',
            margin: '0 0 10px 0',
            fontWeight: '700',
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent'
          }}>
            🎯 WordMixr
          </h1>
          <p style={{
            color: '#718096',
            fontSize: '1.1rem',
            margin: 0
          }}>
            Solve word puzzles by finding all possible words from scrambled letters
          </p>
        </header>
        
        <WordSolver />
        
        <footer style={{
          textAlign: 'center',
          marginTop: '30px',
          color: '#a0aec0',
          fontSize: '0.9rem'
        }}>
          Enter letters and click "Solve" to find all possible words!
        </footer>
      </div>
    </div>
  )
}

export default App 