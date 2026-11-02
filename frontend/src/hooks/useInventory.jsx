import { useState } from "react";
import { fetchInventoryDetail } from "../services/inventoryService";

export function useInventory() {
    const [selectedInventory, setSelectedInventory] = useState(null);

    const handleInventoryDetail = async (inventory) => {
        const detail = await fetchInventoryDetail(inventory.product_id);

        setSelectedInventory(detail);
        return detail;
    }

    return {
        selectedInventory,
        handleInventoryDetail,
    }
}