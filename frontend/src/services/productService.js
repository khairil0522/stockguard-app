import apiClient from "./apiClients";

// Fetch product data from backend
export async function fetchProducts() {
    const response = await apiClient.get("/products");
    return response.data;
}

// Fetch a specific product
export async function fetchProductDetail(productId) {
    const response = await apiClient.get(`/products/${productId}`);
    return response.data;
}

// Fetch stock movements for a specific product
export async function createProduct(productData) {
    const response = await apiClient.post(
        "/products", productData
    );
    return response.data;
}

// Update product data for a specific product
export async function updateProduct(productId, productData) {
    const response = await apiClient.put(
        `/products/${productId}`, productData
    );
    return response.data;
}

// Update product status (active/inactive)
export async function updateProductStatus(productId, isActive) {
    const response = await apiClient.patch(
        `/products/${productId}/status`, { is_active: isActive }
    );
    return response.data;
}