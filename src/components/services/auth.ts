const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export type LoginResponse = {
  access_token: string;
  token_type: string;
};

export type MeResponse = {
  id: number;
  email: string;
};

export async function registerUser(
  email: string,
  password: string,
  role: string
) {
  const response = await fetch(`${API_BASE_URL}/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password, role }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Could not register user");
  }

  return data;
}

export async function loginUser(
  email: string,
  password: string
): Promise<LoginResponse> {
  const formData = new URLSearchParams();
  formData.append("username", email);
  formData.append("password", password);

  const response = await fetch(`${API_BASE_URL}/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: formData.toString(),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Could not log in");
  }

  return data;
}

export async function getMe(token: string): Promise<MeResponse> {
  const response = await fetch(`${API_BASE_URL}/me`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Could not fetch user");
  }

  return data;
}

// ✅ NEW: Check if user is logged in
export function isLoggedIn() {
  return !!localStorage.getItem("token");
}

// ✅ (optional but useful later)
export function logout() {
  localStorage.removeItem("token");
}