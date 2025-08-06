import React, { useEffect, useState } from "react";

function ChangePointTable() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/change-points")
      .then((res) => res.json())
      .then((data) => setData(data));
  }, []);

  return (
    <table border="1" style={{ width: "100%", marginTop: "20px" }}>
      <thead>
        <tr>
          <th>Change Point Date</th>
          <th>Event</th>
          <th>Mean Before</th>
          <th>Mean After</th>
          <th>Impact (%)</th>
        </tr>
      </thead>
      <tbody>
        {data.map((row, index) => (
          <tr key={index}>
            <td>{row["Change Point Date"]}</td>
            <td>{row.Event}</td>
            <td>{row["Mean Before"].toFixed(6)}</td>
            <td>{row["Mean After"].toFixed(6)}</td>
            <td>{row["Impact (%)"].toFixed(2)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default ChangePointTable;
