import { ArrowDownToLine, ArrowUpFromLine } from "lucide-react";

export function getMovementColor(movementType) {
    if (movementType === "INCREASE") {
        return "bg-green-100 text-green-700";
    }

    return "bg-red-100 text-red-700";
}

export function getMovementIcon(movementType) {
    if (movementType === "INCREASE") {
        return <ArrowUpFromLine className="h-4 w-4 text-green-700" />;
    }

    return <ArrowDownToLine className="h-4 w-4 text-red-700" />;
}