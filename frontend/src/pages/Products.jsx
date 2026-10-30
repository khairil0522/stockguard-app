import { useEffect, useState } from "react";
import { fetchProducts, createProduct } from "../services/productService";
import getActiveStatusColor from "../utils/productUtils";

export default function Products() {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    //submit
    const [showForm, setShowForm] = useState(false);
    const [saving, setSaving] = useState(false);
    const [success, setSuccess] = useState("");
    const [formError, setFormError] = useState("");

    const [form, setForm] = useState({
        sku: "",
        name: "",
        unit_price: "",
        description: "",
    });

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

    async function handleSubmit(event) {
        event.preventDefault();

        setSaving(true);
        setSuccess("");
        setFormError("");

        try {
            await createProduct({
                sku: form.sku.trim(),
                name: form.name.trim(),
                unit_price: Number(form.unit_price),
                description: form.description.trim(),
            });

            setSuccess("Produk berhasil dibuat!");
            setForm({
                sku: "",
                name: "",
                unit_price: "",
                description: "",
            });

            setShowForm(false);
            await loadProducts();
        } catch (err) {
            setFormError(err.message);
        } finally {
            setSaving(false);
        }
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


            <div className="mb-6 flex justify-end">
                <button
                    onClick={() => {
                        setShowForm(!showForm);
                        setFormError("");
                        setSuccess("");
                    }}
                    className="rounded-lg bg-emerald-500 px-4 py-2 font-medium text-slate-950 hover:bg-emerald-400"
                >
                    {showForm ? "Cancel" : "+ Add Product"}
                </button>
            </div>

            {success && (
                <p className="mb-4 rounded-lg bg-emerald-100 p-3 text-emerald-700">
                    {success}
                </p>
            )}

            {formError && (
                <p className="mb-4 rounded-lg bg-red-100 p-3 text-red-700">
                    {formError}
                </p>
            )}

            {showForm && (
                <form
                    onSubmit={handleSubmit}
                    className="mb-6 space-y-4 rounded-xl border border-slate-200 bg-white p-6"
                >
                    <div>
                        <label className="mb-1 block text-sm font-medium">SKU</label>
                        <input
                            required
                            value={form.sku}
                            onChange={(e) =>
                                setForm({ ...form, sku: e.target.value })
                            }
                            className="w-full rounded-lg border border-slate-300 px-3 py-2"
                            placeholder="ELE-LAP-004"
                        />
                    </div>

                    <div>
                        <label className="mb-1 block text-sm font-medium">
                            Product Name
                        </label>
                        <input
                            required
                            value={form.name}
                            onChange={(e) =>
                                setForm({ ...form, name: e.target.value })
                            }
                            className="w-full rounded-lg border border-slate-300 px-3 py-2"
                            placeholder="Laptop ASUS"
                        />
                    </div>

                    <div>
                        <label className="mb-1 block text-sm font-medium">
                            Unit Price (IDR)
                        </label>
                        <input
                            required
                            type="number"
                            min="0"
                            step="1"
                            value={form.unit_price}
                            onChange={(e) =>
                                setForm({ ...form, unit_price: e.target.value })
                            }
                            className="w-full rounded-lg border border-slate-300 px-3 py-2"
                            placeholder="5900000"
                        />
                    </div>

                    <div>
                        <label className="mb-1 block text-sm font-medium">
                            Description
                        </label>
                        <textarea
                            required
                            value={form.description}
                            onChange={(e) =>
                                setForm({ ...form, description: e.target.value })
                            }
                            className="w-full rounded-lg border border-slate-300 px-3 py-2"
                            placeholder="Deskripsi produk"
                            rows={3}
                        />
                    </div>

                    <button
                        type="submit"
                        disabled={saving}
                        className="rounded-lg bg-emerald-500 px-5 py-2 font-medium text-slate-950 hover:bg-emerald-400 disabled:opacity-50"
                    >
                        {saving ? "Saving..." : "Save Product"}
                    </button>
                </form>
            )}


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

