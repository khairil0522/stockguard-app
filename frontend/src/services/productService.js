import apiClient from "./apiClients";

export async function fetchProducts() {
    const response = await apiClient.get("/products");
    return response.data;
}

export async function createProduct(productData) {
    const response = await apiClient.post(
        "/products", productData
    );

    return response.data;
}