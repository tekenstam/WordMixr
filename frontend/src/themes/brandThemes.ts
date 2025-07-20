// Brand theme configurations for WordMixr

export interface BrandTheme {
  name: string
  colors: {
    primary: string
    secondary: string
    background: string
    text: {
      primary: string
      secondary: string
      light: string
    }
    button: {
      primary: string
      primaryHover: string
      secondary: string
      secondaryHover: string
    }
    border: string
    error: string
    success: string
    shadow: string
  }
  fonts: {
    primary: string
    fallback: string
  }
  borderRadius: {
    small: string
    medium: string
    large: string
  }
}

// Style Guide 1: Vibrant & Warm
export const vibrantTheme: BrandTheme = {
  name: 'Vibrant',
  colors: {
    primary: '#D36629', // Warm Orange
    secondary: '#F9E8CE', // Soft Cream
    background: '#F9E8CE', // Soft Cream background
    text: {
      primary: '#4E2C1E', // Deep Brown
      secondary: '#6B4423', // Lighter brown
      light: '#8B6635', // Even lighter brown
    },
    button: {
      primary: '#D36629', // Warm Orange
      primaryHover: '#B85520', // Darker orange on hover
      secondary: '#4E2C1E', // Deep Brown
      secondaryHover: '#6B4423', // Lighter brown on hover
    },
    border: '#E5D4B8', // Muted cream border
    error: '#D32F2F',
    success: '#2E7D32',
    shadow: 'rgba(78, 44, 30, 0.1)',
  },
  fonts: {
    primary: 'Poppins, sans-serif',
    fallback: 'Nunito, sans-serif',
  },
  borderRadius: {
    small: '8px',
    medium: '15px',
    large: '20px',
  },
}

// Style Guide 2: Rich & Sophisticated
export const sophisticatedTheme: BrandTheme = {
  name: 'Sophisticated',
  colors: {
    primary: '#B05325', // Warm Orange (muted)
    secondary: '#F8E6C1', // Cream Background
    background: '#F8E6C1', // Cream Background
    text: {
      primary: '#5B3B2F', // Dark Brown
      secondary: '#7A4F3F', // Medium brown
      light: '#9A6B55', // Light brown
    },
    button: {
      primary: '#B05325', // Warm Orange
      primaryHover: '#954420', // Darker orange on hover
      secondary: '#5B3B2F', // Dark Brown
      secondaryHover: '#7A4F3F', // Medium brown on hover
    },
    border: '#E8D5B7', // Muted cream border
    error: '#C62828',
    success: '#388E3C',
    shadow: 'rgba(91, 59, 47, 0.1)',
  },
  fonts: {
    primary: 'Nunito, sans-serif',
    fallback: 'Quicksand, Poppins, Inter, sans-serif',
  },
  borderRadius: {
    small: '8px',
    medium: '15px',
    large: '20px',
  },
}

// Original WordMixr theme (blue/purple gradients)
export const originalTheme: BrandTheme = {
  name: 'Original',
  colors: {
    primary: '#667eea', // Blue from original gradient
    secondary: '#f7fafc', // Light gray/white
    background: 'linear-gradient(135deg, #f0f0f0 0%, #e0e0e0 100%)', // Original body background
    text: {
      primary: '#4a5568', // Original heading color
      secondary: '#718096', // Original subtitle color
      light: '#a0aec0', // Original footer color
    },
    button: {
      primary: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', // Original button gradient
      primaryHover: 'linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%)', // Darker gradient
      secondary: '#e2e8f0', // Light gray
      secondaryHover: '#edf2f7', // Lighter gray
    },
    border: '#e2e8f0', // Original border color
    error: '#e53e3e', // Original error color
    success: '#38a169',
    shadow: 'rgba(0, 0, 0, 0.1)', // Original shadow
  },
  fonts: {
    primary: 'system-ui, -apple-system, sans-serif',
    fallback: 'Arial, sans-serif',
  },
  borderRadius: {
    small: '8px',
    medium: '15px',
    large: '20px',
  },
}

// Theme context hook
export const themes = {
  original: originalTheme,
  vibrant: vibrantTheme,
  sophisticated: sophisticatedTheme,
}

export type ThemeName = keyof typeof themes
