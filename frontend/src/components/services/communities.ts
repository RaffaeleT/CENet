const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

function getToken() {
  return localStorage.getItem("token");
}

function authHeaders() {
  return {
    Authorization: `Bearer ${getToken()}`,
  };
}

export async function getMyCommunities() {
  const response = await fetch(`${API_BASE_URL}/communities/my`, {
    method: "GET",
    headers: authHeaders(),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Could not fetch communities");
  }

  return data;
}

export async function createCommunity(data: {
  name: string;
  region: string;
  province: string;
  description?: string;
}) {
  const response = await fetch(`${API_BASE_URL}/communities/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...authHeaders(),
    },
    body: JSON.stringify(data),
  });

  const result = await response.json();

  if (!response.ok) {
    throw new Error(result.detail || "Could not create community");
  }

  return result;
}

export async function getCommunityDashboard(communityId: number) {
  const response = await fetch(
    `${API_BASE_URL}/communities/${communityId}/dashboard`,
    {
      method: "GET",
      headers: authHeaders(),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Could not fetch dashboard");
  }

  return data;
}

export async function getCommunityMembers(communityId: number) {
  const response = await fetch(
    `${API_BASE_URL}/communities/${communityId}/members`,
    {
      method: "GET",
      headers: authHeaders(),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Could not fetch members");
  }

  return data;
}

export async function addCommunityMember(
  communityId: number,
  data: {
    email: string;
    role?: string;
  }
) {
  const response = await fetch(
    `${API_BASE_URL}/communities/${communityId}/members`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...authHeaders(),
      },
      body: JSON.stringify(data),
    }
  );

  const result = await response.json();

  if (!response.ok) {
    throw new Error(result.detail || "Could not add member");
  }

  return result;
}