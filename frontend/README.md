# WordMixr Frontend

React TypeScript frontend for the WordMixr word puzzle solver application.

## 🎨 Brand Integration

This frontend uses the WordMixr brand identity with:

- **Colors**: Warm orange (`#B05325`) accents on cream background (`#F8E6C1`)
- **Typography**: Nunito font family for friendly, readable text
- **Logo**: Custom frying pan and letter tiles logo
- **Icons**: Progressive Web App icons for mobile installation

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Run tests
npm test
```

## 📁 Project Structure

```
src/
├── components/          # React components
│   ├── WordSolver.tsx   # Main word solving interface
│   └── ThemeSwitcher.tsx # Theme selection component
├── contexts/            # React contexts
│   └── ThemeContext.tsx # Theme management
├── themes/             # Brand theme configurations
│   └── brandThemes.ts  # Color palettes and styling
├── App.tsx             # Main application component
└── index.tsx           # Application entry point

public/
├── favicon.ico         # Browser favicon
├── icon_*.png          # PWA icons
├── manifest.json       # PWA manifest
└── wordmixr_logo*      # Brand logo assets
```

## 🎨 Theme System

The application supports multiple brand themes:

- **Sophisticated** (default): Rich cream and warm orange palette
- **Vibrant**: Brighter, more saturated brand colors  
- **Original**: Legacy blue/purple gradient theme

Themes are configured in `src/themes/brandThemes.ts` following the brand guidelines.

## 🔧 Key Features

- **Word Solving Interface**: Clean, intuitive input and results display
- **Interactive Results**: Click words to mark as found
- **Progressive Web App**: Installable on mobile devices
- **Responsive Design**: Works seamlessly on desktop and mobile
- **Theme Switching**: Multiple brand-compliant color schemes
- **Accessibility**: Proper ARIA labels and keyboard navigation

## 📱 PWA Features

The app includes Progressive Web App capabilities:

- Installable on mobile devices and desktop
- Custom branded app icon and splash screen
- Offline-ready architecture (future enhancement)
- Native app-like experience when installed

## 🎨 Brand Guidelines

When modifying the frontend, follow these brand principles:

### Colors
- **Primary**: `#B05325` (Warm Orange) for buttons and accents
- **Background**: `#F8E6C1` (Cream) for main background
- **Text**: `#5B3B2F` (Dark Brown) for primary text
- **Secondary**: `#7A4F3F` (Medium Brown) for secondary text

### Typography
- **Font**: Nunito (loaded from Google Fonts)
- **Headings**: Bold weights (600-700) for strong hierarchy
- **Body**: Regular weight (400) for readability
- **Fallbacks**: Quicksand, Poppins, Inter, sans-serif

### Logo Usage
- Use `wordmixr_logo_transparent.png` for overlays
- Use `wordmixr_logo.png` for backgrounds
- Maintain aspect ratio and sufficient padding
- Don't place on clashing backgrounds

## 🛠 Development Guidelines

### Adding New Components
1. Follow React functional component patterns
2. Use TypeScript for all components
3. Apply theme colors via the theme context
4. Ensure responsive design on mobile
5. Add proper accessibility attributes

### Modifying Themes
1. Update colors in `src/themes/brandThemes.ts`
2. Test across all theme variants
3. Ensure sufficient color contrast ratios
4. Maintain brand consistency

### Testing Brand Integration
```bash
# Start development server
npm run dev

# Check in browser:
# - Favicon displays correctly
# - Logo loads and displays properly
# - Colors match brand guidelines
# - Typography uses Nunito font
# - PWA icons work on mobile
```

## 🔍 Troubleshooting

### Logo Not Displaying
- Verify assets are in `public/` directory
- Check browser console for 404 errors
- Confirm file paths in component code

### Font Not Loading
- Check Google Fonts link in `index.html`
- Verify font family name in CSS
- Test with fallback fonts

### PWA Issues
- Verify `manifest.json` is accessible
- Check that all icon sizes are present
- Test installation on mobile device

## 📚 Resources

- [React Documentation](https://react.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Vite Guide](https://vitejs.dev/guide/)
- [PWA Documentation](https://web.dev/progressive-web-apps/)
- [Brand Style Guide](../wordmixr_brand_kit/brand_style_guide.md)

---

*Built with ❤️ and modern web technologies to create a delightful word puzzle solving experience.* 