const ROWS = [
  { key: "off_duty", label: "1. Off Duty", y: 70 },
  { key: "sleeper", label: "2. Sleeper Berth", y: 100 },
  { key: "driving", label: "3. Driving", y: 130 },
  { key: "on_duty", label: "4. On Duty (Not Driving)", y: 160 },
];

const CHART_LEFT = 200;
const CHART_WIDTH = 900;
const HOUR_WIDTH = CHART_WIDTH / 24;

function timeToX(iso) {
  const d = new Date(iso);
  const h = d.getHours() + d.getMinutes() / 60;
  return CHART_LEFT + h * HOUR_WIDTH;
}

export default function ELDLogSheet({ day, carrier, driver, truck }) {
  const dayDate = new Date(day.date);

  return (
    <div className="bg-white p-6 my-6 shadow-md border border-slate-300 rounded-xl overflow-x-auto">
      <div className="text-center font-bold text-lg border-b-2 border-black pb-1">
        DRIVER'S DAILY LOG
      </div>
      <div className="text-center text-xs mb-3">(ONE CALENDAR DAY - 24 HOURS)</div>

      <div className="grid grid-cols-3 gap-4 text-sm mb-4">
        <div>
          <div className="border-b border-black py-1">{carrier}</div>
          <div className="text-[10px] text-slate-500">(NAME OF CARRIER)</div>
        </div>
        <div>
          <div className="border-b border-black py-1 text-center">
            {dayDate.toLocaleDateString("en-US")}
          </div>
          <div className="text-[10px] text-slate-500 text-center">(DATE)</div>
        </div>
        <div>
          <div className="border-b border-black py-1 text-right">{truck}</div>
          <div className="text-[10px] text-slate-500 text-right">(VEHICLE)</div>
        </div>
      </div>

      <svg viewBox="0 0 1120 220" className="w-full min-w-[900px]">
        {Array.from({ length: 25 }).map((_, i) => (
          <g key={i}>
            <line
              x1={CHART_LEFT + i * HOUR_WIDTH}
              y1={50}
              x2={CHART_LEFT + i * HOUR_WIDTH}
              y2={180}
              stroke="#000"
              strokeWidth={i % 2 === 0 ? 0.8 : 0.25}
            />
            {i < 24 && (
              <text
                x={CHART_LEFT + i * HOUR_WIDTH + HOUR_WIDTH / 2}
                y={42}
                textAnchor="middle"
                fontSize={10}
              >
                {i === 0 ? "Mid" : i <= 12 ? i : i - 12}
              </text>
            )}
          </g>
        ))}

        {ROWS.map((r) => (
          <g key={r.key}>
            <line
              x1={CHART_LEFT}
              y1={r.y}
              x2={CHART_LEFT + CHART_WIDTH}
              y2={r.y}
              stroke="#000"
              strokeWidth={0.5}
            />
            <text x={10} y={r.y - 4} fontSize={11}>{r.label}</text>
          </g>
        ))}

        {day.events.map((e, i) => {
          const row = ROWS.find((r) => r.key === e.status);
          if (!row) return null;
          const x1 = timeToX(e.start);
          const x2 = timeToX(e.end);
          return (
            <g key={i}>
              <line x1={x1} y1={row.y} x2={x2} y2={row.y} stroke="#2563eb" strokeWidth={5} strokeLinecap="round" />
              <line x1={x1} y1={row.y - 12} x2={x1} y2={row.y} stroke="#2563eb" strokeWidth={2} />
              <line x1={x2} y1={row.y} x2={x2} y2={row.y + 12} stroke="#2563eb" strokeWidth={2} />
            </g>
          );
        })}
      </svg>

      <div className="grid grid-cols-5 gap-4 mt-4 text-sm">
        <div className="border border-slate-300 rounded p-2 text-center">
          <div className="text-[10px] text-slate-500">Off Duty</div>
          <div className="font-bold">{day.totals.off_duty.toFixed(2)}</div>
        </div>
        <div className="border border-slate-300 rounded p-2 text-center">
          <div className="text-[10px] text-slate-500">Sleeper</div>
          <div className="font-bold">{day.totals.sleeper.toFixed(2)}</div>
        </div>
        <div className="border border-slate-300 rounded p-2 text-center">
          <div className="text-[10px] text-slate-500">Driving</div>
          <div className="font-bold">{day.totals.driving.toFixed(2)}</div>
        </div>
        <div className="border border-slate-300 rounded p-2 text-center">
          <div className="text-[10px] text-slate-500">On Duty</div>
          <div className="font-bold">{day.totals.on_duty.toFixed(2)}</div>
        </div>
        <div className="border-2 border-black rounded p-2 text-center">
          <div className="text-[10px] text-slate-500">Total</div>
          <div className="font-bold">
            {(day.totals.off_duty + day.totals.sleeper + day.totals.driving + day.totals.on_duty).toFixed(2)}
          </div>
        </div>
      </div>
    </div>
  );
}
