import { defineStore } from 'pinia';
import { controlApi } from '@/features/auth/services/controlApi';
import { useAuthStore } from '@/features/auth/stores/auth';

export const useChatsStore = defineStore('chats', {
  state: () => ({
    chats: [],         // [{ id, name, messages, createdAt, updatedAt }]
    currentChatId: null,
  }),
  getters: {
    currentChat: (state) => state.chats.find((c) => c.id === state.currentChatId) || null,
    allChats: (state) => [...state.chats],
  },
  actions: {
    _token() {
      return useAuthStore().token;
    },

    async init() {
      const token = this._token();
      if (!token) return;

      try {
        const data = await controlApi.chats.getAll(token);
        const serverChats = (data.chats || []).map(this._mapChat);
        this.chats = serverChats;
        this.currentChatId = serverChats.length > 0 ? serverChats[0].id : null;
      } catch (e) {
        console.error('Ошибка загрузки чатов:', e);
      }

      if (this.chats.length === 0) {
        await this.createChat('Новый чат');
      }
    },

    async createChat(name = null) {
      const token = this._token();
      const chatName = name || `Чат ${this.chats.length + 1}`;

      try {
        const data = await controlApi.chats.create(token, chatName);
        const newChat = this._mapChat(data.chat);
        this.chats.unshift(newChat);
        this.currentChatId = newChat.id;
        return newChat.id;
      } catch (e) {
        console.error('Ошибка создания чата:', e);
      }
    },

    async deleteChat(id) {
      const token = this._token();

      try {
        await controlApi.chats.remove(token, id);
      } catch (e) {
        console.error('Ошибка удаления чата:', e);
      }

      const index = this.chats.findIndex((c) => c.id === id);
      if (index !== -1) this.chats.splice(index, 1);

      if (this.currentChatId === id) {
        this.currentChatId = this.chats.length > 0 ? this.chats[0].id : null;
      }

      if (this.chats.length === 0) {
        await this.createChat('Новый чат');
      }

      return this.currentChatId;
    },

    async renameChat(id, newName) {
      const token = this._token();
      const chat = this.chats.find((c) => c.id === id);
      if (!chat) return;

      const name = (newName || '').trim() || 'Без названия';
      chat.name = name;

      try {
        await controlApi.chats.update(token, id, name, chat.messages || []);
      } catch (e) {
        console.error('Ошибка переименования чата:', e);
      }
    },

    setCurrentChat(id) {
      if (this.chats.find((c) => c.id === id)) {
        this.currentChatId = id;
      }
    },

    async saveChat(id) {
      const token = this._token();
      const chat = this.chats.find((c) => c.id === id);
      if (!chat || !token) return;

      try {
        await controlApi.chats.update(token, id, chat.name, chat.messages || []);
        chat.updatedAt = new Date().toISOString();
        // Переставляем чат в начало списка после обновления
        const index = this.chats.findIndex((c) => c.id === id);
        if (index > 0) {
          const [moved] = this.chats.splice(index, 1);
          this.chats.unshift(moved);
        }
      } catch (e) {
        console.error('Ошибка сохранения чата:', e);
      }
    },

    async clearAllChats() {
      const token = this._token();

      const ids = this.chats.map((c) => c.id);
      await Promise.allSettled(ids.map((id) => controlApi.chats.remove(token, id)));

      this.chats = [];
      this.currentChatId = null;

      await this.createChat('Новый чат');
    },

    _mapChat(serverChat) {
      return {
        id: serverChat.id,
        name: serverChat.name,
        messages: Array.isArray(serverChat.messages) ? serverChat.messages : [],
        lastMessageContent: '',
        createdAt: serverChat.created_at,
        updatedAt: serverChat.updated_at,
      };
    },
  },
});
