export default function AdminDashboardPage() {
  return (
    <div className="rounded-[28px] border border-[#E5E7EB] bg-white p-8 shadow-sm">
      <p className="mb-3 text-sm font-semibold uppercase tracking-[0.18em] text-[#159570]">
        Admin
      </p>
      <h1 className="text-4xl font-semibold text-[#111111]">
        Admin dashboard
      </h1>
      <p className="mt-4 text-[#667085]">
        Users, communities, events, errors, and performance metrics will be shown here.
      </p>
    </div>
  );
}