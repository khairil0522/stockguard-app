
export default function Sidebar({ activePage, onNavigate }) {
  const menuItems = [
    "Dashboard",
    "Products",
    "Stock Adjustments",
    "Bookings",
  ];

  return (
    <aside className="min-h-screen w-64 shrink-0 bg-slate-900 p-6 text-white">
      <div className="flex items-center gap-3">
        <img
          src="/logo-ka.svg"
          alt="Logo creator"
          className="h-10 w-10 rounded-lg object-cover"
        />
        <h1 className="text-2xl font-bold">StockGuard</h1>
      </div>

      <nav className="mt-8 flex flex-col gap-2">
        {menuItems.map((item) => (
          <button
            key={item}
            onClick={() => onNavigate(item)}
            className={`rounded-lg px-4 py-3 text-left transition-colors ${
              activePage === item
                ? "bg-indigo-600 text-white"
                : "text-slate-300 hover:bg-slate-800 hover:text-white"
            }`}
          >
            {item}
          </button>
        ))}
      </nav>
    </aside>
  );
}
