import { useState } from "react";

export default function TripForm({ onSubmit, loading }) {
  const [form, setForm] = useState({
    current_location: "Chicago, IL",
    pickup_location: "St. Louis, MO",
    dropoff_location: "Dallas, TX",
    cycle_used_hours: 0,
  });

  const update = (key) => (e) => setForm({ ...form, [key]: e.target.value });

  const submit = (e) => {
    e.preventDefault();
    onSubmit({
      ...form,
      cycle_used_hours: parseFloat(form.cycle_used_hours) || 0,
    });
  };

  return (
    <form
      onSubmit={submit}
      className="bg-white rounded-xl shadow-md p-6 grid grid-cols-1 md:grid-cols-2 gap-4"
    >
      <div>
        <label className="block text-sm font-semibold text-slate-700 mb-1">
          Current Location
        </label>
        <input
          value={form.current_location}
          onChange={update("current_location")}
          className="w-full px-4 py-2 border border-slate-300 rounded-lg"
          required
        />
      </div>

      <div>
        <label className="block text-sm font-semibold text-slate-700 mb-1">
          Pickup Location
        </label>
        <input
          value={form.pickup_location}
          onChange={update("pickup_location")}
          className="w-full px-4 py-2 border border-slate-300 rounded-lg"
          required
        />
      </div>

      <div>
        <label className="block text-sm font-semibold text-slate-700 mb-1">
          Dropoff Location
        </label>
        <input
          value={form.dropoff_location}
          onChange={update("dropoff_location")}
          className="w-full px-4 py-2 border border-slate-300 rounded-lg"
          required
        />
      </div>

      <div>
        <label className="block text-sm font-semibold text-slate-700 mb-1">
          Current Cycle Used (Hours)
        </label>
        <input
          type="number"
          min="0"
          max="70"
          step="0.5"
          value={form.cycle_used_hours}
          onChange={update("cycle_used_hours")}
          className="w-full px-4 py-2 border border-slate-300 rounded-lg"
        />
      </div>

      <button
        type="submit"
        disabled={loading}
        className="md:col-span-2 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-400 text-white font-semibold py-3 rounded-lg"
      >
        {loading ? "Planning..." : "Plan Trip"}
      </button>
    </form>
  );
}
