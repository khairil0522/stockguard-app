export default function Header() {

  const user = "Khairil"

  return (
    <header className="flex items-center justify-between border-b border-slate-200 bg-white px-8 py-4">
      <h1 className="text-xl font-semibold text-slate-800">
        Hi, {user}
      </h1>

      <input
        type="text"
        placeholder="Search..."
        className="rounded-lg border border-slate-300 px-4 py-2 outline-none focus:border-indigo-500"
      />
    </header>
  );
}