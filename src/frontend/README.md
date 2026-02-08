# 📸 Camera TestGen Frontend

## 🎯 Overview

React frontend for Camera TestGen — a tool to review, accept, and reject Gherkin test cases generated from UI
screenshots.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Start Development Server

```bash
npm run dev
```

Access: `http://localhost:5173`

### 3. Build for Production

```bash
npm run build
```

Output: `../dist/` (used by Docker frontend image)

## 📁 Folder Structure

```
src/
├── assets/        # Images, icons
├── components/    # Reusable UI components
├── pages/         # Main pages (Dashboard, Review, Export, Feedback)
├── services/      # API calls to FastAPI backend
├── store/         # Zustand state management
├── App.tsx        # Main app component
├── main.tsx       # Entry point
└── index.css      # Tailwind + global styles
```

## 🧩 Features

- Dashboard: View all screenshots and their status
- Review: Accept or reject generated Gherkin test cases
- Export: Download accepted test cases as `.feature` files
- Feedback: View logs of user feedback
- Dark/Light mode toggle
- Multi-language support (English/Korean)

## 🛡️ On-Prem Compliance

- All API calls go to local FastAPI backend (`http://localhost:8000`)
- No external dependencies (except React ecosystem)
- Configurable via `config/settings.yaml`

## 📦 Dependencies

See `package.json` for full list.

## 📝 Notes

- Uses **Vite + React + TypeScript + Tailwind CSS**
- API proxy configured in `vite.config.ts` to forward `/api` to backend
- Zustand for global state (theme, language)