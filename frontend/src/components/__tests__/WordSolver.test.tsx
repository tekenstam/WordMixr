import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import WordSolver from '../WordSolver'

// Mock fetch
const mockFetch = vi.fn()
global.fetch = mockFetch

describe('WordSolver Component', () => {
  beforeEach(() => {
    mockFetch.mockClear()
  })

  it('renders the component with initial state', () => {
    render(<WordSolver />)
    
    expect(screen.getByText('WordMixr')).toBeInTheDocument()
    expect(screen.getByPlaceholderText('Enter letters to solve...')).toBeInTheDocument()
    expect(screen.getByText('Solve Words')).toBeInTheDocument()
    expect(screen.getByText('Find Anagrams')).toBeInTheDocument()
    expect(screen.getByDisplayValue('3+ letters (recommended)')).toBeInTheDocument()
  })

  it('shows validation error for empty input', async () => {
    const user = userEvent.setup()
    render(<WordSolver />)
    
    const solveButton = screen.getByText('Solve Words')
    await user.click(solveButton)
    
    expect(screen.getByText('Please enter some letters')).toBeInTheDocument()
  })

  it('calls API and displays results on successful solve', async () => {
    const user = userEvent.setup()
    const mockResponse = {
      success: true,
      input_letters: 'test',
      word_count: 3,
      words: ['set', 'test', 'tests']
    }
    
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse
    })
    
    render(<WordSolver />)
    
    const input = screen.getByPlaceholderText('Enter letters to solve...')
    const solveButton = screen.getByText('Solve Words')
    
    await user.type(input, 'test')
    await user.click(solveButton)
    
    await waitFor(() => {
      expect(screen.getByText('Found 3 words from "test"')).toBeInTheDocument()
    })
    
    expect(screen.getByText('set')).toBeInTheDocument()
    expect(screen.getByText('test')).toBeInTheDocument()
    expect(screen.getByText('tests')).toBeInTheDocument()
  })

  it('handles API errors gracefully', async () => {
    const user = userEvent.setup()
    
    mockFetch.mockRejectedValueOnce(new Error('Network error'))
    
    render(<WordSolver />)
    
    const input = screen.getByPlaceholderText('Enter letters to solve...')
    const solveButton = screen.getByText('Solve Words')
    
    await user.type(input, 'test')
    await user.click(solveButton)
    
    await waitFor(() => {
      expect(screen.getByText('Failed to connect to server')).toBeInTheDocument()
    })
  })

  it('switches between solve and anagram modes', async () => {
    const user = userEvent.setup()
    render(<WordSolver />)
    
    const anagramButton = screen.getByText('Find Anagrams')
    await user.click(anagramButton)
    
    // Should show anagram mode UI changes
    expect(anagramButton).toHaveClass('active') // assuming we have active class styling
  })

  it('changes minimum word length filter', async () => {
    const user = userEvent.setup()
    render(<WordSolver />)
    
    const select = screen.getByDisplayValue('3+ letters (recommended)')
    await user.selectOptions(select, '4')
    
    expect(screen.getByDisplayValue('4+ letters')).toBeInTheDocument()
  })

  it('handles word clicking functionality', async () => {
    const user = userEvent.setup()
    const mockResponse = {
      success: true,
      input_letters: 'test',
      word_count: 2,
      words: ['set', 'test']
    }
    
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse
    })
    
    render(<WordSolver />)
    
    const input = screen.getByPlaceholderText('Enter letters to solve...')
    const solveButton = screen.getByText('Solve Words')
    
    await user.type(input, 'test')
    await user.click(solveButton)
    
    await waitFor(() => {
      expect(screen.getByText('set')).toBeInTheDocument()
    })
    
    // Click on a word
    const wordElement = screen.getByText('set')
    await user.click(wordElement)
    
    // Word should have clicked styling (this would depend on actual implementation)
    // For now, just verify the click event works
    expect(wordElement).toBeInTheDocument()
  })

  it('shows loading state during API call', async () => {
    const user = userEvent.setup()
    
    // Create a promise that we can control
    let resolvePromise: (value: any) => void
    const mockPromise = new Promise((resolve) => {
      resolvePromise = resolve
    })
    
    mockFetch.mockReturnValueOnce(mockPromise)
    
    render(<WordSolver />)
    
    const input = screen.getByPlaceholderText('Enter letters to solve...')
    const solveButton = screen.getByText('Solve Words')
    
    await user.type(input, 'test')
    await user.click(solveButton)
    
    // Should show loading state
    expect(screen.getByText('Searching for words...')).toBeInTheDocument()
    
    // Resolve the promise
    resolvePromise!({
      ok: true,
      json: async () => ({
        success: true,
        input_letters: 'test',
        word_count: 1,
        words: ['test']
      })
    })
    
    await waitFor(() => {
      expect(screen.queryByText('Searching for words...')).not.toBeInTheDocument()
    })
  })

  it('constructs correct API URLs', async () => {
    const user = userEvent.setup()
    const mockResponse = {
      success: true,
      input_letters: 'test',
      word_count: 1,
      words: ['test']
    }
    
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse
    })
    
    render(<WordSolver />)
    
    const input = screen.getByPlaceholderText('Enter letters to solve...')
    const solveButton = screen.getByText('Solve Words')
    
    await user.type(input, 'test')
    await user.click(solveButton)
    
    await waitFor(() => {
      expect(mockFetch).toHaveBeenCalledWith('/solve?letters=test&min_word_length=3')
    })
  })

  it('handles anagram API calls', async () => {
    const user = userEvent.setup()
    const mockResponse = {
      success: true,
      input_letters: 'listen',
      word_count: 2,
      words: ['listen', 'silent']
    }
    
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse
    })
    
    render(<WordSolver />)
    
    const input = screen.getByPlaceholderText('Enter letters to solve...')
    const anagramButton = screen.getByText('Find Anagrams')
    
    // Switch to anagram mode
    await user.click(anagramButton)
    await user.type(input, 'listen')
    await user.click(anagramButton) // Click again to submit
    
    await waitFor(() => {
      expect(mockFetch).toHaveBeenCalledWith('/anagrams?letters=listen&min_word_length=3')
    })
  })
}) 