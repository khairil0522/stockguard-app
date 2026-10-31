export default function InventoryCard({title, value, color}) {
    const colorClasses = {
        blue: "text-blue-600",
        amber: "text-amber-600",
        emerald: "text-emerald-600",
    };

    return (
        <>
        <div className="rounded-xl border border-slate-200 bg-white p-6">
            <p className="text-sm text-slate-500">{title}</p>
            <h3 className={`mt-2 text-3xl font-bold ${colorClasses[color]}`}>
                {value}
            </h3>
        </div>
        </>
    )
}