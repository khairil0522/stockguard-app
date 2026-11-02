import { useState } from "react";
import { fetchStockMovementByProductId } from "../services/stockService";

export function useStockMovement() {
    const [stockMovements, setStockMovements] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleFetchStockMovement = async (product_id) => {
        setLoading(true);
        setError("");

        try {
            const data = await fetchStockMovementByProductId(product_id);
            setStockMovements(data);
            return data;
        } catch (err) {
            setStockMovements([]);
            setError(err.message);
            throw err;
        } finally {
            setLoading(false);
        }
    };

    return {
        stockMovements,
        loading,
        error,
        handleFetchStockMovement
    };
}