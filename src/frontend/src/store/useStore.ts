import { create } from 'zustand';

interface Store {
  theme: 'light' | 'dark';
  setTheme: (theme: 'light' | 'dark') => void;
  language: 'en' | 'ko';
  setLanguage: (lang: 'en' | 'ko') => void;
}

const useStore = create<Store>((set) => ({
  theme: 'light',
  setTheme: (theme) => set({ theme }),
  language: 'en',
  setLanguage: (lang) => set({ language: lang }),
}));

export default useStore;