import apiClient from "./apiClients";

export async function fetchStockMovements() {
    const response = await apiClient.get("/stocks")
    return response.data;
}

export async function fetchStockMovementByProductId(product_id){
    const response = await apiClient.get(`/stocks/${product_id}`)
    return response.data;
}

// Create a new stock adjustment
export async function createStockAdjustment(product_id, payload) {
    const response = await apiClient.post(
        `/stocks/products/${product_id}/stock-adjustments`,
        payload
    );

    return response.data;
}   