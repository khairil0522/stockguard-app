import { useState, useEffect } from "react";
import { fetchProducts } from "../services/productService";
import { createStockAdjustment } from "../services/stockService";

export default function StockAdjustments() {
    // Store stock adjustment form values
    const [formData, setFormData] = useState({
        product_id: "",
        movement_type: "INCREASE",
        quantity: "",
        reason: "",
    });

    // Store available products
    const [products, setProducts] = useState([]);
    const [loadingProducts, setLoadingProducts] = useState(true);
    // Track stock adjustment submission status
    const [isSubmitting, setIsSubmitting] = useState(false);
    // Store notification message
    const [notification, setNotification] = useState(null);

    // Handle form submission adjustment
    const handleSubmit = async () => {
        if (isSubmitting) return;

        setIsSubmitting(true);
        setNotification(null);

        try {
            const payload = {
                movement_type: formData.movement_type,
                quantity: Number(formData.quantity),
                reason: formData.reason,
            };

            const result = await createStockAdjustment(
                formData.product_id,
                payload
            );

            setNotification({
                type: "success",
                message: "Stock adjustment successfully created.",
            });

            // Reset form after successful adjustment
            setFormData({
                product_id: "",
                movement_type: "INCREASE",
                quantity: "",
                reason: "",
            });

        } catch (error) {
            console.error(
                "Failed to create stock adjustment:",
                error.response?.data || error.message
            );

            setNotification({
                type: "error",
                message:
                    error.response?.data?.detail ||
                    "Failed to create stock adjustment.",
            });

        } finally {
            setIsSubmitting(false);
        }
    };

    // Fetch products when the page is mounted
    useEffect(() => {
        async function loadProducts() {
            try {
                const data = await fetchProducts();
                setProducts(data);
            } catch (error) {
                console.error("Failed to load products:", error);
            } finally {
                setLoadingProducts(false);
            }
        }

        loadProducts();
    }, []);

    return (
        <div className="p-8">
            <div className="mx-auto max-w-5xl">

                {/* Main Form Container */}
                <div className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm space-y-7">

                    {/* Form Header */}
                    <div>
                        <h1 className="text-2xl font-bold text-slate-800">
                            New Stock Adjustment
                        </h1>
                        <p className="mt-1 text-sm text-slate-500">
                            Manage inventory stock increases and decreases.
                        </p>
                    </div>

                    {/* Notification */}
                    {notification && (
                        <div
                            className={`rounded-lg border p-4 ${
                                notification.type === "success"
                                    ? "border-emerald-200 bg-emerald-50 text-emerald-700"
                                    : "border-red-200 bg-red-50 text-red-700"
                            }`}
                        >
                            <p className="text-sm font-medium">
                                {notification.message}
                            </p>
                        </div>
                    )}

                    {/* Product Selection */}
                    <div>
                        <label className="mb-2 block text-sm font-semibold text-slate-700">
                            Product
                        </label>

                        <select
                            value={formData.product_id}
                            onChange={(e) =>
                                setFormData({
                                    ...formData,
                                    product_id: e.target.value,
                                })
                            }
                            className="w-full rounded-lg border border-slate-300 bg-white px-4 py-3 text-slate-800 outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100"
                        >
                            <option value="">
                                {loadingProducts
                                    ? "Loading products..."
                                    : "Choose a product"}
                            </option>

                            {products
                                .filter((product) => product.is_active)
                                .map((product) => (
                                    <option key={product.id} value={product.id}>
                                        {product.sku} - {product.name}
                                    </option>
                            ))}
                        </select>
                    </div>

                    {/* Adjustment Type */}
                    <div>
                        <label className="mb-3 block text-sm font-semibold text-slate-700">
                            Adjustment Type
                        </label>

                        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">

                            {/* Increase Button */}
                            <button
                                type="button"
                                onClick={() =>
                                    setFormData({
                                        ...formData,
                                        movement_type: "INCREASE",
                                    })
                                }
                                className={`flex min-h-[160px] flex-col items-center justify-center gap-3 rounded-xl border-2 p-6 transition-all ${
                                    formData.movement_type === "INCREASE"
                                        ? "border-emerald-500 bg-emerald-50"
                                        : "border-slate-200 bg-white hover:border-emerald-300"
                                }`}
                            >
                                <span className="text-4xl font-light text-emerald-600">
                                    ↑
                                </span>

                                <span className="text-xl font-bold text-emerald-700">
                                    INCREASE
                                </span>

                                <span className="text-sm text-slate-500">
                                    Add stock to inventory
                                </span>
                            </button>

                            {/* Decrease Button */}
                            <button
                                type="button"
                                onClick={() =>
                                    setFormData({
                                        ...formData,
                                        movement_type: "DECREASE",
                                    })
                                }
                                className={`flex min-h-[160px] flex-col items-center justify-center gap-3 rounded-xl border-2 p-6 transition-all ${
                                    formData.movement_type === "DECREASE"
                                        ? "border-red-500 bg-red-50"
                                        : "border-slate-200 bg-white hover:border-red-300"
                                }`}
                            >
                                <span className="text-4xl font-light text-red-600">
                                    ↓
                                </span>

                                <span className="text-xl font-bold text-red-700">
                                    DECREASE
                                </span>

                                <span className="text-sm text-slate-500">
                                    Remove stock from inventory
                                </span>
                            </button>
                        </div>
                    </div>

                    <div className="border-t border-slate-200" />

                    {/* Adjustment Details */}
                    <div className="space-y-5">
                        <h2 className="text-lg font-bold text-slate-800">
                            Adjustment Details
                        </h2>

                        {/* Quantity */}
                        <div>
                            <label className="mb-2 block text-sm font-medium text-slate-700">
                                Quantity
                            </label>

                            <input
                                type="number"
                                min="1"
                                placeholder="Enter quantity..."
                                value={formData.quantity}
                                onChange={(e) =>
                                    setFormData({
                                        ...formData,
                                        quantity: e.target.value,
                                    })
                                }
                                className="w-full rounded-lg border border-slate-300 bg-white px-4 py-3 text-slate-800 outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100"
                            />
                        </div>

                        {/* Reason */}
                        <div>
                            <label className="mb-2 block text-sm font-medium text-slate-700">
                                Reason
                            </label>

                            <textarea
                                rows={4}
                                placeholder="Explain the reason for this adjustment..."
                                value={formData.reason}
                                onChange={(e) =>
                                    setFormData({
                                        ...formData,
                                        reason: e.target.value,
                                    })
                                }
                                className="w-full resize-y rounded-lg border border-slate-300 bg-white px-4 py-3 text-slate-800 outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100"
                            />
                        </div>
                    </div>

                    {/* Submit Button - submission logic will be connected next */}
                    <button
                        type="button"
                        onClick={handleSubmit}
                        disabled={isSubmitting}
                        className="w-full rounded-xl bg-emerald-600 px-6 py-4 font-semibold text-white transition-colors hover:bg-emerald-700 disabled:cursor-not-allowed disabled:opacity-60"
                    >
                        {isSubmitting ? "Submitting..." : "Submit Adjustment"}
                    </button>

                </div>
            </div>
        </div>
    );
}