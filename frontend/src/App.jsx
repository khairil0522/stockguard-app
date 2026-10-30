import "./App.css";
import { useState } from "react";
import Sidebar from "./components/Sidebar";
import Header from "./components/Header";
import Dashboard from "./pages/Dashboard";
import Products from "./pages/Products";
import ProductDetail from "./pages/ProductDetails";

function App() {
  const [activePage, setActivePage] = useState("Dashboard");
  const [selectedProduct, setSelectedProduct] = useState(null);

  return (
    <div className="flex min-h-screen bg-slate-100">
      <Sidebar 
        activePage={activePage}
        onNavigate={setActivePage}
      />

      <main className="min-w-0 flex-1">
        <Header />

        {activePage === "Dashboard" && <Dashboard />}
        {activePage === "Products" && (
            <Products
                onViewDetail={(product) => {
                    setSelectedProduct(product);
                    setActivePage("ProductDetail");
                }}
            />
        )}

        {activePage === "ProductDetail" && selectedProduct && (
            <ProductDetail
                product={selectedProduct}
                onBack={() => setActivePage("Products")}
            />
        )}
      </main>
    </div>
  );
}

export default App;