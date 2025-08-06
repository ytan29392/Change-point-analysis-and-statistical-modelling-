import React, { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";

function PriceChart() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/prices")
      .then((res) => res.json())
      .then((data) => setData(data));
  }, []);

  return (
    <LineChart width={900} height={400} data={data}>
      <CartesianGrid stroke="#ccc" />
      <XAxis dataKey="Date" hide />
      <YAxis />
      <Tooltip />
      <Line type="monotone" dataKey="Price" stroke="#8884d8" dot={false} />
    </LineChart>
  );
}

export default PriceChart;
