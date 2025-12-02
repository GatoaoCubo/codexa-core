# TAC-7 Frontend Client

Vite-powered TypeScript frontend for the TAC-7 E-commerce Intelligence Platform.

## Overview

Modern web interface for:
- **Natural Language Queries** - Ask questions about your data in Portuguese or English
- **Data Visualization** - Interactive charts and tables
- **Agent Control** - Trigger and monitor agent operations
- **Real-time Updates** - Live data streaming from backend

## Quick Start

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Access application
# http://localhost:5173
```

## Structure

```
app/client/
├── src/                     # Source code
│   ├── components/          # React components
│   ├── services/            # API services
│   ├── utils/               # Utility functions
│   ├── App.tsx              # Main application
│   └── main.tsx             # Entry point
├── public/                  # Static assets
├── index.html               # HTML template
├── vite.config.ts           # Vite configuration
├── tsconfig.json            # TypeScript configuration
└── package.json             # Node dependencies
```

## Features

- **Natural Language Interface** - Type questions in plain language
- **Multi-language Support** - Portuguese and English queries
- **Responsive Design** - Works on desktop and mobile
- **Real-time Results** - Instant query execution
- **Export Options** - Download results in multiple formats

## Configuration

The frontend connects to the backend at:
- Development: `http://localhost:8000`
- Production: Configure in environment variables

## Scripts

```bash
npm run dev       # Start development server
npm run build     # Build for production
npm run preview   # Preview production build
npm run lint      # Run ESLint
npm run type-check # TypeScript type checking
```

## Technology Stack

- **Framework**: Vite 6.3.5
- **Language**: TypeScript 5.8.3
- **UI Library**: React (if applicable)
- **Styling**: CSS Modules / Tailwind
- **HTTP Client**: Axios / Fetch API
- **State Management**: Context API / Redux

## Development

### Environment Setup
```bash
# Install Node.js 18+
# Install dependencies
npm install
```

### API Integration
The client communicates with the FastAPI backend:
- Base URL: `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`

### Building for Production
```bash
# Create production build
npm run build

# Output directory: dist/
# Serve with any static file server
```

## Testing

```bash
# Run tests (if configured)
npm test

# Run tests with coverage
npm run test:coverage
```

## Troubleshooting

### Port already in use
```bash
# Change port in vite.config.ts
# Or use environment variable
VITE_PORT=3000 npm run dev
```

### Backend connection issues
- Verify backend is running: `http://localhost:8000`
- Check CORS settings in backend
- Verify API endpoints in services

### Build errors
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
npm run build
```

## Related Documentation

- Main README: `/README.md`
- Backend: `/app/server/README.md`
- Vite Documentation: https://vitejs.dev/
- TypeScript Documentation: https://www.typescriptlang.org/