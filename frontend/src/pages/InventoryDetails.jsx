export default function InventoryDetails({ inventory, onBack }) {
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
            </div>

            {/* Stock Overview */}
            <div>
                <h2 className="mb-4 text-xl font-semibold text-slate-800">
                    Stock Overview
                </h2>

                <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
                    {/* Physical stock */}
                    <div className="rounded-xl border border-blue-100 bg-white p-5">
                        <p className="text-sm text-slate-500">On Hand</p>
                        <h3 className="mt-2 text-3xl font-bold text-blue-600">
                            {inventory.on_hand}
                        </h3>
                        <p className="mt-1 text-xs text-slate-400">
                            Physical stock
                        </p>
                    </div>

                    {/* Reserved stock */}
                    <div className="rounded-xl border border-amber-100 bg-white p-5">
                        <p className="text-sm text-slate-500">Reserved</p>
                        <h3 className="mt-2 text-3xl font-bold text-amber-600">
                            {inventory.reserved_qty}
                        </h3>
                        <p className="mt-1 text-xs text-slate-400">
                            Allocated stock
                        </p>
                    </div>

                    {/* Available stock */}
                    <div className="rounded-xl border border-emerald-100 bg-white p-5">
                        <p className="text-sm text-slate-500">Available</p>
                        <h3 className="mt-2 text-3xl font-bold text-emerald-600">
                            {inventory.available_qty}
                        </h3>
                        <p className="mt-1 text-xs text-slate-400">
                            Available for reservation
                        </p>
                    </div>
                </div>
            </div>
        </div>        
        </>
    );
}