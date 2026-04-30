const API_BASE_URL = "https://code-lh0o.onrender.com";

export type RoiRequest = {
  title: string;
  province: string;
  annual_kwh: number;
  pv_size_kw: number;
  installation_cost: number;
  electricity_price: number;
  incentive_rate: number;
};

export async function createRoiSimulation(data: RoiRequest) {
  const token = localStorage.getItem("token");

  const response = await fetch(`${API_BASE_URL}/simulations/roi`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(data),
  });

  const result = await response.json();

  if (!response.ok) {
    throw new Error(result.detail || "Could not create ROI simulation");
  }

  return result;
}