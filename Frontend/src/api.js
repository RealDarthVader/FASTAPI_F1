const API_BASE_URL = "https://fastapi-f1-lz8j.onrender.com";

export const getSchedule = async (year = 2024) => {
  const res = await fetch(`${API_BASE_URL}/races/${year}`);
  if (!res.ok) throw new Error("Failed to fetch schedule");
  return res.json();
};

export const getDriverResults = async (year = 2024, gp = "Monaco") => {
  const res = await fetch(`${API_BASE_URL}/drivers/${year}/${gp}`);
  if (!res.ok) throw new Error("Failed to fetch driver results");
  return res.json();
};

export const getFavorites = async () => {
  const res = await fetch(`${API_BASE_URL}/favorites`);
  if (!res.ok) throw new Error("Failed to fetch favorites");
  return res.json();
};

export const addFavorite = async (driverData) => {
  const res = await fetch(`${API_BASE_URL}/favorites`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(driverData),
  });
  if (!res.ok) throw new Error("Failed to add favorite");
  return res.json();
};

export const deleteFavorite = async (driverCode) => {
  const res = await fetch(`${API_BASE_URL}/favorites/${driverCode}`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error("Failed to remove favorite");
};