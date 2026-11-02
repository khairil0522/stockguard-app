import "./App.css";
import { useState } from "react";
import Sidebar from "./components/Sidebar";
import Header from "./components/Header";
import Dashboard from "./pages/Dashboard";
import Products from "./pages/Products";
import ProductDetail from "./pages/ProductDetails";
import Inventory from "./pages/Inventory";
import InventoryDetails from "./pages/InventoryDetails";
import { useProduct } from "./hooks/useProducts";
import { useInventory } from "./hooks/useInventory";

function App() {
  const [activePage, setActivePage] = useState("Dashboard");
  const { selectedProduct, handleProductDetail, handleUpdateProduct } = useProduct();
  const { selectedInventory, handleInventoryDetail } = useInventory();

  const handleNavigateToProductDetail = async (product) => {
      const detail = await handleProductDetail(product);

      if (detail) {
          setActivePage("ProductDetail");
      }
  };

  const handleNavigateToInventoryDetail = async (inventory) => {
      const detail = await handleInventoryDetail(inventory);

      if (detail) {
          setActivePage("InventoryDetail");
      }
  };

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
            <Products onViewDetail={handleNavigateToProductDetail} />
        )}

        {activePage === "ProductDetail" && selectedProduct && (
            <ProductDetail
                product={selectedProduct}
                onBack={() => setActivePage("Products")}
            />
        )}

        {activePage === "Inventory" && (
              <Inventory onViewDetail={handleNavigateToInventoryDetail} />
        )}

        {activePage === "InventoryDetail" && selectedInventory && (
            <InventoryDetails
                inventory={selectedInventory}
                onBack={() => setActivePage("Inventory")}
            />
        )}
      </main>
    </div>
  );
}

export default App;