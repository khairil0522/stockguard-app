export default function getActiveStatusColor(isactive) {
    if (isactive) {
        return "rounded-full bg-emerald-100 px-3 py-1 text-xs font-semibold text-emerald-700";
    }

    return "rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-600";
}