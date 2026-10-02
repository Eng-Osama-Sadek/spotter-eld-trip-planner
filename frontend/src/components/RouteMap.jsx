import { MapContainer, TileLayer, Polyline, Marker, Popup } from "react-leaflet";
import L from "leaflet";

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
});

export default function RouteMap({ route, fuelStations }) {
  const leg1 = (route.leg1.coordinates || []).map(([lng, lat]) => [lat, lng]);
  const leg2 = (route.leg2.coordinates || []).map(([lng, lat]) => [lat, lng]);
  const center = leg1[0] || leg2[0] || [39.8, -98.5];

  return (
    <div className="bg-white rounded-xl shadow-md p-3 border border-slate-200">
      <MapContainer
        center={center}
        zoom={5}
        style={{ height: "520px", width: "100%", borderRadius: "10px" }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="&copy; OpenStreetMap contributors"
        />
        <Polyline positions={leg1} color="#2563eb" weight={5} />
        <Polyline positions={leg2} color="#16a34a" weight={5} />

        {fuelStations.map((s, i) => (
          <Marker key={i} position={[s.lat, s.lng]}>
            <Popup>
              <b>{s.name}</b>
              <br />
              {s.city}, {s.state}
              <br />
              ${s.price.toFixed(3)}/gal
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}
