import { useEffect, useState } from "react";
import axios from "axios";
import {
  LineChart, Line, XAxis, YAxis, Tooltip,
  BarChart, Bar, CartesianGrid
} from "recharts";

function App() {
  const [monthly, setMonthly] = useState([]);
  const [category, setCategory] = useState([]);
  const [trends, setTrends] = useState([]);
  const [overspending, setOverspending] = useState([]);

  useEffect(() => {
    Promise.all([
      axios.get("http://127.0.0.1:8000/monthly-spend"),
      axios.get("http://127.0.0.1:8000/category-breakdown"),
      axios.get("http://127.0.0.1:8000/category-trends"),
      axios.get("http://127.0.0.1:8000/overspending")
    ]).then(([m, c, t, o]) => {
      setMonthly(m.data);
      setCategory(c.data);
      setTrends(t.data);
      setOverspending(o.data);
    });
  }, []);

  const total = monthly.reduce((a, b) => a + b.total_spend, 0);

  // 🔥 overspending only
  const anomalyData = overspending
    .filter(x => x.z_score > 1)
    .map(x => ({
      category: x.category,
      z: x.z_score
    }));

  return (
    <div style={{ padding: 30 }}>

      <h1>💰 Finance Dashboard</h1>

      {/* KPI */}
      <h2>Total Spend: ₹ {total}</h2>

      {/* Monthly Trend */}
      <h2>Monthly Trend</h2>
      <LineChart width={700} height={300} data={monthly}>
        <XAxis dataKey="month" />
        <YAxis />
        <Tooltip />
        <Line dataKey="total_spend" stroke="#6366f1" />
      </LineChart>

      {/* 🔥 Stacked Bar (BEST CHART) */}
      <h2>Spending by Category per Month</h2>
      <BarChart width={700} height={300} data={trends}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="month" />
        <YAxis />
        <Tooltip />

        {Object.keys(trends[0] || {})
          .filter(k => k !== "month")
          .map((key, i) => (
            <Bar key={key} dataKey={key} stackId="a" />
          ))}
      </BarChart>

      {/* 🔥 Top Categories */}
      <h2>Top Categories</h2>
      <BarChart width={700} height={300} data={category}>
        <XAxis dataKey="category" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="amount" fill="#22c55e" />
      </BarChart>

      {/* 🔥 Overspending */}
      <h2>Overspending (Anomalies)</h2>
      <BarChart width={700} height={300} data={anomalyData}>
        <XAxis dataKey="category" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="z" fill="#ef4444" />
      </BarChart>

    </div>
  );
}

export default App;