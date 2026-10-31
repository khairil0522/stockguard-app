import apiClient from "./apiClients";

export async function fetchInventory() {
    const response = await apiClient.get("/inventory")
    return response.data
}