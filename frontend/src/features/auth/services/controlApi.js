const BASE_URL = '/api';

async function post(path, body) {
  const response = await fetch(`${BASE_URL}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || 'Ошибка сервера');
  }

  return data;
}

async function get(path, token) {
  const response = await fetch(`${BASE_URL}${path}`, {
    method: 'GET',
    headers: { Authorization: `Bearer ${token}` },
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || 'Ошибка сервера');
  }

  return data;
}

async function authRequest(method, path, token, body) {
  const opts = {
    method,
    headers: { Authorization: `Bearer ${token}` },
  };
  if (body !== undefined) {
    opts.headers['Content-Type'] = 'application/json';
    opts.body = JSON.stringify(body);
  }

  const response = await fetch(`${BASE_URL}${path}`, opts);
  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || 'Ошибка сервера');
  }

  return data;
}

export const controlApi = {
  login: (username, password) => post('/auth/login', { login: username, password }),
  register: (username, password) => post('/auth/register', { login: username, password }),
  verify: (token) => get('/auth/verify', token),

  admin: {
    getUsers: (token) => authRequest('GET', '/admin/users', token),
    createUser: (token, login, password) =>
      authRequest('POST', '/admin/users', token, { login, password }),
    renameUser: (token, id, login) =>
      authRequest('PUT', `/admin/users/${id}`, token, { login }),
    deleteUser: (token, id) => authRequest('DELETE', `/admin/users/${id}`, token),
  },
};
