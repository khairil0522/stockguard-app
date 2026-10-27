export default function Sidebar() {
  return (
    <aside className="min-h-screen w-64 shrink-0 bg-slate-900 p-6 text-white">
      <img src="/logo-ka.svg" alt="Logo creator" className="h-10 w-10 rounded-lg object-cover"/>
      <h1 className="text-2xl font-bold text-white  ">StockGuard</h1>
        <nav className="mt-8 flex flex-col gap-2">
            <a href="#" className="rounded-lg bg-indigo-600 px-4 py-3 text-white">Dashboard</a>
            <a href="#" className="rounded-lg bg-indigo-600 px-4 py-3 text-white">Products</a>
            <a href="#" className="rounded-lg bg-indigo-600 px-4 py-3 text-white">Stock Adjustments</a>
            <a href="#" className="rounded-lg bg-indigo-600 px-4 py-3 text-white">Bookings</a>
        </nav>  
    </aside>
  );
}