import React, { useState } from 'react'
import { useTheme } from '../contexts/ThemeContext'

interface WordResponse {
  success: boolean
  input_letters: string
  word_count: number
  words: string[]
  errors?: string[]
}

const WordSolver: React.FC = () => {
  const [letters, setLetters] = useState('')
  const [words, setWords] = useState<string[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [wordCount, setWordCount] = useState(0)
  const [searchType, setSearchType] = useState<'solve' | 'anagrams'>('solve')
  const [minWordLength, setMinWordLength] = useState(3)
  const [clickedWords, setClickedWords] = useState<Set<string>>(new Set())

  const handleWordClick = (word: string) => {
    const newClickedWords = new Set(clickedWords)
    if (newClickedWords.has(word)) {
      newClickedWords.delete(word)
    } else {
      newClickedWords.add(word)
    }
    setClickedWords(newClickedWords)
  }

  const solve = async () => {
    if (!letters.trim()) {
      setError('Please enter some letters')
      return
    }

    setLoading(true)
    setError(null)
    setClickedWords(new Set()) // Clear clicked words on new search
    
    try {
      const endpoint = searchType === 'anagrams' ? '/anagrams' : '/solve'
      const res = await fetch(`${endpoint}?letters=${encodeURIComponent(letters.trim())}&min_word_length=${minWordLength}`)
      const data: WordResponse = await res.json()
      
      if (data.success) {
        setWords(data.words)
        setWordCount(data.word_count)
        if (data.words.length === 0) {
          setError('No words found for these letters')
        }
      } else {
        setError(data.errors?.join(', ') || 'Failed to solve puzzle')
        setWords([])
        setWordCount(0)
      }
    } catch (err) {
      setError('Failed to connect to server')
      setWords([])
      setWordCount(0)
    } finally {
      setLoading(false)
    }
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value.replace(/[^a-zA-Z]/g, '') // Only allow letters
    setLetters(value)
    if (error && value.trim()) {
      setError(null)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      solve()
    }
  }

  return (
    <div style={{ width: '100%' }}>
      {/* Search Type Toggle */}
      <div style={{
        display: 'flex',
        gap: '10px',
        marginBottom: '15px',
        justifyContent: 'center'
      }}>
        <button
          onClick={() => setSearchType('solve')}
          style={{
            padding: '10px 20px',
            borderRadius: '25px',
            border: 'none',
            background: searchType === 'solve' ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' : '#e2e8f0',
            color: searchType === 'solve' ? 'white' : '#4a5568',
            cursor: 'pointer',
            fontWeight: '600',
            transition: 'all 0.2s'
          }}
        >
          All Words
        </button>
        <button
          onClick={() => setSearchType('anagrams')}
          style={{
            padding: '10px 20px',
            borderRadius: '25px',
            border: 'none',
            background: searchType === 'anagrams' ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' : '#e2e8f0',
            color: searchType === 'anagrams' ? 'white' : '#4a5568',
            cursor: 'pointer',
            fontWeight: '600',
            transition: 'all 0.2s'
          }}
        >
          Anagrams Only
        </button>
      </div>

      {/* Word Length Filter */}
      <div style={{
        display: 'flex',
        gap: '10px',
        marginBottom: '20px',
        justifyContent: 'center',
        alignItems: 'center'
      }}>
        <label style={{
          color: '#4a5568',
          fontSize: '0.9rem',
          fontWeight: '500'
        }}>
          Min word length:
        </label>
        <select
          value={minWordLength}
          onChange={(e) => setMinWordLength(Number(e.target.value))}
          style={{
            padding: '5px 10px',
            borderRadius: '8px',
            border: '2px solid #e2e8f0',
            fontSize: '0.9rem',
            background: 'white',
            color: '#4a5568',
            cursor: 'pointer'
          }}
        >
          <option value={2}>2+ letters</option>
          <option value={3}>3+ letters (recommended)</option>
          <option value={4}>4+ letters</option>
          <option value={5}>5+ letters</option>
          <option value={6}>6+ letters</option>
          <option value={7}>7+ letters</option>
        </select>
      </div>

      {/* Input Section */}
      <div style={{
        display: 'flex',
        gap: '15px',
        marginBottom: '30px',
        alignItems: 'center'
      }}>
        <input
          type="text"
          value={letters}
          onChange={handleInputChange}
          onKeyPress={handleKeyPress}
          placeholder="Enter scrambled letters..."
          style={{
            flex: 1,
            padding: '15px 20px',
            borderRadius: '15px',
            border: error ? '2px solid #e53e3e' : '2px solid #e2e8f0',
            fontSize: '1.1rem',
            outline: 'none',
            transition: 'border-color 0.2s',
            textTransform: 'lowercase'
          }}
          maxLength={20}
          disabled={loading}
        />
        <button
          onClick={solve}
          disabled={loading || !letters.trim()}
          style={{
            padding: '15px 30px',
            borderRadius: '15px',
            border: 'none',
            background: loading || !letters.trim() 
              ? '#cbd5e0' 
              : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            fontSize: '1.1rem',
            fontWeight: '600',
            cursor: loading || !letters.trim() ? 'not-allowed' : 'pointer',
            transition: 'all 0.2s',
            minWidth: '120px'
          }}
        >
          {loading ? '🔍' : 'Solve'}
        </button>
      </div>

      {/* Error Message */}
      {error && (
        <div style={{
          padding: '15px',
          borderRadius: '10px',
          background: '#fed7d7',
          color: '#c53030',
          marginBottom: '20px',
          textAlign: 'center'
        }}>
          {error}
        </div>
      )}

      {/* Results Count */}
      {wordCount > 0 && (
        <div style={{
          textAlign: 'center',
          marginBottom: '20px',
          color: '#4a5568',
          fontSize: '1.1rem',
          fontWeight: '600'
        }}>
          Found {wordCount} {searchType === 'anagrams' ? 'anagram' : 'word'}{wordCount !== 1 ? 's' : ''} 
          {searchType === 'solve' && ` from "${letters}"`}
        </div>
      )}

      {/* Results List */}
      {words.length > 0 && (() => {
        // Separate and sort words
        const unclickedWords = words.filter(word => !clickedWords.has(word)).sort((a, b) => a.length - b.length || a.localeCompare(b))
        const clickedWordsList = words.filter(word => clickedWords.has(word)).sort((a, b) => a.length - b.length || a.localeCompare(b))
        
        const renderWord = (word: string, isClicked: boolean) => (
          <div
            key={word}
            onClick={() => handleWordClick(word)}
            style={{
              padding: '8px 12px',
              background: isClicked ? '#f1f5f9' : '#f7fafc',
              borderRadius: '8px',
              textAlign: 'center',
              fontWeight: '500',
              color: isClicked ? '#94a3b8' : '#4a5568',
              border: isClicked ? '1px solid #cbd5e0' : '1px solid #e2e8f0',
              transition: 'all 0.2s',
              cursor: 'pointer',
              opacity: isClicked ? 0.6 : 1,
              textDecoration: isClicked ? 'line-through' : 'none'
            }}
            onMouseEnter={(e) => {
              if (!isClicked) {
                e.currentTarget.style.background = '#edf2f7'
                e.currentTarget.style.transform = 'translateY(-1px)'
              }
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = isClicked ? '#f1f5f9' : '#f7fafc'
              e.currentTarget.style.transform = 'translateY(0)'
            }}
          >
            {word}
          </div>
        )

        return (
          <div style={{
            maxHeight: '400px',
            overflowY: 'auto',
            border: '2px solid #e2e8f0',
            borderRadius: '15px',
            padding: '20px'
          }}>
            {/* Unclicked words section */}
            {unclickedWords.length > 0 && (
              <div style={{ marginBottom: clickedWordsList.length > 0 ? '20px' : '0' }}>
                <div style={{
                  display: 'grid',
                  gridTemplateColumns: 'repeat(auto-fill, minmax(120px, 1fr))',
                  gap: '10px'
                }}>
                  {unclickedWords.map(word => renderWord(word, false))}
                </div>
              </div>
            )}
            
            {/* Clicked words section */}
            {clickedWordsList.length > 0 && (
              <div>
                {unclickedWords.length > 0 && (
                  <div style={{
                    borderTop: '1px solid #e2e8f0',
                    margin: '20px 0 15px 0',
                    paddingTop: '15px'
                  }} />
                )}
                <div style={{
                  display: 'grid',
                  gridTemplateColumns: 'repeat(auto-fill, minmax(120px, 1fr))',
                  gap: '10px'
                }}>
                  {clickedWordsList.map(word => renderWord(word, true))}
                </div>
              </div>
            )}
          </div>
        )
      })()}

      {/* Loading State */}
      {loading && (
        <div style={{
          textAlign: 'center',
          padding: '40px',
          color: '#718096',
          fontSize: '1.1rem'
        }}>
          <div style={{ fontSize: '2rem', marginBottom: '10px' }}>🔍</div>
          Searching for words...
        </div>
      )}
    </div>
  )
}

export default WordSolver 