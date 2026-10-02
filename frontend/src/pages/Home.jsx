import { useState } from "react";
import { planTrip } from "../api/client";
import TripForm from "../components/TripForm";
import RouteMap from "../components/RouteMap";
import ELDLogSheet from "../components/ELDLogSheet";
import TripSummary from "../components/TripSummary";
import StopsTimeline from "../components/StopsTimeline";
import LoadingSpinner from "../components/LoadingSpinner";

export default function Home() {
  const [trip, setTrip] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (form) => {
    setLoading(true);
    setError(null);
    setTrip(null);
    try {
      const { data } = await planTrip(form);
      setTrip(data);
    } catch (e) {
      setError(e.response?.data?.error || e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-200">
      <header className="bg-slate-900 text-white py-6 shadow-lg">
        <div className="max-w-7xl mx-auto px-6">
          <h1 className="text-3xl font-bold">Spotter ELD Trip Planner</h1>
          <p className="text-slate-400 mt-1">
            Plan your route, respect HOS rules, generate FMCSA-compliant logs
          </p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8 space-y-8">
        <TripForm onSubmit={handleSubmit} loading={loading} />

        {loading && <LoadingSpinner />}
        {error && (
          <div className="bg-red-50 border border-red-300 text-red-700 p-4 rounded-lg">
            {error}
          </div>
        )}

        {trip && (
          <>
            <TripSummary summary={trip.summary} />
            <RouteMap route={trip.route} fuelStations={trip.fuel_stations} />
            <StopsTimeline fuelStations={trip.fuel_stations} />

            <section>
              <h2 className="text-2xl font-bold mb-4">Daily Log Sheets</h2>
              {trip.daily_logs.map((day, i) => (
                <ELDLogSheet
                  key={i}
                  day={day}
                  carrier="Spotter Logistics LLC"
                  driver="John E. Doe"
                  truck="TRK-1234"
                />
              ))}
            </section>
          </>
        )}
      </main>
    </div>
  );
}
