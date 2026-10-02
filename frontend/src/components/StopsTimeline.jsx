export default function StopsTimeline({ fuelStations }) {
  if (!fuelStations?.length) return null;
  return (
    <div className="bg-white rounded-xl shadow-md p-6 border border-slate-200">
      <h3 className="font-bold text-lg mb-4">Cheapest Fuel Stops Along Route</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
        {fuelStations.map((s, i) => (
          <div key={i} className="border border-slate-200 rounded-lg p-3">
            <div className="font-semibold text-sm">{s.name}</div>
            <div className="text-xs text-slate-500">
              {s.address}, {s.city}, {s.state}
            </div>
            <div className="text-blue-600 font-bold mt-1">${s.price.toFixed(3)}/gal</div>
          </div>
        ))}
      </div>
    </div>
  );
}
