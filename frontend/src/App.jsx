import "./App.css";
import Sidebar from "./components/Sidebar";
import Header from "./components/Header";
import MetricCard from "./components/MetricCard";
import Dashboard from "./pages/Dashboard";

function App() {

  return (
    <div className="flex min-h-screen bg-slate-100">
      <Sidebar />

      <main className="min-w-0 flex-1">
        <Header />
        <Dashboard />
      </main>
    </div>
  );
}

export default App;