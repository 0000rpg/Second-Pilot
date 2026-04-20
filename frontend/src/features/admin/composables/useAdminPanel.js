import { ref, reactive, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/features/auth/stores/auth';
import { controlApi } from '@/features/auth/services/controlApi';

export function useAdminPanel() {
  const router = useRouter();
  const authStore = useAuthStore();

  const users = ref([]);
  const showModal = ref(false);
  const modalMode = ref('add');
  const editForm = reactive({ id: null, username: '', password: '' });
  const modalError = ref('');

  const loadUsers = async () => {
    try {
      const data = await controlApi.admin.getUsers(authStore.token);
      users.value = data.users;
    } catch (e) {
      console.error('Ошибка загрузки пользователей:', e.message);
    }
  };

  onMounted(loadUsers);

  const openAddModal = () => {
    modalMode.value = 'add';
    editForm.id = null;
    editForm.username = '';
    editForm.password = '';
    modalError.value = '';
    showModal.value = true;
  };

  const openEditModal = (user) => {
    modalMode.value = 'edit';
    editForm.id = user.id;
    editForm.username = user.username;
    editForm.password = '';
    modalError.value = '';
    showModal.value = true;
  };

  const closeModal = () => {
    showModal.value = false;
  };

  const saveAccount = async () => {
    modalError.value = '';
    try {
      if (modalMode.value === 'add') {
        await controlApi.admin.createUser(authStore.token, editForm.username, editForm.password);
      } else {
        await controlApi.admin.renameUser(authStore.token, editForm.id, editForm.username);
        // Если переименовали себя — обновить имя в сторе
        if (authStore.user === users.value.find((u) => u.id === editForm.id)?.username) {
          authStore.user = editForm.username;
        }
      }
      await loadUsers();
      closeModal();
    } catch (e) {
      modalError.value = e.message;
    }
  };

  const deleteAccount = async (id, username) => {
    if (!confirm(`Вы уверены, что хотите удалить аккаунт ${username}?`)) return;
    try {
      await controlApi.admin.deleteUser(authStore.token, id);
      if (authStore.user === username) {
        authStore.logout();
        router.push('/');
        return;
      }
      await loadUsers();
    } catch (e) {
      console.error('Ошибка удаления пользователя:', e.message);
    }
  };

  const logout = () => {
    authStore.logout();
    router.push('/');
  };

  return {
    users,
    showModal,
    modalMode,
    editForm,
    modalError,
    openAddModal,
    openEditModal,
    closeModal,
    saveAccount,
    deleteAccount,
    logout,
    authStore,
  };
}
