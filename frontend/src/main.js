import { createApp } from 'vue';
import { createPinia } from 'pinia';
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate';
import App from './App.vue';
import router from './router';
import './assets/main.css';

import { storageRepository, nativeFacade /*, capacitorAdapter*/ } from '@/shared/services';
import { useAuthStore } from '@/features/auth/stores/auth';

const activeNativeFacade = nativeFacade;

const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);

const app = createApp(App);

app.provide('storageRepository', storageRepository);
app.provide('nativeFacade', activeNativeFacade);

app.use(pinia);

// Проверяем сохранённый токен до монтирования роутера,
// чтобы guard видел актуальное состояние аутентификации.
const authStore = useAuthStore();
authStore.initAuth().finally(() => {
  app.use(router);
  app.mount('#app');
});
