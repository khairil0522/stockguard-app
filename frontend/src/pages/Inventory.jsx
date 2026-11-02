import {useState, useEffect } from "react";
import { fetchInventory } from "../services/inventoryService";

export default function Inventory({ onViewDetail }) {
    const [inventory, setInventory] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    async function loadInventory() {
        setLoading(true);
        setError("");

        try {
            const data = await fetchInventory();
            setInventory(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        loadInventory();
    }, []);

    if (loading) {
        return <div className="p-8 text-slate-400">Loading inventory...</div>;
    }

    if (error) {
        return (
            <div className="p-8">
                <p className="text-red-500">{error}</p>
                <button onClick={loadInventory}>Coba lagi</button>
            </div>
        );
    }

    return (
        <>
        <div className="p-8">
            <div className="mb-6 flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold text-slate-800">
                        Inventory Management
                    </h1>
                    <p className="mt-1 text-slate-500">
                        List Management Inventory, including product details and stock levels.
                    </p>
                </div>

                <button
                    onClick={loadInventory}
                    className="rounded-lg bg-emerald-500 px-4 py-2
                               font-medium text-slate-950 hover:bg-emerald-400"
                >
                    Refresh
                </button>
            </div>

            <div className="overflow-x-auto rounded-xl border border-slate-200 bg-white">
                <table className="w-full text-left text-sm">
                    <thead className="bg-slate-50 text-slate-500">
                        <tr>
                            <th className="px-6 py-4" >SKU</th> 
                            <th className="px-6 py-4" >Product Name</th>
                            <th className="px-6 py-4" >On Hand</th>
                            <th className="px-6 py-4" >Available</th>
                            <th className="px-6 py-4 text-center" >Action</th>
                        </tr>
                    </thead>

                    <tbody className="divide-y divide-slate-100">
                        {inventory.map((inventoryItem) => (
                            <tr key={inventoryItem.product_id} className="hover:bg-slate-50">
                                <td className="px-6 py-4 font-mono">
                                    {inventoryItem.sku}
                                </td>
                                <td className="px-6 py-4 font-medium text-slate-800">
                                    {inventoryItem.product_name}
                                </td>
                                <td className={`px-6 py-4 ${inventoryItem.on_hand == 0 ? 'text-red-500' : 'text-green-500'}`}>
                                    {inventoryItem.on_hand == 0 ? 'Out of Stock' : inventoryItem.on_hand}
                                </td>
                                <td className={`px-6 py-4 ${inventoryItem.available_qty === 0 ? 'text-red-500' : 'text-green-500'}`}>
                                    {inventoryItem.available_qty === 0 ? 'Fully Reserved' : inventoryItem.available_qty}
                                </td>
                                <td className="px-6 py-4 text-center">
                                    <button
                                        onClick={() => onViewDetail(inventoryItem)}
                                        className="rounded-lg bg-slate-800 px-3 py-2 text-sm text-white hover:bg-slate-700"
                                    >
                                        Detail
                                    </button>
                                </td>
                            </tr>
                        ))}
                        {inventory.length === 0 && (
                            <tr>
                                <td colSpan={5} className="px-6 py-10 text-center text-slate-500">
                                    Belum ada inventaris.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
        </>
    );
}
