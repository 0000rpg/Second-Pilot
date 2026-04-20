import { defineStore } from 'pinia';
import { controlApi } from '../services/controlApi';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: null,
    isAuthenticated: false,
  }),
  actions: {
    async login(username, password) {
      const data = await controlApi.login(username, password);
      this.user = data.username;
      this.token = data.token;
      this.isAuthenticated = true;
    },
    async register(username, password) {
      const data = await controlApi.register(username, password);
      this.user = data.username;
      this.token = data.token;
      this.isAuthenticated = true;
    },
    logout() {
      this.user = null;
      this.token = null;
      this.isAuthenticated = false;
    },
    // Вызывается при старте приложения: проверяет сохранённый токен через сервер.
    async initAuth() {
      if (!this.token) return;
      try {
        const data = await controlApi.verify(this.token);
        this.user = data.username;
        this.isAuthenticated = true;
      } catch {
        this.logout();
      }
    },
  },
  persist: true,
});
