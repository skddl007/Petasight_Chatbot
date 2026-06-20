const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function getToken() {
  return sessionStorage.getItem("token");
}

function setToken(token) {
  sessionStorage.setItem("token", token);
}

function clearToken() {
  sessionStorage.removeItem("token");
}

async function request(path, options = {}) {
  const headers = { "Content-Type": "application/json", ...options.headers };
  const token = getToken();
  if (token) headers.Authorization = `Bearer ${token}`;

  const res = await fetch(`${API_URL}${path}`, { ...options, headers });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const detail = data.detail;
    const message =
      typeof detail === "string"
        ? detail
        : Array.isArray(detail)
          ? detail.map((d) => d.msg).join(", ")
          : data.message || `Request failed (${res.status})`;
    throw new Error(message);
  }
  return data;
}

export async function register(email, password) {
  return request("/auth/register", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export async function login(email, password) {
  const data = await request("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
  setToken(data.access_token);
  return data;
}

export async function getMe() {
  return request("/auth/me");
}

export async function sendMessage(message, history = []) {
  return request("/chat", {
    method: "POST",
    body: JSON.stringify({ message, history }),
  });
}

export function logout() {
  clearToken();
}

export { getToken };
// client setup