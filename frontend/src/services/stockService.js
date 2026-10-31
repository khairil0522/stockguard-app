import apiClient from "./apiClients";

export async function fetchStockMovements() {
    const response = await apiClient.get("/stocks")
    return response.data;
}

export async function fetchStockMovementByProductId(product_id){
    const response = await apiClient.get(`/stocks/${product_id}`)
    return response.data;
}