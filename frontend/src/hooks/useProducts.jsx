import { useState } from "react";
import { fetchProductDetail } from "../services/productService";

export function useProduct() {
    const [selectedProduct, setSelectedProduct] = useState(null);

    const handleViewDetail = async (product) => {
        const detail = await fetchProductDetail(product.id);
        setSelectedProduct(detail);

        return detail;
    };

    return {
        selectedProduct,
        handleViewDetail,
    };
}