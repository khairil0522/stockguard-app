const API_BASE_URL = "http://127.0.0.1:8000/api/v1";

export async function fetchProducts() {
    const response = await fetch(`${API_BASE_URL}/products`);

    if (!response.ok) {
        throw new Error("Gagal mengambil daftar produk");
    }

    return response.json();
}