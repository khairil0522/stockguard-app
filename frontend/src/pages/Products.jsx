// ==========================================
// IMPORTS
// Dependencies, services, and utilities
// ==========================================
import { useEffect, useState } from "react";
import { fetchProducts, createProduct, updateProduct, updateProductStatus } from "../services/productService";
import DialogBox from "../components/DialogBox";
import getActiveStatusColor from "../utils/productUtils";

// ==========================================
// PRODUCT LIST COMPONENT
// Main page for managing products
// ==========================================   
export default function Products({ onViewDetail }) {
    // ----------------------------------------
    // STATE MANAGEMENT
    // Stores product data and UI states
    // ----------------------------------------
    const [products, setProducts] = useState([]);

    // Controls the selected product status tab
    const [activeTab, setActiveTab] = useState("active");
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    // Controls the reusable dialog
    const [dialog, setDialog] = useState({
        isOpen: false,
        title: "",
        message: "",
        type: "info",
        confirmText: "OK",
    });

    // ----------------------------------------
    // CREATE PRODUCT FORM STATE
    // Controls form visibility and submission
    // ----------------------------------------
    const [showForm, setShowForm] = useState(false);
    const [saving, setSaving] = useState(false);
    const [success, setSuccess] = useState("");
    const [formError, setFormError] = useState("");

    // ==========================================
    // SELECTED PRODUCT STATE
    // Stores product currently being edited
    // ==========================================
    const [editingProduct, setEditingProduct] = useState(null);

    // ----------------------------------------
    // PRODUCT FORM DATA
    // Stores values entered by the user
    // ----------------------------------------
    const [form, setForm] = useState({
        sku: "",
        name: "",
        unit_price: "",
        description: "",
    });

    // ----------------------------------------
    // DIALOG HANDLER
    // Opens a dialog with specified parameters
    // Open dialog with dynamic configuration
    function openDialog(config) {
        setDialog({
            ...config,
            isOpen: true,
        });
    }

    // Close the currently displayed dialog
    function closeDialog() {
        setDialog((prev) => ({
            ...prev,
            isOpen: false,
        }));
    }


    // ----------------------------------------
    // FETCH PRODUCT LIST
    // Retrieves products from backend API
    // ----------------------------------------
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

    // ----------------------------------------
    // INITIAL DATA LOADING
    // Fetches products when component mounts
    // ----------------------------------------
    useEffect(() => {
        loadProducts();
    }, []);

    // Filter products based on the selected tab
    const filteredProducts = products.filter((product) =>
        activeTab === "active"
            ? product.is_active === true
            : product.is_active === false
    );

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

    // ----------------------------------------
    // CREATE/UPDATE PRODUCT HANDLER
    // Handles product creation/update and API response based on conditions
    // ----------------------------------------
    async function handleSubmit(event) {
        event.preventDefault();

        setSaving(true);
        setSuccess("");
        setFormError("");

        try {
            const productData = {
                name: form.name.trim(),
                unit_price: Number(form.unit_price),
                description: form.description.trim(),
            }

            if (editingProduct) {
                await updateProduct(editingProduct.id, productData);
                setSuccess("Produk berhasil diperbarui!");
            } else {
                productData.sku = form.sku.trim();
                await createProduct(productData);
                setSuccess("Produk berhasil dibuat!");
            }

            setForm({
                sku: "",
                name: "",
                unit_price: "",
                description: "",
            });

            setShowForm(false);
            setEditingProduct(null);
            await loadProducts();
        } catch (err) {
            setFormError(err.message);
        } finally {
            setSaving(false);
        }
    }

    function handleEditProduct(product) {
        setEditingProduct(product);

        setForm({
            sku: product.sku,
            name: product.name,
            unit_price: product.unit_price.toString(),
            description: product.description || "",
        });

        setShowForm(true);
        setFormError("");
        setSuccess("");
    }

    // Update product active status
    function handleUpdateProductStatus(product) {
        const newStatus = !product.is_active;

        openDialog({
            title: newStatus
                ? "Reactivate Product"
                : "Deactivate Product",

            message: `Apakah kamu yakin ingin ${
                newStatus ? "mengaktifkan kembali" : "menonaktifkan"
            } produk ${product.name}?`,

            type: "confirm",

            confirmText: newStatus ? "Reactivate" : "Deactivate",
            cancelText: "Cancel",

            onConfirm: () => processProductStatus(product.id, newStatus),
        });
    }

    // ==========================================
    // RENDER UI
    // ==========================================
    return (
        <>
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
                        setForm({
                            sku: "",
                            name: "",
                            unit_price: "",
                            description: "",
                        });
                        setShowForm(!showForm);
                        setFormError("");
                        setSuccess("");
                        setEditingProduct(null);
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
                            className={`w-full rounded-lg border px-3 py-2 outline-none ${
                                editingProduct
                                    ? "cursor-not-allowed border-gray-300 bg-gray-100 text-gray-500"
                                    : "border-gray-300 bg-white text-gray-900 focus:border-blue-500"
                            }`}
                            placeholder="ELE-LAP-004"
                            disabled={!!editingProduct}
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
                        {saving ? "Saving...": editingProduct ? "Update Product" : "Save Product"}
                    </button>
                </form>
            )}


            <div className="overflow-x-auto rounded-xl border border-slate-200 bg-white">

                {/* Product Status Tabs */}
                <div className="mb-4 flex gap-2 border-b border-slate-200">
                    <button
                        onClick={() => setActiveTab("active")}
                        className={`px-4 py-3 text-sm font-medium ${
                            activeTab === "active"
                                ? "border-b-2 border-emerald-500 text-emerald-600"
                                : "text-slate-500 hover:text-slate-800"
                        }`}
                    >
                        Active Products
                    </button>

                    <button
                        onClick={() => setActiveTab("inactive")}
                        className={`px-4 py-3 text-sm font-medium ${
                            activeTab === "inactive"
                                ? "border-b-2 border-emerald-500 text-emerald-600"
                                : "text-slate-500 hover:text-slate-800"
                        }`}
                    >
                        Inactive Products
                    </button>
                </div>

                <table className="w-full text-left text-sm">
                    <thead className="bg-slate-50 text-slate-500">
                        <tr>
                            <th className="px-6 py-4" >SKU</th> 
                            <th className="px-6 py-4" >Product Name</th>
                            <th className="px-6 py-4" >Unit Price</th>
                            <th className="px-6 py-4" >Status</th>
                            <th className="px-6 py-4 text-center" >Action</th>
                        </tr>
                    </thead>

                    <tbody className="divide-y divide-slate-100">
                        {filteredProducts.map((product) => (    
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
                                <td className="px-6 py-4    ">
                                    <div className="flex items-center gap-2">
                                        <button
                                            onClick={() => onViewDetail(product)}
                                            className="rounded-lg bg-slate-800 px-3 py-2 text-sm text-white hover:bg-slate-700"
                                        >
                                            Detail
                                        </button>
                                        <button
                                            onClick={() => handleEditProduct(product)}
                                            className="rounded-lg bg-amber-500 px-3 py-2 text-sm text-white hover:bg-amber-600"
                                        >
                                            Edit
                                        </button>
                                        <button
                                            onClick={() => handleUpdateProductStatus(product)}
                                            className={`rounded-lg px-3 py-2 text-sm text-white ${
                                                product.is_active
                                                    ? "bg-red-500 hover:bg-red-600"
                                                    : "bg-emerald-500 hover:bg-emerald-600"
                                            }`}
                                        >
                                            {product.is_active ? "Deactivate" : "Reactivate"}
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        ))}

                        {filteredProducts.length === 0 && (
                            <tr>
                                <td colSpan={5} className="px-6 py-10 text-center text-slate-500">
                                    {activeTab === "active"
                                    ? "Belum ada produk aktif."
                                    : "Belum ada produk inactive."}
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>

            <p className="mt-4 text-sm text-slate-500">
                Total {filteredProducts .length} produk
            </p>

            <DialogBox
                isOpen={dialog.isOpen}
                title={dialog.title}
                message={dialog.message}
                type={dialog.type}
                confirmText={dialog.confirmText}
                cancelText={dialog.cancelText}
                onConfirm={dialog.onConfirm}
                onCancel={closeDialog}
            />
        </div>
        </>
    );
}

