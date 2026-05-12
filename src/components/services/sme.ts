const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

function getToken() {
  return localStorage.getItem("token");
}

export async function createSmeSimulation(input_data: any) {
  const response = await fetch(`${API_BASE_URL}/simulations/sme`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${getToken()}`,
    },
    body: JSON.stringify({
      title: "SME Energy Optimizer",
      input_data: JSON.stringify(input_data),
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Could not create SME simulation");
  }

  return data;
}