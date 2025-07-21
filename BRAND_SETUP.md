# WordMixr Brand Asset Setup

This document explains how to properly set up the WordMixr brand assets in the application.

## 📁 Brand Assets Location

The brand kit is located in `wordmixr_brand_kit/` and contains:

- `wordmixr_logo.png` - Full-color logo with background
- `wordmixr_logo_transparent.png` - Logo with transparent background  
- `wordmixr_logo.svg` - Scalable vector logo (placeholder)
- `favicon.ico` - Browser favicon
- `icon_192x192.png` - PWA icon (192x192)
- `icon_512x512.png` - PWA icon (512x512)
- `brand_style_guide.md` - Brand guidelines and color palette
- `brand_style_guide2.md` - Additional brand specifications

## 🔧 Setup Instructions

### 1. Copy Brand Assets to Frontend

Copy the icon files from the brand kit to the frontend public directory:

```bash
# From project root directory
cp wordmixr_brand_kit/favicon.ico frontend/public/
cp wordmixr_brand_kit/icon_192x192.png frontend/public/
cp wordmixr_brand_kit/icon_512x512.png frontend/public/
cp wordmixr_brand_kit/wordmixr_logo.png frontend/public/
cp wordmixr_brand_kit/wordmixr_logo_transparent.png frontend/public/
cp wordmixr_brand_kit/wordmixr_logo.svg frontend/public/
```

### 2. Verify Asset Integration

The application has been updated to use these assets:

- ✅ **HTML Meta Tags**: Updated `frontend/index.html` with proper favicon and PWA manifest
- ✅ **PWA Manifest**: Created `frontend/public/manifest.json` with brand colors and icons
- ✅ **React Components**: Updated `frontend/src/App.tsx` to use the logo image
- ✅ **Typography**: Added Nunito font from Google Fonts
- ✅ **Color Scheme**: Applied brand colors throughout the application

### 3. Brand Color Palette

The application uses the sophisticated brand theme with these colors:

| Color Name      | Hex Code   | Usage                 |
|-----------------|------------|-----------------------|
| Dark Brown      | `#5B3B2F`  | Text and outlines     |
| Warm Orange     | `#B05325`  | Accents and highlights|
| Cream Background| `#F8E6C1`  | Base background       |

### 4. Typography

- **Primary Font**: Nunito (loaded from Google Fonts)
- **Fallback Fonts**: Quicksand, Poppins, Inter, sans-serif
- **Style**: Bold, rounded styles for headings and app name

## 🎨 Usage Guidelines

Following the brand style guide:

- ✅ Always leave padding around the logo
- ✅ Do not alter the aspect ratio
- ✅ Avoid placing on clashing backgrounds without contrast
- ✅ Use bold, all-uppercase for headers when appropriate
- ✅ Maintain friendly, clean body text with soft rounding

## 🧪 Testing Brand Integration

After copying the assets, test the integration:

1. **Start the development server**: `cd frontend && npm run dev`
2. **Check favicon**: Verify the WordMixr icon appears in the browser tab
3. **Check logo**: Confirm the frying pan logo appears in the app header
4. **Check PWA icons**: Test on mobile devices or use browser dev tools
5. **Check colors**: Verify the warm orange and cream color scheme is applied

## 📱 PWA Features

The brand assets enable Progressive Web App features:

- Custom app icon when installed on mobile devices
- Branded splash screen with theme colors
- Consistent visual identity across all platforms

## 🔄 Future Updates

When updating brand assets:

1. Replace files in `wordmixr_brand_kit/`
2. Copy updated files to `frontend/public/`
3. Update color values in `frontend/src/themes/brandThemes.ts` if needed
4. Test across all devices and browsers

---

*WordMixr aims to blend fun, clarity, and warmth – keep your visual design playful and accessible!* 