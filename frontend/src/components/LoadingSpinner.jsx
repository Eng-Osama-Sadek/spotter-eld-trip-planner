export default function LoadingSpinner({ label = "Planning your trip..." }) {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <div className="animate-spin rounded-full h-12 w-12 border-b-4 border-blue-600" />
      <p className="mt-4 text-slate-600 font-medium">{label}</p>
    </div>
  );
}
