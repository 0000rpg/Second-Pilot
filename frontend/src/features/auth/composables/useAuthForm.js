import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import { validateLogin, validatePassword } from '@/shared/utils/validation';

export function useAuthForm() {
  const router = useRouter();
  const authStore = useAuthStore();

  const state = ref('login');
  const username = ref('');
  const password = ref('');
  const confirmPassword = ref('');
  const errorMessage = ref('');
  const usernameErrors = ref([]);
  const passwordErrors = ref([]);
  const confirmPasswordError = ref('');
  const inputModes = ref({ login: '', password: '', confirmPassword: '' });

  const validateUsernameField = () => {
    const result = validateLogin(username.value);
    usernameErrors.value = result.errors;
    inputModes.value.login = result.isValid ? 'correct' : 'error';
    return result.isValid;
  };
  const validatePasswordField = () => {
    const result = validatePassword(password.value);
    passwordErrors.value = result.errors;
    inputModes.value.password = result.isValid ? 'correct' : 'error';
    return result.isValid;
  };
  const validateConfirmPassword = () => {
    if (state.value !== 'register') return true;
    const isValid = password.value === confirmPassword.value;
    confirmPasswordError.value = isValid ? '' : 'Пароли не совпадают';
    inputModes.value.confirmPassword = isValid ? 'correct' : 'error';
    return isValid;
  };
  const validateRegistrationForm = () => {
    return validateUsernameField() && validatePasswordField() && validateConfirmPassword();
  };

  const handleSubmit = async () => {
    errorMessage.value = '';
    if (state.value === 'login') {
      return handleLogin();
    } else {
      return handleRegistration();
    }
  };

  const handleLogin = async () => {
    try {
      await authStore.login(username.value, password.value);
      router.push('/main');
      return true;
    } catch (err) {
      errorMessage.value = err.message || 'Неверное имя пользователя или пароль.';
      return false;
    }
  };

  const handleRegistration = async () => {
    if (!validateRegistrationForm()) return false;

    try {
      await authStore.register(username.value, password.value);
      router.push('/main');
      return true;
    } catch (err) {
      errorMessage.value = err.message || 'Ошибка регистрации.';
      return false;
    }
  };

  const tabs = [
    { value: 'login', label: 'Вход' },
    { value: 'register', label: 'Регистрация' },
  ];
  const state_list = ref({ login: 'Войти', register: 'Зарегистрироваться' });

  return {
    state,
    username,
    password,
    confirmPassword,
    errorMessage,
    usernameErrors,
    passwordErrors,
    confirmPasswordError,
    inputModes,
    tabs,
    state_list,
    handleSubmit,
    validateUsernameField,
    validatePasswordField,
    validateConfirmPassword,
  };
}
