export default function TripSummary({ summary }) {
  const cards = [
    { label: "Total Miles", value: summary.total_miles.toLocaleString() },
    { label: "Total Days", value: summary.total_days },
    { label: "Cycle Start", value: `${summary.cycle_used_start} h` },
    { label: "Cycle End", value: `${summary.cycle_used_end} h` },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {cards.map((c) => (
        <div key={c.label} className="bg-white rounded-xl shadow-sm p-5 border border-slate-200">
          <div className="text-xs text-slate-500 font-medium uppercase">{c.label}</div>
          <div className="text-2xl font-bold text-slate-900 mt-1">{c.value}</div>
        </div>
      ))}
    </div>
  );
}
