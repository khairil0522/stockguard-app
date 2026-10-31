import { useState } from "react";
import { fetchStockMovementByProductId } from "../services/stockService";

export function useStockMovement() {
    const [stockMovements, setStockMovements] = useState([]);

    const handleFetchStockMovement = async (product_id) => {
        const data = await fetchStockMovementByProductId(product_id);
        setStockMovements(data);
        return data;
    };

    return {
        stockMovements,
        handleFetchStockMovement
    };
}