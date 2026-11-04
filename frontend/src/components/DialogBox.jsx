    import { CircleCheck, CircleX, TriangleAlert, Info } from "lucide-react";

    export default function DialogBox({ isOpen, title, message, type, onConfirm, onCancel, confirmText, cancelText }) {
        if (!isOpen) return null;

        const icons = {
            success: <CircleCheck className="h-6 w-6 text-emerald-500" />,
            error: <CircleX className="h-6 w-6 text-red-500" />,
            warning: <TriangleAlert className="h-6 w-6 text-yellow-500" />,
            info: <Info className="h-6 w-6 text-blue-500" />,
            confirm: <TriangleAlert className="h-6 w-6 text-amber-500" />,
        };

        const buttonStyles = {
            success: "bg-emerald-500 hover:bg-emerald-600",
            error: "bg-red-500 hover:bg-red-600",
            warning: "bg-amber-500 hover:bg-amber-600",
            info: "bg-blue-500 hover:bg-blue-600",
            confirm: "bg-slate-500 hover:bg-slate-600",
        };

        return (
            <>
            <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">

                {/* Dialog Container */}
                <div className="w-full max-w-md rounded-xl bg-white p-6 shadow-xl">

                    {/* Dialog Header */}
                    <div className="flex items-center gap-3">
                        {icons[type]}

                        <h2 className="text-xl font-bold text-slate-800">
                            {title}
                        </h2>
                    </div>

                    {/* Dialog Message */}
                    <p className="mt-3 text-sm text-slate-600">
                        {message}
                    </p>

                    {/* Dialog Actions */}
                    <div className="mt-6 flex justify-end gap-3">

                        {/* Cancel Button */}
                        {type === "confirm" && onCancel && (
                            <button
                                onClick={onCancel}
                                className="rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100"
                            >
                                {cancelText || "Cancel"}
                            </button>
                        )}

                        {/* Confirm Button */}
                        <button
                            onClick={() => {
                                console.log("Confirm button clicked");
                                onConfirm?.();
                            }}
                            className={`rounded-lg px-4 py-2 text-sm font-medium text-white ${
                                buttonStyles[type] || buttonStyles.info
                            }`}
                        >
                            {confirmText || "OK"}
                        </button>

                    </div>

                </div>

            </div>  
            </>
        )
    }