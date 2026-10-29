import { useEffect, useState } from "react";
import { fetchProducts } from "../services/productService";
import getActiveStatusColor from "../utils/productUtils";

export default function Products() {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    async function loadProducts() {
        setLoading(true);
        setError("");

        try {
            const data = await fetchProducts();
            setProducts(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        loadProducts();
    }, []);

    if (loading) {
        return <div className="p-8 text-slate-400">Loading products...</div>;
    }

    if (error) {
        return (
            <div className="p-8">
                <p className="text-red-500">{error}</p>
                <button onClick={loadProducts}>Coba lagi</button>
            </div>
        );
    }

    return (
        <div className="p-8">
            <div className="mb-6 flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold text-slate-800">
                        Products
                    </h1>
                    <p className="mt-1 text-slate-500">
                        Manage your inventory products.
                    </p>
                </div>

                <button
                    onClick={loadProducts}
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
                            <th className="px-6 py-4">SKU</th>
                            <th className="px-6 py-4">Product Name</th>
                            <th className="px-6 py-4">Unit Price</th>
                            <th className="px-6 py-4">Status</th>
                        </tr>
                    </thead>

                    <tbody className="divide-y divide-slate-100">
                        {products.map((product) => (
                            <tr key={product.id} className="hover:bg-slate-50">
                                <td className="px-6 py-4 font-mono">
                                    {product.sku}
                                </td>
                                <td className="px-6 py-4 font-medium text-slate-800">
                                    {product.name}
                                </td>
                                <td className="px-6 py-4">
                                    {Number(product.unit_price).toLocaleString(
                                        "id-ID",
                                        {
                                            style: "currency",
                                            currency: "IDR",
                                            maximumFractionDigits: 0,
                                        }
                                    )}
                                </td>
                                <td className="px-6 py-4">
                                    <span
                                        className={
                                            getActiveStatusColor(product.is_active)
                                        }
                                    >
                                        {product.is_active ? "Active" : "Inactive"}
                                    </span>
                                </td>
                            </tr>
                        ))}

                        {products.length === 0 && (
                            <tr>
                                <td colSpan={4} className="px-6 py-10 text-center text-slate-500">
                                    Belum ada produk.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>

            <p className="mt-4 text-sm text-slate-500">
                Total {products.length} produk
            </p>
        </div>
    );
}