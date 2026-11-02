import apiClient from "./apiClients";

// Fetch all inventory data
export async function fetchInventory() {
    const response = await apiClient.get("/inventory/");
    return response.data;
}

// Fetch inventory detail by product ID
export async function fetchInventoryDetail(productId) {
    const response = await apiClient.get(`/inventory/${productId}`);
    return response.data;
}