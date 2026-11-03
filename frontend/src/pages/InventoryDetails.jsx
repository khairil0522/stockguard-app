import { useEffect } from "react";
import { getMovementColor, getMovementIcon } from "../utils/movementUtils";
import { useStockMovement } from "../hooks/useMovements";
import { Package, LockKeyhole, CircleCheck } from "lucide-react"; 

export default function InventoryDetails({ inventory, onBack }) {
    const {
        stockMovements,
        handleFetchStockMovement
    } = useStockMovement();

    // Calculate stock utilization percentage
    const reservedPercentage = inventory.on_hand > 0
        ? (inventory.reserved_qty / inventory.on_hand) * 100
        : 0;

    const availablePercentage = inventory.on_hand > 0
        ? (inventory.available_qty / inventory.on_hand) * 100
        : 0;

    // Determine inventory status based on stock availability
    const stockStatus = inventory.on_hand === 0
        ? "Out of Stock"
        : inventory.available_qty === 0
            ? "Fully Reserved"
            : "In Stock";

    useEffect(() => {
        if (inventory?.product_id) {
            handleFetchStockMovement(inventory.product_id);
        }
    }, [inventory?.product_id]);

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
                        ← Back to Inventory
                    </button>

                    <p className="text-sm text-slate-500">
                        Inventory Management / Detail
                    </p>

                    <h1 className="mt-1 text-3xl font-bold text-slate-800">
                        Inventory Overview
                    </h1>

                    <p className="mt-1 text-slate-500">
                        {inventory.product_name} · SKU: {inventory.sku}
                    </p>
                </div>
                <div>
                    <span
                        className={`rounded-full px-4 py-2 text-sm font-semibold ${
                            stockStatus === "In Stock"
                                ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/40"
                                : stockStatus === "Fully Reserved"
                                    ? "bg-amber-500/20 text-amber-400 border border-amber-500/40"
                                    : "bg-red-500/20 text-red-400 border border-red-500/40"
                        }`}
                    >
                        {stockStatus}
                    </span>
                </div>
            </div>

            {/* Stock Overview */}
            <div>
                <h2 className="mb-4 text-xl font-semibold text-slate-800">
                    Stock Overview
                </h2>

                <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
                    {/* Physical stock */}
                    <div className="rounded-xl border border-slate-700 bg-slate-800 p-5 space-y-2">
                        <Package className="h-5 w-5 text-blue-400" />
                        <h3 className="text-4xl font-bold text-white">
                            {inventory.on_hand}
                        </h3>
                        <p className="text-sm font-medium text-white">On Hand</p>
                        <p className="mt-1 text-xs text-slate-400 text-white">
                            Physical stock
                        </p>
                    </div>

                    {/* Reserved stock */}
                    <div className="rounded-xl border border-amber-900/40 bg-[#3b2d17] p-5 space-y-2">
                        <LockKeyhole className="h-5 w-5 text-amber-500" />
                        <h3 className="text-4xl font-bold text-white">
                            {inventory.reserved_qty}
                        </h3>
                        <p className="text-sm font-medium text-white">Reserved</p>
                        <p className="mt-1 text-xs text-slate-400 text-white">
                            Allocated stock
                        </p>
                    </div>

                    {/* Available stock */}
                    <div className="rounded-xl border border-emerald-900/40 bg-[#12352b] p-5 space-y-2">
                        <CircleCheck className="h-5 w-5 text-emerald-500" />
                        <h3 className="text-4xl font-bold text-white">
                            {inventory.available_qty}
                        </h3>
                        <p className="text-sm font-medium text-white">Available</p>
                        <p className="mt-1 text-xs text-slate-400 text-white">
                            Available for reservation
                        </p>
                    </div>
                </div>
            </div>

            {/* Stock Utilization */}
            <div>
                <h2 className="mb-4 text-xl font-semibold text-slate-800">
                    Stock Utilization
                </h2>

                {/* Progress bar */}
                <div className="flex h-3 w-full overflow-hidden rounded-full bg-slate-200">
                    <div
                        className="bg-amber-500 transition-all duration-500"
                        style={{ width: `${reservedPercentage}%` }}
                    />

                    <div
                        className="bg-emerald-500 transition-all duration-500"
                        style={{ width: `${availablePercentage}%` }}
                    />
                </div>

                {/* Percentage labels */}
                <div className="mt-3 flex justify-between text-sm text-slate-500">
                    <span>{Math.round(reservedPercentage)}% Reserved</span>
                    <span>{Math.round(availablePercentage)}% Available</span>
                </div>
            </div>

            {/* Product Information */}
            <div>
                <h2 className="mb-4 text-xl font-semibold text-slate-800">
                    Product Information
                </h2>

                <div className="overflow-hidden rounded-xl border border-slate-200 bg-white">
                    <table className="w-full text-left text-sm">
                        <thead className="bg-slate-50 text-slate-500">
                            <tr>
                                <th className="px-6 py-4">Field</th>
                                <th className="px-6 py-4">Value</th>
                            </tr>
                        </thead>

                        <tbody className="divide-y divide-slate-100">
                            <tr>
                                <td className="px-6 py-4 font-medium">SKU</td>
                                <td className="px-6 py-4">{inventory.sku}</td>
                            </tr>

                            <tr>
                                <td className="px-6 py-4 font-medium">Product Name</td>
                                <td className="px-6 py-4">{inventory.product_name}</td>
                            </tr>

                            <tr>
                                <td className="px-6 py-4 font-medium">Description</td>
                                <td className="px-6 py-4">
                                    {inventory.description || "-"}
                                </td>
                            </tr>

                            <tr>
                                <td className="px-6 py-4 font-medium">Last Updated</td>
                                <td className="px-6 py-4">
                                    {inventory.updated_at
                                        ? new Date(inventory.updated_at).toLocaleDateString("id-ID", {
                                            day: "2-digit",
                                            month: "short",
                                            year: "numeric"
                                        })
                                        : "-"}
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            {/* Recent Stock Movements */}
            <div>
                <h2 className="mb-4 text-xl font-semibold text-slate-800">
                    Recent Stock Movements
                </h2>

                <div className="rounded-xl border border-slate-200 bg-white p-5">
                    {stockMovements.map((movement, index) => (
                        <div key={movement.id}>
                            <div className="flex items-center justify-between py-4">
                                <div>
                                    <h3 className="font-semibold text-slate-800">
                                        Stock {movement.movement_type}
                                    </h3>

                                    <p className="mt-1 text-sm text-slate-500">
                                        {movement.reason}
                                    </p>
                                </div>

                                <div className="text-right">
                                    <p className={`text-2xl font-bold ${
                                        movement.movement_type === "INCREASE"
                                            ? "text-emerald-500"
                                            : "text-red-500"
                                    }`}>
                                        {movement.movement_type === "INCREASE" ? "+" : "-"}
                                        {movement.quantity}
                                    </p>

                                    <p className="mt-1 text-sm text-slate-500">
                                        {new Date(movement.created_at).toLocaleDateString("id-ID", {
                                            day: "2-digit",
                                            month: "short",
                                            year: "numeric"
                                        })}
                                    </p>
                                </div>
                            </div>

                            {index !== stockMovements.length - 1 && (
                                <div className="border-b border-slate-100" />
                            )}
                        </div>
                    ))}

                    {stockMovements.length === 0 && (
                        <p className="py-8 text-center text-slate-500">
                            No stock movements recorded yet.
                        </p>
                    )}
                </div>
            </div>
        </div>
        </>
    );
}