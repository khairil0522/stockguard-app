export function formatCurrency(value, str) {
    return Number(value).toLocaleString("id-ID", {
        style: "currency",
        currency: str,
        maximumFractionDigits: 0,
    });
}