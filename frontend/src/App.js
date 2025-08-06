import React from "react";
import PriceChart from "./components/PriceChart";
import ChangePointTable from "./components/ChangePointTable";

function App() {
  return (
    <div style={{ padding: "20px" }}>
      <h1>Brent Oil Price Analysis Dashboard</h1>
      <PriceChart />
      <h2>Change Point Summary</h2>
      <ChangePointTable />
    </div>
  );
}

export default App;