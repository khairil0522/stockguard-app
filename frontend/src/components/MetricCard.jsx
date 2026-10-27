export default function MetricCard({ title, value, description }) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      <p className="text-sm text-slate-500">
        {title}
      </p>

      <h2 className="mt-2 text-3xl font-bold text-slate-800">
        {value}
      </h2>

      <p className="mt-2 text-sm text-slate-400">
        {description}
      </p>
    </div>
  );
}