import { useState } from "react";
import { useNavigate } from "react-router";
import { createSmeSimulation } from "../components/services/sme";

type Step = 1 | 2 | 3;

export default function SMEOptimizerPage() {
  const navigate = useNavigate();
  const [step, setStep] = useState<Step>(1);
  const [error, setError] = useState("");
  const [result, setResult] = useState<any>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const [form, setForm] = useState({
    sector: "",
    province: "",
    surface: "",
    operatingHours: "8 hours (single shift)",
    annualKwh: "",
    annualBill: "",
    consumptionProfile: "Daytime (peak F1 09–19)",
    horizon: "20 years",

    existingPv: "No (to install)",
    pvCapacity: "",
    existingStorage: "No",
    storageCapacity: "",

    contractedPower: "",
    estimatedPeak: "",
    f1: "55",
    f2: "30",
    f3: "15",

    evVehicles: "0",
    evConsumption: "15",
    financing: "No — own investment",
  });

  const update = (key: string, value: string) => {
    setForm((prev) => ({ ...prev, [key]: value }));
  };

  const totalBands =
    Number(form.f1 || 0) + Number(form.f2 || 0) + Number(form.f3 || 0);

  const handleSubmit = async () => {
    const token = localStorage.getItem("token");

    if (!token) {
      navigate("/signin");
      return;
    }

    setError("");
    setIsSubmitting(true);

    try {
      const data = await createSmeSimulation(form);
      setResult(data);
      setStep(3);
    } catch (err: any) {
      setError(err.message || "Could not calculate SME strategy");
    } finally {
      setIsSubmitting(false);
    }
  };

  const inputClass =
    "h-14 w-full rounded-2xl border border-[#E5E7EB] bg-white px-4 text-base text-[#111827] placeholder:text-[#667085] outline-none transition focus:border-[#159570] focus:ring-4 focus:ring-[#DDE3E8]/60";

  const selectClass =
    "h-14 w-full rounded-2xl border border-[#E5E7EB] bg-white px-4 text-base text-[#111827] outline-none transition focus:border-[#159570] focus:ring-4 focus:ring-[#DDE3E8]/60";

  return (
    <div className="min-h-screen bg-[#F8FAFC] px-4 py-8 md:px-8 md:py-10">
      <div className="mx-auto max-w-6xl">
        <div className="mb-8 text-center">
          <div className="mb-4 inline-flex rounded-full border border-[#B7EAD9] bg-[#F0FBF7] px-4 py-2 text-xs font-semibold uppercase tracking-[0.18em] text-[#159570]">
            SME Energy Optimizer v3.0
          </div>

          <h1 className="text-4xl font-semibold tracking-tight text-[#111827] md:text-6xl">
            Energy analysis for your business
          </h1>

          <p className="mx-auto mt-4 max-w-3xl text-lg leading-8 text-[#475467]">
            Enter your SME data and calculate the optimal strategy between PV,
            storage, CER and hybrid combinations.
          </p>
        </div>

        <div className="mb-10 flex items-center justify-center gap-4">
          {[
            [1, "SME Profile"],
            [2, "Technical"],
            [3, "Results"],
          ].map(([number, label]) => (
            <button
              key={number}
              onClick={() => setStep(number as Step)}
              className={`rounded-full border px-5 py-2 text-sm font-semibold transition ${
                step === number
                  ? "border-[#159570] bg-[#159570] text-white"
                  : "border-[#DDE3E8] bg-white text-[#334155] hover:border-[#159570] hover:bg-[#F0FBF7]"
              }`}
            >
              {label}
            </button>
          ))}
        </div>

        {error && (
          <div className="mx-auto mb-6 max-w-4xl rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
            {error}
          </div>
        )}

        {step === 1 && (
          <div className="mx-auto max-w-4xl space-y-6">
            <section className="rounded-[32px] border border-[#E5E7EB] bg-white p-6 shadow-sm md:p-10">
              <h2 className="text-2xl font-semibold text-[#111827]">
                Company profile
              </h2>

              <div className="mt-6 grid gap-6 md:grid-cols-2">
                <div>
                  <label className="mb-3 block text-sm font-semibold uppercase tracking-wide text-[#667085]">
                    Sector *
                  </label>
                  <select
                    className={selectClass}
                    value={form.sector}
                    onChange={(e) => update("sector", e.target.value)}
                  >
                    <option className="text-black" value="">
                      Select sector...
                    </option>
                    <option className="text-black">Manufacturing / Industry</option>
                    <option className="text-black">Retail / Commerce</option>
                    <option className="text-black">Office / Services</option>
                    <option className="text-black">Logistics / Warehouse</option>
                    <option className="text-black">Food / Catering</option>
                    <option className="text-black">Agri-food</option>
                    <option className="text-black">Other</option>
                  </select>
                </div>

                <div>
                  <label className="mb-3 block text-sm font-semibold uppercase tracking-wide text-[#667085]">
                    Province *
                  </label>
                  <input
                    className={inputClass}
                    placeholder="e.g. Agrigento"
                    value={form.province}
                    onChange={(e) => update("province", e.target.value)}
                  />
                </div>

                <div>
                  <label className="mb-3 block text-sm font-semibold uppercase tracking-wide text-[#667085]">
                    Company surface optional
                  </label>
                  <input
                    className={inputClass}
                    placeholder="e.g. 1200"
                    value={form.surface}
                    onChange={(e) => update("surface", e.target.value)}
                  />
                  <p className="mt-2 text-xs text-white/40">
                    Useful to estimate typical sector consumption.
                  </p>
                </div>

                <div>
                  <label className="mb-3 block text-sm font-semibold uppercase tracking-wide text-[#667085]">
                    Operating hours / day *
                  </label>
                  <select
                    className={selectClass}
                    value={form.operatingHours}
                    onChange={(e) => update("operatingHours", e.target.value)}
                  >
                    <option className="text-black">8 hours (single shift)</option>
                    <option className="text-black">12 hours (double shift)</option>
                    <option className="text-black">16 hours (partial night)</option>
                    <option className="text-black">24 hours (continuous)</option>
                  </select>
                </div>
              </div>
            </section>

            <section className="rounded-[32px] border border-white/10 bg-white/[0.04] p-6 shadow-2xl backdrop-blur-sm md:p-10">
              <h2 className="text-2xl font-semibold text-white">
                Energy consumption
              </h2>

              <div className="mt-6 grid gap-6 md:grid-cols-2">
                <div>
                  <label className="mb-3 block text-sm font-semibold uppercase tracking-wide text-white/65">
                    Annual consumption
                  </label>
                  <input
                    className={inputClass}
                    type="number"
                    placeholder="kWh/year"
                    value={form.annualKwh}
                    onChange={(e) => update("annualKwh", e.target.value)}
                  />
                </div>

                <div>
                  <label className="mb-3 block text-sm font-semibold uppercase tracking-wide text-white/65">
                    Annual bill optional
                  </label>
                  <input
                    className={inputClass}
                    type="number"
                    placeholder="€/year"
                    value={form.annualBill}
                    onChange={(e) => update("annualBill", e.target.value)}
                  />
                </div>

                <div>
                  <label className="mb-3 block text-sm font-semibold uppercase tracking-wide text-white/65">
                    Consumption profile *
                  </label>
                  <select
                    className={selectClass}
                    value={form.consumptionProfile}
                    onChange={(e) =>
                      update("consumptionProfile", e.target.value)
                    }
                  >
                    <option className="text-black">
                      Daytime (peak F1 09–19)
                    </option>
                    <option className="text-black">
                      Evening (peak F2 19–23)
                    </option>
                    <option className="text-black">
                      Continuous (F1+F2+F3 balanced)
                    </option>
                  </select>
                </div>

                <div>
                  <label className="mb-3 block text-sm font-semibold uppercase tracking-wide text-white/65">
                    Analysis horizon *
                  </label>
                  <select
                    className={selectClass}
                    value={form.horizon}
                    onChange={(e) => update("horizon", e.target.value)}
                  >
                    <option className="text-black">10 years</option>
                    <option className="text-black">15 years</option>
                    <option className="text-black">20 years</option>
                  </select>
                </div>
              </div>

              <div className="mt-8 flex justify-end">
                <button
                  onClick={() => setStep(2)}
                  className="rounded-full bg-[#159570] px-8 py-4 text-base font-semibold text-white hover:bg-[#127e56]"
                >
                  Technical details →
                </button>
              </div>
            </section>
          </div>
        )}

        {step === 2 && (
          <div className="mx-auto max-w-4xl space-y-6">
            <section className="rounded-[32px] border border-[#E5E7EB] bg-white p-6 shadow-sm md:p-10">
              <h2 className="text-2xl font-semibold text-[#111827]">
                Existing installations
              </h2>

              <div className="mt-6 grid gap-6 md:grid-cols-2">
                <div>
                  <label className="mb-3 block text-sm font-semibold uppercase tracking-wide text-[#667085]">
                    Existing PV?
                  </label>
                  <select
                    className={selectClass}
                    value={form.existingPv}
                    onChange={(e) => update("existingPv", e.target.value)}
                  >
                    <option className="text-black">No (to install)</option>
                    <option className="text-black">Yes — already installed</option>
                  </select>
                </div>

                <div>
                  <label className="mb-3 block text-sm font-semibold uppercase tracking-wide text-[#667085]">
                    Storage / BESS existing?
                  </label>
                  <select
                    className={selectClass}
                    value={form.existingStorage}
                    onChange={(e) => update("existingStorage", e.target.value)}
                  >
                    <option className="text-black">No</option>
                    <option className="text-black">Yes — already installed</option>
                  </select>
                </div>

                <input
                  className={inputClass}
                  placeholder="PV capacity (kWp)"
                  value={form.pvCapacity}
                  onChange={(e) => update("pvCapacity", e.target.value)}
                />

                <input
                  className={inputClass}
                  placeholder="BESS capacity (kWh)"
                  value={form.storageCapacity}
                  onChange={(e) => update("storageCapacity", e.target.value)}
                />
              </div>
            </section>

            <section className="rounded-[32px] border border-[#E5E7EB] bg-white p-6 shadow-sm md:p-10">
              <h2 className="text-2xl font-semibold text-[#111827]">
                Electrical parameters
                <span className="ml-3 text-xs uppercase tracking-widest text-white/35">
                  Advanced / Premium
                </span>
              </h2>

              <div className="mt-6 grid gap-6 md:grid-cols-2">
                <div>
                  <label className="mb-3 block text-sm font-semibold uppercase tracking-wide text-[#667085]">
                    Contracted power optional
                  </label>
                  <input
                    className={inputClass}
                    placeholder="e.g. 150"
                    value={form.contractedPower}
                    onChange={(e) => update("contractedPower", e.target.value)}
                  />
                  <p className="mt-2 text-xs text-white/40">
                    From your bill: available/contracted power.
                  </p>
                </div>

                <div>
                  <label className="mb-3 block text-sm font-semibold uppercase tracking-wide text-[#667085]">
                    Estimated peak optional
                  </label>
                  <input
                    className={inputClass}
                    placeholder="e.g. 120"
                    value={form.estimatedPeak}
                    onChange={(e) => update("estimatedPeak", e.target.value)}
                  />
                </div>
              </div>

              <div className="mt-8">
                <div className="mb-4 flex items-center justify-between">
                  <p className="text-sm font-semibold uppercase tracking-wide text-[#667085]">
                    Time-band distribution
                  </p>
                  <p
                    className={`text-sm font-semibold ${
                      totalBands === 100 ? "text-[#159570]" : "text-red-600"
                    }`}
                  >
                    Total: {totalBands}%
                  </p>
                </div>

                {[
                  ["f1", "F1 (9–19)"],
                  ["f2", "F2 (19–23)"],
                  ["f3", "F3 (night)"],
                ].map(([key, label]) => (
                  <div
                    key={key}
                    className="mb-5 grid grid-cols-[110px_1fr_55px] items-center gap-4"
                  >
<span className="text-sm font-semibold text-[#475467]">
                      {label}
                    </span>

                    <input
                      type="range"
                      min="0"
                      max="100"
                      value={form[key as "f1" | "f2" | "f3"]}
                      onChange={(e) => update(key, e.target.value)}
                      className="w-full accent-[#16C7D8]"
                    />

                    <span className="text-sm font-semibold text-[#22D3EE]">
                      {form[key as "f1" | "f2" | "f3"]}%
                    </span>
                  </div>
                ))}

                <p className="text-xs text-[#667085]">
                  Check that the sum is 100%. F1 = peak working hours, F3 =
                  off-peak night/holiday.
                </p>
              </div>
            </section>

            <section className="rounded-[32px] border border-[#E5E7EB] bg-white p-6 shadow-sm md:p-10">
              <h2 className="text-2xl font-semibold text-[#111827]">
                EV fleet and financing
              </h2>

              <div className="mt-6 grid gap-6 md:grid-cols-2">
                <div>
                  <label className="mb-3 block text-sm font-semibold uppercase tracking-wide text-[#667085]">
                    Number of company EVs
                  </label>
                  <input
                    className={inputClass}
                    value={form.evVehicles}
                    onChange={(e) => update("evVehicles", e.target.value)}
                  />
                </div>

                <div>
                  <label className="mb-3 block text-sm font-semibold uppercase tracking-wide text-[#667085]">
                    Consumption per vehicle
                  </label>
                  <input
                    className={inputClass}
                    value={form.evConsumption}
                    onChange={(e) => update("evConsumption", e.target.value)}
                  />
                </div>

                <div>
                  <label className="mb-3 block text-sm font-semibold uppercase tracking-wide text-[#667085]">
                    Financing planned?
                  </label>
                  <select
                    className={selectClass}
                    value={form.financing}
                    onChange={(e) => update("financing", e.target.value)}
                  >
                    <option className="text-black">No — own investment</option>
                    <option className="text-black">Yes — leasing / loan</option>
                  </select>
                </div>
              </div>

              <div className="mt-8 flex justify-between">
                <button
                  onClick={() => setStep(1)}
                  className="rounded-full border border-[#DDE3E8] px-8 py-4 text-base font-semibold text-[#475467] hover:bg-[#F0FBF7]"
                >
                  ← Back
                </button>

                <button
                  onClick={handleSubmit}
                  disabled={isSubmitting || totalBands !== 100}
                  className="rounded-full bg-[#159570] px-8 py-4 text-base font-semibold text-white hover:bg-[#127e56] disabled:opacity-50"
                >
                  {isSubmitting
                    ? "Calculating..."
                    : "Calculate SME strategy →"}
                </button>
              </div>
            </section>
          </div>
        )}

        {step === 3 && (
          <div className="mx-auto max-w-4xl rounded-[32px] border border-[#E5E7EB] bg-white p-6 shadow-sm md:p-10">
            <h2 className="text-3xl font-semibold text-[#111827]">Results</h2>

            {result ? (
              <pre className="mt-6 max-h-[500px] overflow-auto rounded-2xl bg-[#F8FAFC] p-5 text-xs text-[#111827]">
                {JSON.stringify(result, null, 2)}
              </pre>
            ) : (
              <p className="mt-3 text-[#475467]">
                Run the SME optimizer to see results.
              </p>
            )}

            <button
              onClick={() => setStep(1)}
              className="mt-8 rounded-full border border-[#DDE3E8] px-8 py-4 text-base font-semibold text-[#475467] hover:bg-[#F0FBF7]"
            >
              New analysis
            </button>
          </div>
        )}
      </div>
    </div>
  );
}