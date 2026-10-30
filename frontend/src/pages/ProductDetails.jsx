const mockInventory = {
    on_hand: 100,
    reserved_qty: 20,
    available_qty: 80,
};

const mockMovements = [
    {
        id: 1,
        date: "2026-10-30",
        type: "INCREASE",
        quantity: 50,
        reason: "Stock replenishment",
    },
    {
        id: 2,
        date: "2026-10-29",
        type: "DECREASE",
        quantity: 10,
        reason: "Stock adjustment",
    },
    {
        id: 3,
        date: "2026-10-28",
        type: "INCREASE",
        quantity: 60,
        reason: "Initial stock",
    },
];

export default function ProductDetail({ product, onBack }) {
    const formatCurrency = (value) =>
        Number(value).toLocaleString("id-ID", {
            style: "currency",
            currency: "IDR",
            maximumFractionDigits: 0,
        });

    return (
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
                <p className="mb-2 text-sm text-slate-500">
                    SKU: {product.sku}
                </p>

                <h2 className="text-2xl font-bold text-slate-800">
                    {product.name}
                </h2>

                <p className="mt-3 text-slate-500">
                    {product.description || "No description available."}
                </p>

                <p className="mt-5 text-xl font-semibold text-slate-800">
                    {formatCurrency(product.unit_price)}
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
                        value={mockInventory.on_hand}
                    />

                    <InventoryCard
                        title="Reserved"
                        value={mockInventory.reserved_qty}
                    />

                    <InventoryCard
                        title="Available"
                        value={mockInventory.available_qty}
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
                            {mockMovements.map((movement) => (
                                <tr key={movement.id}>
                                    <td className="px-4 py-3">
                                        {movement.date}
                                    </td>
                                    <td className="px-4 py-3">
                                        <span className={
                                            movement.type === "INCREASE"
                                                ? "font-medium text-emerald-600"
                                                : "font-medium text-red-600"
                                        }>
                                            {movement.type}
                                        </span>
                                    </td>
                                    <td className="px-4 py-3">
                                        {movement.type === "INCREASE" ? "+" : "-"}
                                        {movement.quantity}
                                    </td>
                                    <td className="px-4 py-3">
                                        {movement.reason}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}

function InventoryCard({ title, value }) {
    return (
        <div className="rounded-xl border border-slate-200 bg-white p-6">
            <p className="text-sm text-slate-500">{title}</p>
            <h3 className="mt-2 text-3xl font-bold text-slate-800">
                {value}
            </h3>
        </div>
    );
}
