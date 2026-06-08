const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export type LoginResponse = {
  access_token: string;
  token_type: string;
};

export type MeResponse = {
  id: number;
  email: string;
  role: "user" | "operator" | "supplier" | "admin";
  full_name?: string | null;
  auth_provider?: string | null;
};

async function parseResponse(response: Response): Promise<any> {
  const text = await response.text();
  if (!text) {
    throw new Error(
      `Server returned an empty response (HTTP ${response.status}). ` +
      `Backend URL: ${API_BASE_URL || "(not set)"}`
    );
  }
  try {
    return JSON.parse(text);
  } catch {
    throw new Error(
      `Unexpected server response (HTTP ${response.status}): ${text.slice(0, 120)}`
    );
  }
}

export async function registerUser(
  email: string,
  password: string,
  role: string
) {
  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password, role }),
    });
  } catch {
    throw new Error("Cannot reach the server. Check the API URL or your connection.");
  }

  const data = await parseResponse(response);
  if (!response.ok) throw new Error(data.detail || "Could not register user");
  return data;
}

export async function loginUser(
  email: string,
  password: string
): Promise<LoginResponse> {
  const formData = new URLSearchParams();
  formData.append("username", email);
  formData.append("password", password);
  formData.append("grant_type", "password");

  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: formData.toString(),
    });
  } catch {
    throw new Error("Cannot reach the server. Check the API URL or your connection.");
  }

  const data = await parseResponse(response);
  if (!response.ok) throw new Error(data.detail || `Login failed (HTTP ${response.status})`);
  return data;
}

export async function getMe(token: string): Promise<MeResponse> {
  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}/me`, {
      method: "GET",
      headers: { Authorization: `Bearer ${token}` },
    });
  } catch {
    throw new Error("Cannot reach the server. Check the API URL or your connection.");
  }

  const data = await parseResponse(response);
  if (!response.ok) throw new Error(data.detail || "Could not fetch user");
  return data;
}

export function isLoggedIn() {
  return !!localStorage.getItem("token");
}

export function getToken() {
  return localStorage.getItem("token");
}

export function logout() {
  localStorage.removeItem("token");
}
