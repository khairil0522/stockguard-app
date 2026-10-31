import InventoryCard from "../components/InventoryCard"
import { formatCurrency } from "../utils/formatCurrency";
import { useEffect } from "react";
import { useStockMovement } from "../hooks/useMovements";

export default function ProductDetail({ product, onBack }) {

    const { stockMovements, handleFetchStockMovement } = useStockMovement();

    useEffect(() => {
        if (product?.id) {
            handleFetchStockMovement(product.id);
        }
    }, [product?.id]);

    console.log("Stock Movements:", stockMovements);

    return (
        <>
        <div className="p-8 space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <button
                        onClick={onBack}
                        className="mb-3 text-sm text-emerald-600 hover:text-emerald-700"
                    >
                        ← Back to Products
                    </button>

                    <h1 className="text-3xl font-bold text-slate-800">
                        Product Details
                    </h1>
                    <p className="mt-1 text-slate-500">
                        View product information and inventory.
                    </p>
                </div>

                <span className={`rounded-full px-3 py-1 text-sm font-medium ${
                    product.is_active
                        ? "bg-emerald-100 text-emerald-700"
                        : "bg-red-100 text-red-700"
                }`}>
                    {product.is_active ? "Active" : "Inactive"}
                </span>
            </div>

            {/* Product Information */}
            <div className="rounded-xl border border-slate-200 bg-white p-6">
                <h2 className="text-lg font-semibold text-slate-800">
                    Product Information
                </h2>
                <p className="mb-2 text-sm text-slate-500">
                    SKU: {product.sku}
                </p>

                <h2 className="text-2xl font-bold text-slate-800">
                    {product.name}
                </h2>

                <p className="mt-2 text-sm text-slate-500">
                    {product.description || "No description available."}
                </p>

                <p className="mt-5 text-xl font-semibold text-slate-800">
                    {formatCurrency(product.unit_price, "IDR")}
                </p>

                <p className="text-sm text-slate-500">
                    Last Updated: {product.updated_at || "No update yet"}
                </p>
            </div>

            {/* Inventory Overview */}
            <div>
                <h2 className="mb-4 text-xl font-semibold text-slate-800">
                    Inventory Overview
                </h2>

                <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
                    <InventoryCard
                        title="On Hand"
                        value={product.inventory.on_hand}
                        color="blue"
                    />

                    <InventoryCard
                        title="Reserved"
                        value={product.inventory.reserved_qty}
                        color="amber"
                    />

                    <InventoryCard
                        title="Available"
                        value={product.inventory.available_qty}
                        color="emerald"
                    />
                    
                </div>
            </div>

            {/* Stock Movement History */}
            <div className="rounded-xl border border-slate-200 bg-white p-6">
                <h2 className="mb-5 text-xl font-semibold text-slate-800">
                    Recent Stock Movements
                </h2>

                <div className="overflow-x-auto">
                    <table className="w-full text-left text-sm">
                        <thead className="bg-slate-50 text-slate-500">
                            <tr>
                                <th className="px-4 py-3">Date</th>
                                <th className="px-4 py-3">Type</th>
                                <th className="px-4 py-3">Quantity</th>
                                <th className="px-4 py-3">Reason</th>
                            </tr>
                        </thead>

                        <tbody className="divide-y divide-slate-100">

                            {stockMovements.length === 0 ? (
                            <tr>
                                <td colSpan="4" className="px-4 py-6 text-center text-slate-400">
                                No stock movement history available.
                                </td>
                            </tr>
                            ) : (
                            stockMovements.map((movement) => (
                                <tr key={movement.id}>
                                    <td className="px-4 py-3">
                                        {new Date(movement.created_at).toLocaleString("id-ID")}
                                    </td>
                                    <td className="px-4 py-3">
                                        <span className={
                                            movement.movement_type === "INCREASE"
                                                ? "font-medium text-emerald-600"
                                                : "font-medium text-red-600"
                                        }>
                                            {movement.movement_type}
                                        </span>
                                    </td>
                                    <td className="px-4 py-3">
                                        {movement.movement_type === "INCREASE" ? "+" : "-"}
                                        {movement.quantity}
                                    </td>
                                    <td className="px-4 py-3">
                                        {movement.reason}
                                    </td>
                                </tr>
                            ))
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        </>
    );
}