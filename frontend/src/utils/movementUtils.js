export default function getMovementColor(movementType) {
    if (movementType === "INCREASE") {
        return "bg-green-100 text-green-700";
    }

    return "bg-red-100 text-red-700";
}