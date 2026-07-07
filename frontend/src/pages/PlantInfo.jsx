import { useState } from "react";
import axios from "axios";

export default function PlantInfo() {
  const [query, setQuery] = useState("");
  const [data, setData] = useState([]);

  const searchPlant = async () => {
    const res = await axios.get(
      `https://perenual.com/api/species-list?key=YOUR_KEY&q=${query}`
    );

    setData(res.data.data);
  };

  return (
    <div>
      <h1 className="text-2xl font-bold text-green-700">
        📚 Plant Info Explorer
      </h1>

      <div className="flex gap-2 mt-4">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="border p-3 rounded-xl flex-1"
          placeholder="Search plant"
        />

        <button
          onClick={searchPlant}
          className="bg-green-600 text-white px-5 rounded-xl"
        >
          Search
        </button>
      </div>

      <div className="grid md:grid-cols-2 gap-4 mt-6">
        {data.map((p, i) => (
          <div key={i} className="bg-white p-4 rounded-xl shadow">
            <h2 className="font-bold">{p.common_name}</h2>
            <p className="text-sm text-gray-500">{p.scientific_name}</p>
          </div>
        ))}
      </div>
    </div>
  );
}