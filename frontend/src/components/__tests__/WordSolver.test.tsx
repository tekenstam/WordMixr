import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import WordSolver from '../WordSolver'

// Mock fetch
const mockFetch = vi.fn()
globalThis.fetch = mockFetch

describe('WordSolver Component', () => {
  beforeEach(() => {
    mockFetch.mockClear()
  })

  it('renders the component with initial state', () => {
    render(<WordSolver />)

    expect(screen.getByText('All Words')).toBeInTheDocument()
    expect(
      screen.getByPlaceholderText('Enter scrambled letters...')
    ).toBeInTheDocument()
    expect(screen.getByText('Solve')).toBeInTheDocument()
    expect(screen.getByText('Anagrams Only')).toBeInTheDocument()
    expect(
      screen.getByDisplayValue('3+ letters (recommended)')
    ).toBeInTheDocument()
  })

  it('shows validation error for empty input', async () => {
    const user = userEvent.setup()
    render(<WordSolver />)

    const input = screen.getByPlaceholderText('Enter scrambled letters...')
    
    // Focus the input and press Enter to trigger validation (without typing anything)
    await user.click(input)
    await user.keyboard('{Enter}')

    await waitFor(() => {
      expect(screen.getByText('Please enter some letters')).toBeInTheDocument()
    })
  })

  it('calls API and displays results on successful solve', async () => {
    const user = userEvent.setup()
    const mockResponse = {
      success: true,
      input_letters: 'test',
      word_count: 3,
      words: ['set', 'test', 'tests'],
    }

    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    })

    render(<WordSolver />)

    const input = screen.getByPlaceholderText('Enter scrambled letters...')
    const solveButton = screen.getByText('Solve')

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

    const input = screen.getByPlaceholderText('Enter scrambled letters...')
    const solveButton = screen.getByText('Solve')

    await user.type(input, 'test')
    await user.click(solveButton)

    await waitFor(() => {
      expect(
        screen.getByText('Failed to connect to server')
      ).toBeInTheDocument()
    })
  })

  it('switches between solve and anagram modes', async () => {
    const user = userEvent.setup()
    render(<WordSolver />)

    const anagramButton = screen.getByText('Anagrams Only')
    const allWordsButton = screen.getByText('All Words')
    
    // Initially "All Words" should be active (has gradient background)
    expect(allWordsButton).toHaveStyle('background: linear-gradient(135deg, #667eea 0%, #764ba2 100%)')
    
    await user.click(anagramButton)

    // After clicking, "Anagrams Only" should be active
    expect(anagramButton).toHaveStyle('background: linear-gradient(135deg, #667eea 0%, #764ba2 100%)')
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
      words: ['set', 'test'],
    }

    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    })

    render(<WordSolver />)

    const input = screen.getByPlaceholderText('Enter scrambled letters...')
    const solveButton = screen.getByText('Solve')

    await user.type(input, 'test')
    await user.click(solveButton)

    await waitFor(() => {
      expect(screen.getByText('set')).toBeInTheDocument()
    })

    // Click on a word
    const wordElement = screen.getByText('set')
    await user.click(wordElement)

    // After clicking, the word should still be in the document but with different styling
    // The word gets re-rendered when clicked, so we need to find it again
    await waitFor(() => {
      const clickedWordElement = screen.getByText('set')
      expect(clickedWordElement).toBeInTheDocument()
      expect(clickedWordElement).toHaveStyle('opacity: 0.6')
      expect(clickedWordElement).toHaveStyle('text-decoration: line-through')
    })
  })

  it('shows loading state during API call', async () => {
    const user = userEvent.setup()

    // Create a promise that we can control
    let resolvePromise: (value: unknown) => void
    const mockPromise = new Promise(resolve => {
      resolvePromise = resolve
    })

    mockFetch.mockReturnValueOnce(mockPromise)

    render(<WordSolver />)

    const input = screen.getByPlaceholderText('Enter scrambled letters...')
    const solveButton = screen.getByText('Solve')

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
        words: ['test'],
      }),
    })

    await waitFor(() => {
      expect(
        screen.queryByText('Searching for words...')
      ).not.toBeInTheDocument()
    })
  })

  it('constructs correct API URLs', async () => {
    const user = userEvent.setup()
    const mockResponse = {
      success: true,
      input_letters: 'test',
      word_count: 1,
      words: ['test'],
    }

    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    })

    render(<WordSolver />)

    const input = screen.getByPlaceholderText('Enter scrambled letters...')
    const solveButton = screen.getByText('Solve')

    await user.type(input, 'test')
    await user.click(solveButton)

    await waitFor(() => {
      expect(mockFetch).toHaveBeenCalledWith(
        '/solve?letters=test&min_word_length=3'
      )
    })
  })

  it('handles anagram API calls', async () => {
    const user = userEvent.setup()
    const mockResponse = {
      success: true,
      input_letters: 'listen',
      word_count: 2,
      words: ['listen', 'silent'],
    }

    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    })

    render(<WordSolver />)

    const input = screen.getByPlaceholderText('Enter scrambled letters...')
    const anagramButton = screen.getByText('Anagrams Only')
    const solveButton = screen.getByText('Solve')

    // Switch to anagram mode
    await user.click(anagramButton)
    await user.type(input, 'listen')
    await user.click(solveButton) // Click the Solve button, not the anagram button again

    await waitFor(() => {
      expect(mockFetch).toHaveBeenCalledWith(
        '/anagrams?letters=listen&min_word_length=3'
      )
    })
  })
})
