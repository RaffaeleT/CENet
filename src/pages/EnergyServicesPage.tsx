import { useNavigate } from "react-router";
import { BoltIcon, DocsIcon, GroupIcon } from "../icons";

const services = [
  {
    Icon: DocsIcon,
    title: "Energy Audit & Diagnosis",
    text: "In-depth consumption assessment, waste identification and prioritized intervention roadmap to maximize energy ROI.",
  },
  {
    Icon: BoltIcon,
    title: "Photovoltaic + Storage",
    text: "Sizing of PV systems integrated with BESS. Technical-economic analysis, access to GSE incentives and complete application management.",
  },
  {
    Icon: GroupIcon,
    title: "CER Community Support",
    text: "Operational assistance for energy community managers: governance tools, reporting, flow optimization and regulatory support.",
  },
];

export default function EnergyServicesPage() {
  const navigate = useNavigate();

  const handleRequest = (service: string) => {
    const token = localStorage.getItem("token");

    if (!token) {
      navigate("/signin");
      return;
    }

    alert(`Contact request created for: ${service}`);
  };

  return (
    <div className="min-h-screen bg-[#F7F8F7] px-4 py-10 md:px-8">
      <div className="mx-auto max-w-6xl space-y-20">
        <section>
          <p className="mb-4 text-sm font-semibold uppercase tracking-[0.22em] text-[#20C997]">
            Marketplace
          </p>

          <h1 className="text-4xl font-semibold tracking-tight text-[#111111] md:text-5xl">
            Tailored energy services
          </h1>

          <p className="mt-4 text-lg text-[#667085]">
            Connect with the right professionals: submit a request and get
            started.
          </p>

          <div className="mt-10 grid gap-6 md:grid-cols-3">
            {services.map((service) => (
              <div
                key={service.title}
                className="rounded-[28px] border border-[#E5E7EB] bg-white p-8 shadow-sm"
              >
                <div className="mb-8 flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-[#0098D8] to-[#29C879] shadow-lg">
                  <service.Icon className="h-10 w-10 text-white" />
                </div>

                <h2 className="text-2xl font-semibold text-[#111111]">
                  {service.title}
                </h2>

                <p className="mt-5 min-h-[120px] text-base leading-8 text-[#4F665F]">
                  {service.text}
                </p>

                <button
                  onClick={() => handleRequest(service.title)}
                  className="mt-6 rounded-full bg-gradient-to-r from-[#0098D8] to-[#29C879] px-6 py-3 text-sm font-semibold text-white shadow-lg hover:opacity-90"
                >
                  Request contact →
                </button>
              </div>
            ))}
          </div>

          <div className="mt-8 rounded-2xl border border-[#BDEFE1] bg-[#F0FBF7] p-5 text-sm font-medium text-[#4F665F]">
            Demo: requests are currently confirmed locally. Backend contact
            request connection can be added through the subscriptions/contact
            endpoint.
          </div>
        </section>

        <section>
          <p className="mb-4 text-sm font-semibold uppercase tracking-[0.22em] text-[#20C997]">
            GSE incentives
          </p>

          <h2 className="text-4xl font-semibold tracking-tight text-[#111111] md:text-5xl">
            Calculate the incentive for your CER
          </h2>

          <p className="mt-4 text-lg text-[#667085]">
            Access the official GSE simulator to estimate the due contribution.
          </p>

          <div className="mt-10 rounded-[28px] border border-[#E5E7EB] bg-white p-8 shadow-sm">
            <div className="grid gap-6 lg:grid-cols-[1fr_auto] lg:items-center">
              <div>
                <h3 className="text-2xl font-semibold text-[#111111]">
                  Official GSE Simulator
                </h3>

                <p className="mt-5 text-base leading-8 text-[#4F665F]">
                  The Energy Services Manager simulator allows you to calculate
                  the contribution for shared energy within a Renewable Energy
                  Community, based on installed capacity and consumption
                  profile.
                </p>
              </div>

              <div className="text-left lg:text-center">
                <a
                  href="https://www.autoconsumo.gse.it/"
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex rounded-full bg-gradient-to-r from-[#0098D8] to-[#29C879] px-8 py-4 text-base font-semibold text-white shadow-lg hover:opacity-90"
                >
                  ↗ Open GSE Simulator
                </a>

                <p className="mt-4 text-sm text-[#667085]">
                  Opens the official site autoconsumo.gse.it
                </p>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}