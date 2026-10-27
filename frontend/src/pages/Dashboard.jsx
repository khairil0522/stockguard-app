import { useState, useEffect } from "react";
import MetricCard from "../components/MetricCard";

function getMovementColor(movementType) {
  if (movementType === "INCREASE") {
    return "bg-green-100 text-green-700";
  }

  return "bg-red-100 text-red-700";
}

export default function Dashboard() {

    const [movements, setMovements] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    const metrics = [
    {
        id: 1,
        title: "Total Products",
        value: "—",
        description: "Jumlah produk terdaftar",
    },
    {
        id: 2,
        title: "Available Stock",
        value: "—",
        description: "Total stok tersedia",
    },
    ]; 

    useEffect(() => {
    async function fetchDashboard() {
        const [statsResponse, movementsResponse] =
        await Promise.all([
            fetch("http://localhost:8000/api/v1/dashboard/stats"),
            fetch("http://localhost:8000/api/v1/stocks/"),
        ]);

        if (!statsResponse.ok || !movementsResponse.ok) {
            throw new Error("Gagal mengambil data dashboard");
        }

        const [statsData, movementsData] = await Promise.all([
            statsResponse.json(),
            movementsResponse.json(),
        ]);

        setStats(statsData);
        setMovements(movementsData);
    }

    fetchDashboard().catch(console.error);
    }, []);

    if (loading) {
        return <p className="p-8">Loading stock movements...</p>;
    }

    if (error) {
        return <p className="p-8 text-red-600">{error}</p>;
    }

    return (
    <div className="p-8">
        <h1 className="text-3xl font-bold text-slate-800">
        Dashboard
        </h1>

        <div className="mt-8 grid grid-cols-1 gap-6 md:grid-cols-2">
        {metrics.map((metric) => (
            <MetricCard
            key={metric.id}
            title={metric.title}
            value={metric.value}
            description={metric.description}
            />
        ))}
        </div>

        <div className="mt-8 grid grid-cols-1 gap-6 md:grid-cols-2">
            Total Movements : {movements.length}
        </div>

        <div className="mt-8 overflow-x-auto rounded-xl border border-slate-200 bg-white">
        <table className="w-full text-left text-sm">
            <thead className="bg-slate-50 text-slate-500">
            <tr>
                <th className="px-6 py-4 font-medium">Product</th>
                <th className="px-6 py-4 font-medium">Movement</th>
                <th className="px-6 py-4 font-medium">Quantity</th>
                <th className="px-6 py-4 font-medium">New Stock</th>
            </tr>
            </thead>

            <tbody className="divide-y divide-slate-100">
            {movements.map((movement) => (
                <tr key={movement.id} className="hover:bg-slate-50">
                <td className="px-6 py-4 font-medium text-slate-800">
                    {movement.product_name}
                </td>

                <td className="px-6 py-4">
                    <span
                        className={`rounded-full px-3 py-1 text-xs font-semibold ${getMovementColor(movement.movement_type)}`}
                    >
                        {movement.movement_type}
                    </span>
                </td>

                <td className="px-6 py-4 text-slate-600">
                    {movement.quantity}
                </td>

                <td className="px-6 py-4 text-slate-600">
                    {movement.new_on_hand}
                </td>
                </tr>
            ))}
            </tbody>
        </table>
        </div>

    </div>
    );
}
