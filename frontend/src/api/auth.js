const API_BASE_URL = "http://localhost:8001";

export async function registerCandidate({ name, email, password, roleApplied }) {
  const params = new URLSearchParams({
    name,
    email,
    password,
    role_applied: roleApplied,
  });

  const response = await fetch(`${API_BASE_URL}/api/register?${params}`, {
    method: "POST",
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Registration failed");
  }

  return data;
}

export async function loginCandidate({ email, password }) {
  const params = new URLSearchParams({ email, password });

  const response = await fetch(`${API_BASE_URL}/api/login?${params}`, {
    method: "POST",
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Login failed");
  }

  return data;
}
