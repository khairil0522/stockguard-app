import { useState } from "react";
import { fetchProductDetail, updateProduct } from "../services/productService";

export function useProduct() {
    const [selectedProduct, setSelectedProduct] = useState(null);

    const handleProductDetail = async (product) => {
        const detail = await fetchProductDetail(product.id);
        setSelectedProduct(detail);

        return detail;
    };

    const handleUpdateProduct = async (productId, productData) => {
        const updatedProduct = await updateProduct(productId, productData);

        setSelectedProduct(updatedProduct);

        return updatedProduct;
    };

    return {
        selectedProduct,
        handleProductDetail,
        handleUpdateProduct,
    };
}