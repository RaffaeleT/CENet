import { useEffect } from "react";
import { useLocation, Link } from "react-router";

export default function LandingPage() {
  const location = useLocation();

  useEffect(() => {
    const hash = location.hash;
    if (hash) {
      const element = document.querySelector(hash);
      if (element) {
        element.scrollIntoView({ behavior: "smooth" });
      }
    }
  }, [location]);

  return (
    <div className="bg-[#F7F8F7] text-[#0F172A]">
      {/* Hero */}
      <section className="mx-auto max-w-7xl px-6 pb-16 pt-8">
  {/* Top text area */}
  <div className="mx-auto max-w-5xl text-center">
    <div className="mb-6 inline-flex rounded-full border border-[#20C997]/30 bg-[#20C997]/10 px-4 py-2 text-sm font-medium text-[#159570]">
      ENERGY HUB ITALY
    </div>

    <h1 className="text-5xl font-medium leading-[1.02] tracking-tight text-[#111111] md:text-7xl">
      Community energy
      <br />
      built for action
    </h1>

    <p className="mx-auto mt-8 max-w-3xl text-lg leading-8 text-[#667085]">
      Simulate investments, optimize SME energy use, and connect with the
      right renewable energy communities in one integrated platform.
    </p>

    <div className="mt-10 flex justify-center gap-4">
      <Link
        to="/roi-simulator"
        className="rounded-lg bg-[#159570] px-7 py-3 text-sm font-medium text-white hover:bg-[#127a5c]"
      >
        Start simulation
      </Link>
      <a
        href="/matching"
        className="rounded-lg border border-[#DDE3E8] bg-white px-7 py-3 text-sm font-medium text-[#0F172A] hover:bg-[#F7F8F7]"
      >
        Explore matching
      </a>
    </div>
  </div>

  {/* Image block */}
  <div className="relative mt-10">
    <div className="overflow-hidden rounded-[36px] border border-[#E6E9ED] bg-white shadow-sm">
      <img
        src="/wind-turbines-field-wind-power-station-evening-sky.jpg"
        alt="Wind turbines in field at sunset"
        className="h-[560px] w-full object-cover"
      />
      <div className="absolute inset-0 bg-[linear-gradient(180deg,rgba(255,255,255,0.06)_0%,rgba(15,23,42,0.12)_100%)]" />
    </div>

    {/* Floating cards */}
    <div className="pointer-events-none absolute inset-0 hidden lg:block">
      {/* Left main card */}
  <div className="absolute left-[-14px] top-[58%] w-[300px] -translate-y-1/2 rounded-[28px] border border-[#E6E9ED] bg-white/95 p-6 shadow-xl backdrop-blur-md">
    <div className="text-[11px] font-semibold uppercase tracking-[0.18em] text-[#20C997]">
      Simulation
    </div>
    <h3 className="mt-3 text-2xl font-medium text-[#111111]">
      ROI Simulation
    </h3>
    <p className="mt-3 text-sm leading-7 text-[#667085]">
      Estimate savings, incentives, and payback.
    </p>
  </div>

  {/* Left small support card */}
    <div className="absolute top-[18%] right-[-12px] w-[300px] rounded-[28px] border border-[#E6E9ED] bg-white/95 p-6 shadow-xl backdrop-blur-md">
    <div className="text-[11px] font-semibold uppercase tracking-[0.18em] text-[#0E88D3]">
     Matching
    </div>
    <h3 className="mt-3 text-2xl font-medium text-[#111111]">
     HUB Matching
    </h3>
      <p className="mt-3 text-sm leading-7 text-[#667085]">
       Find the right energy community or partner.
     </p>
</div>

  {/* Right main card */}
  <div className="absolute bottom-[38px] right-[-12px] w-[315px] rounded-[28px] border border-[#E6E9ED] bg-white/95 p-6 shadow-xl backdrop-blur-md">
    <div className="text-[11px] font-semibold uppercase tracking-[0.18em] text-[#F0B44C]">
      Optimization
    </div>
    <h3 className="mt-3 text-2xl font-medium text-[#111111]">
      SME Optimization
    </h3>
    <p className="mt-3 text-sm leading-7 text-[#667085]">
      Explore energy strategies and reduce costs.
        </p>
      </div>
    </div>
  </div>
</section>

      {/* Stats - boxed but premium */}
<section className="w-full bg-[#F7F8F7] py-10">
  <div className="mx-auto max-w-10xl px-6">
    <div className="-mt-12 grid gap-4 md:grid-cols-2 xl:grid-cols-4">

      {/* Card */}
      <div className="group rounded-[28px] border border-[#E6E9ED] bg-white p-8 transition-all duration-300 hover:shadow-md hover:-translate-y-1">
        <div className="text-4xl font-semibold bg-gradient-to-r from-[#0E88D3] to-[#20C997] bg-clip-text text-transparent md:text-5xl">
          240+
        </div>
        <p className="mt-4 text-sm leading-6 text-[#667085]">
          Active energy communities in Italy
        </p>
      </div>

      <div className="group rounded-[28px] border border-[#E6E9ED] bg-white p-8 transition-all duration-300 hover:shadow-md hover:-translate-y-1">
        <div className="text-4xl font-semibold bg-gradient-to-r from-[#0E88D3] to-[#20C997] bg-clip-text text-transparent md:text-5xl">
          5 GW
        </div>
        <p className="mt-4 text-sm leading-6 text-[#667085]">
          Installable potential by 2030
        </p>
      </div>

      <div className="group rounded-[28px] border border-[#E6E9ED] bg-white p-8 transition-all duration-300 hover:shadow-md hover:-translate-y-1">
        <div className="text-4xl font-semibold bg-gradient-to-r from-[#0E88D3] to-[#20C997] bg-clip-text text-transparent md:text-5xl">
          40%
        </div>
        <p className="mt-4 text-sm leading-6 text-[#667085]">
          Average bill savings with CER
        </p>
      </div>

      <div className="group rounded-[28px] border border-[#E6E9ED] bg-white p-8 transition-all duration-300 hover:shadow-md hover:-translate-y-1">
        <div className="text-4xl font-semibold bg-gradient-to-r from-[#0E88D3] to-[#20C997] bg-clip-text text-transparent md:text-5xl">
          €110
        </div>
        <p className="mt-4 text-sm leading-6 text-[#667085]">
          GSE incentive per shared MWh
        </p>
      </div>

    </div>
  </div>
</section>

      {/* Info section */}
<section  id="about" className="mx-auto max-w-5xl px-6 py-16">
  <h2 className="text-[48px] font-medium leading-[1.1] tracking-[-0.02em] text-[#111111] md:text-[42px]">
    CENet is the operating platform for community energy
  </h2>

  <div className="mt-6 space-y-6 text-[16px] leading-[1.7] text-[#111111]">
    <p>
      CENet helps users, SMEs, and service providers navigate the renewable
      energy ecosystem through one integrated digital platform. By combining
      simulation, matching, and service access, it turns a fragmented process
      into a clear and actionable user journey.
    </p>

    <p>
      The platform supports each stage of the decision process — from
      evaluating savings and incentives to identifying the right energy
      community, partner, or technical service. Rather than acting as a
      simple directory, CENet creates a guided path from exploration to
      implementation.
    </p>

    <p>
      By bringing together practical tools and ecosystem actors in one place,
      CENet is designed to support local renewable energy adoption today while
      remaining scalable across regions, users, and future services.
    </p>
  </div>
</section>

{/* Applications heading */}
<section className="mx-auto max-w-5xl px-6 py-16 text-center">
  <h2 className="mx-auto text-[42px] font-medium leading-[1.1] tracking-[-0.02em] text-[#111111] md:text-[46px]">
    Introducing the CENet platform applications
  </h2>

  <p className="mt-4 text-xl leading-8 text-[#6B7280]">
    Simulation, optimization, matching, and services — aligned in one platform
    for community energy decisions.
  </p>
</section>

{/* Large showcase block */}
{/* Image with overlay text */}
<section className="mx-auto max-w-7xl px-6 pb-10">
  <div className="relative overflow-hidden rounded-[34px]">

    {/* Background image */}
    <img
      src="/3d-solar-pannels-project-energy-saving.jpg"
      alt="Solar panels and wind turbines"
      className="h-[520px] w-full object-cover"
    />

    {/* Dark overlay (important for readability) */}
    <div className="absolute inset-0 bg-black/10" />

    {/* Text content */}
    <div className="absolute inset-0 flex items-center">
      <div className="max-w-xl px-10 md:px-16">

        <h3 className="text-[36px] font-medium leading-tight text-white md:text-[28px]">
          The platform for community energy
        </h3>

       <p className="mt-6 text-[18px] leading-[1.7] font-light text-white/90 md:text-[18px]">
          From simulation and optimization to matching and service access,
          CENet brings the renewable energy ecosystem into one connected
          digital experience.
        </p>

       <p className="mt-6 text-[18px] leading-[1.7] font-light text-white/90 md:text-[18px]">
          Built to simplify a fragmented ecosystem, the platform helps users
          identify opportunities, compare solutions, and move from planning
          to implementation with clarity.
        </p>

      </div>
    </div>

  </div>
</section>

      {/* Applications */}
      <section className="mx-auto max-w-7xl px-6 pb-20">
  <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
    <div className="flex min-h-[320px] flex-col justify-between rounded-[28px] border border-[#BEEFD9] bg-white p-8 shadow-sm">
      <div>
        <div className="mb-4 text-xs font-semibold uppercase tracking-[0.18em] text-[#20C997]">
          New
        </div>
        <h3 className="text-[28px] font-medium leading-tight tracking-[-0.02em] text-[#111111]">
          ROI Simulator
        </h3>
        <p className="mt-6 text-[18px] leading-[1.7] text-[#667085]">
          Calculate savings, incentives, and investment payback in a simple
          workflow.
        </p>
      </div>
    </div>

    <div className="flex min-h-[320px] flex-col justify-between rounded-[28px] border border-[#F1CC83] bg-white p-8 shadow-sm">
      <div>
        <div className="mb-4 text-xs font-semibold uppercase tracking-[0.18em] text-[#D89B21]">
          SME
        </div>
        <h3 className="text-[28px] font-medium leading-tight tracking-[-0.02em] text-[#111111]">
          SME Optimizer
        </h3>
        <p className="mt-6 text-[18px] leading-[1.7] text-[#667085]">
          Explore energy strategies for PV, storage, community participation,
          and ESG goals.
        </p>
      </div>
    </div>

    <div className="flex min-h-[320px] flex-col justify-between rounded-[28px] border border-[#B9DEFF] bg-white p-8 shadow-sm">
      <div>
        <div className="mb-4 text-xs font-semibold uppercase tracking-[0.18em] text-[#0E88D3]">
          Directory
        </div>
        <h3 className="text-[28px] font-medium leading-tight tracking-[-0.02em] text-[#111111]">
          HUB Matching
        </h3>
        <p className="mt-6 text-[18px] leading-[1.7] text-[#667085]">
          Find the right energy community, partner, or service provider for
          your profile.
        </p>
      </div>
    </div>

    <div className="flex min-h-[320px] flex-col justify-between rounded-[28px] border border-[#E5E7EB] bg-white p-8 shadow-sm">
      <div>
        <div className="mb-4 text-xs font-semibold uppercase tracking-[0.18em] text-[#667085]">
          Services
        </div>
        <h3 className="text-[28px] font-medium leading-tight tracking-[-0.02em] text-[#111111]">
          Energy Services
        </h3>
        <p className="mt-6 text-[18px] leading-[1.7] text-[#667085]">
          Access technical support, consulting, and useful tools for
          implementation.
        </p>
      </div>
    </div>
  </div>
</section>

{/* Newsletter */}
<section id="newsletter" className="mx-auto max-w-7xl px-6 pb-24 pt-2">
  <div className="rounded-[32px] border border-[#E5E7EB] bg-[#FBFCFD] px-8 py-10 md:px-12 md:py-12">
    <div className="grid gap-10 lg:grid-cols-[1.05fr_0.95fr] lg:items-end">
      {/* Left side */}
      <div className="max-w-2xl">
        <div className="mb-4 text-sm font-semibold uppercase tracking-[0.18em] text-[#20C997]">
          Newsletter
        </div>

        <h2 className="text-[38px] font-medium leading-[1.02] tracking-[-0.03em] text-[#111111] md:text-[45px]">
          Stay updated on the future of community energy.
        </h2>

        <p className="mt-5 max-w-xl text-[18px] leading-[1.7] text-[#6B7280]">
          Get selected updates on platform releases, regulatory changes,
          incentive developments, and news across the renewable energy
          ecosystem.
        </p>
      </div>

      {/* Right side */}
      <div className="w-full">
        <label
          htmlFor="newsletter-email"
          className="mb-3 block text-sm font-medium text-[#111111]"
        >
          Work email
        </label>

        <div className="flex flex-col gap-4 sm:flex-row sm:items-end">
          <div className="flex-1">
            <input
              id="newsletter-email"
              type="email"
              placeholder="name@company.com"
              className="h-14 w-full border-0 border-b border-[#C8D2E0] bg-transparent px-0 text-[17px] text-[#111111] placeholder:text-[#98A2B3] focus:border-[#111111] focus:outline-none focus:ring-0"
            />
            <p className="mt-3 text-sm text-[#6B7280]">
              Occasional updates. No spam.
            </p>
          </div>

          <button
            type="button"
            className="inline-flex h-14 items-center justify-center rounded-full bg-[#159570] px-7 text-[16px] font-medium text-white transition hover:bg-black"
          >
            Subscribe →
          </button>
        </div>
      </div>
    </div>
  </div>
</section>
    </div>
  );
}