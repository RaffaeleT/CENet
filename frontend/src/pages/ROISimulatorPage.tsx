import { useMemo, useState } from "react";
import { useNavigate } from "react-router";
import { createRoiSimulation } from "../components/services/roi";

type UserType = "Private" | "Condominium" | "SME" | "Public body";
type MainGoal = "Join a CER" | "New PV system" | "PV + Storage" | "Energy audit";

type FormData = {
  userType: UserType | null;
  mainGoal: MainGoal | null;
  province: string;
  municipality: string;
  annualConsumption: string;
  annualBill: string;
  pvSizeKw: string;
  installationCost: string;
  electricityPrice: string;
  incentiveRate: string;
};

const userTypes: UserType[] = ["Private", "Condominium", "SME", "Public body"];
const mainGoals: MainGoal[] = ["Join a CER", "New PV system", "PV + Storage", "Energy audit"];
const provinces = ["Milano", "Roma", "Torino", "Bologna", "Cremona", "Napoli", "Bari", "Palermo"];

function ChipButton({ active, label, onClick }: { active: boolean; label: string; onClick: () => void }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`rounded-full border px-5 py-3 text-sm font-medium transition ${
        active
          ? "border-[#159570] bg-[#159570] text-white"
          : "border-[#DDE3E8] bg-white text-[#334155] hover:border-[#159570] hover:bg-[#F0FBF7]"
      }`}
    >
      {label}
    </button>
  );
}

function StepIndicator({ currentStep }: { currentStep: 1 | 2 | 3 }) {
  const steps = [
    { number: 1, label: "Profile" },
    { number: 2, label: "Details" },
    { number: 3, label: "Results" },
  ] as const;

  return (
    <div className="flex items-center justify-center gap-3 md:gap-6">
      {steps.map((step, index) => {
        const isActive = step.number === currentStep;
        const isCompleted = step.number < currentStep;

        return (
          <div key={step.number} className="flex items-center gap-3">
            <div className="flex flex-col items-center gap-2">
              <div
                className={`flex h-11 w-11 items-center justify-center rounded-full border text-base font-semibold ${
                  isActive || isCompleted
                    ? "border-[#159570] bg-[#159570] text-white"
                    : "border-[#DDE3E8] bg-white text-[#98A2B3]"
                }`}
              >
                {step.number}
              </div>
              <span
                className={`text-sm font-semibold ${
                  isActive ? "text-[#159570]" : "text-[#98A2B3]"
                }`}
              >
                {step.label}
              </span>
            </div>

            {index < steps.length - 1 && (
              <div className="mb-6 hidden h-px w-16 bg-[#DDE3E8] md:block" />
            )}
          </div>
        );
      })}
    </div>
  );
}

export default function ROISimulatorPage() {
  const navigate = useNavigate();
  const [step, setStep] = useState<1 | 2 | 3>(1);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const [formData, setFormData] = useState<FormData>({
    userType: null,
    mainGoal: null,
    province: "",
    municipality: "",
    annualConsumption: "",
    annualBill: "",
    pvSizeKw: "",
    installationCost: "",
    electricityPrice: "0.25",
    incentiveRate: "0.4",
  });

  const canContinue = useMemo(() => {
    return (
      formData.userType &&
      formData.mainGoal &&
      formData.province.trim() &&
      formData.annualConsumption.trim() &&
      formData.annualBill.trim()
    );
  }, [formData]);

  const canCalculate = useMemo(() => {
    return (
      formData.pvSizeKw.trim() &&
      formData.installationCost.trim() &&
      formData.electricityPrice.trim() &&
      formData.incentiveRate.trim()
    );
  }, [formData]);

  const updateField = <K extends keyof FormData>(key: K, value: FormData[K]) => {
    setFormData((prev) => ({ ...prev, [key]: value }));
  };

  const handleCalculate = async () => {
    const token = localStorage.getItem("token");

    if (!token) {
      navigate("/signin");
      return;
    }

    setError("");
    setIsSubmitting(true);

    try {
      const data = await createRoiSimulation({
        title: `${formData.userType} ROI simulation`,
        province: formData.province,
        annual_kwh: Number(formData.annualConsumption),
        pv_size_kw: Number(formData.pvSizeKw),
        installation_cost: Number(formData.installationCost),
        electricity_price: Number(formData.electricityPrice),
        incentive_rate: Number(formData.incentiveRate),
      });

      setResult(data);
      setStep(3);
    } catch (err: any) {
      setError(err.message || "Could not calculate ROI");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#F8FAFC] px-6 py-10">
      <div className="mx-auto max-w-7xl">
        <div className="rounded-[32px] border border-[#E5E7EB] bg-white p-8 shadow-sm md:p-12">
          <div className="mb-10 text-center">
            <div className="mb-4 inline-flex rounded-full border border-[#B7EAD9] bg-[#F0FBF7] px-4 py-2 text-xs font-semibold uppercase tracking-[0.18em] text-[#159570]">
              CENet Simulator
            </div>

            <h1 className="text-[42px] font-semibold leading-[1.02] tracking-[-0.04em] text-[#111111] md:text-[64px]">
              Calculate your energy ROI
            </h1>

            <p className="mx-auto mt-5 max-w-3xl text-lg leading-8 text-[#667085]">
              Personalized analysis: bill savings, incentives, payback and active CERs in your area.
            </p>
          </div>

          <div className="mb-10">
            <StepIndicator currentStep={step} />
          </div>

          <div className="mx-auto max-w-5xl rounded-[28px] border border-[#E5E7EB] bg-[#FBFCFD] p-6 md:p-10">
            {step === 1 && (
              <>
                <div className="mb-8">
                  <h2 className="text-3xl font-semibold tracking-[-0.02em] text-[#111111]">
                    Who are you and what are you looking for?
                  </h2>
                  <p className="mt-2 text-lg text-[#667085]">
                    This information helps calibrate calculations to your real context.
                  </p>
                </div>

                <div className="space-y-8">
                  <div>
                    <label className="mb-3 block text-sm font-semibold uppercase tracking-wide text-[#667085]">
                      User type *
                    </label>
                    <div className="flex flex-wrap gap-3">
                      {userTypes.map((type) => (
                        <ChipButton
                          key={type}
                          label={type}
                          active={formData.userType === type}
                          onClick={() => updateField("userType", type)}
                        />
                      ))}
                    </div>
                  </div>

                  <div>
                    <label className="mb-3 block text-sm font-semibold uppercase tracking-wide text-[#667085]">
                      Main goal *
                    </label>
                    <div className="flex flex-wrap gap-3">
                      {mainGoals.map((goal) => (
                        <ChipButton
                          key={goal}
                          label={goal}
                          active={formData.mainGoal === goal}
                          onClick={() => updateField("mainGoal", goal)}
                        />
                      ))}
                    </div>
                  </div>

                  <div className="grid gap-6 md:grid-cols-2">
                    <div>
                      <label className="mb-3 block text-sm font-semibold uppercase tracking-wide text-[#667085]">
                        Province *
                      </label>
                      <select
                        value={formData.province}
                        onChange={(e) => updateField("province", e.target.value)}
                        className="h-14 w-full rounded-2xl border border-[#DDE3E8] bg-white px-4 text-base text-[#111111] outline-none focus:border-[#159570]"
                      >
                        <option value="">— Select province —</option>
                        {provinces.map((province) => (
                          <option key={province} value={province}>
                            {province}
                          </option>
                        ))}
                      </select>
                    </div>

                    <div>
                      <label className="mb-3 block text-sm font-semibold uppercase tracking-wide text-[#667085]">
                        Municipality
                      </label>
                      <input
                        type="text"
                        value={formData.municipality}
                        onChange={(e) => updateField("municipality", e.target.value)}
                        placeholder="e.g. Cremona"
                        className="h-14 w-full rounded-2xl border border-[#DDE3E8] bg-white px-4 text-base text-[#111111] placeholder:text-[#98A2B3] outline-none focus:border-[#159570]"
                      />
                    </div>
                  </div>

                  <div className="grid gap-6 md:grid-cols-2">
                    <div>
                      <label className="mb-3 block text-sm font-semibold uppercase tracking-wide text-[#667085]">
                        Annual consumption (kWh) *
                      </label>
                      <input
                        type="number"
                        value={formData.annualConsumption}
                        onChange={(e) => updateField("annualConsumption", e.target.value)}
                        placeholder="e.g. 3500"
                        className="h-14 w-full rounded-2xl border border-[#DDE3E8] bg-white px-4 text-base text-[#111111] placeholder:text-[#98A2B3] outline-none focus:border-[#159570]"
                      />
                    </div>

                    <div>
                      <label className="mb-3 block text-sm font-semibold uppercase tracking-wide text-[#667085]">
                        Annual electricity bill (€) *
                      </label>
                      <input
                        type="number"
                        value={formData.annualBill}
                        onChange={(e) => updateField("annualBill", e.target.value)}
                        placeholder="e.g. 1200"
                        className="h-14 w-full rounded-2xl border border-[#DDE3E8] bg-white px-4 text-base text-[#111111] placeholder:text-[#98A2B3] outline-none focus:border-[#159570]"
                      />
                    </div>
                  </div>

                  <div className="flex justify-end">
                    <button
                      type="button"
                      disabled={!canContinue}
                      onClick={() => setStep(2)}
                      className={`h-14 rounded-full px-8 text-lg font-semibold transition ${
                        canContinue
                          ? "bg-[#159570] text-white hover:bg-[#127a5c]"
                          : "cursor-not-allowed bg-[#E5E7EB] text-[#98A2B3]"
                      }`}
                    >
                      Next →
                    </button>
                  </div>
                </div>
              </>
            )}

            {step === 2 && (
              <>
                <div className="mb-8">
                  <h2 className="text-3xl font-semibold tracking-[-0.02em] text-[#111111]">
                    Technical details
                  </h2>
                  <p className="mt-2 text-lg text-[#667085]">
                    These values are sent to the backend ROI simulator.
                  </p>
                </div>

                <div className="grid gap-6 md:grid-cols-2">
                  <div>
                    <label className="mb-3 block text-sm font-semibold uppercase tracking-wide text-[#667085]">
                      PV size (kW) *
                    </label>
                    <input
                      type="number"
                      value={formData.pvSizeKw}
                      onChange={(e) => updateField("pvSizeKw", e.target.value)}
                      placeholder="e.g. 5"
                      className="h-14 w-full rounded-2xl border border-[#DDE3E8] bg-white px-4 text-base text-[#111111] placeholder:text-[#98A2B3] outline-none focus:border-[#159570]"
                    />
                  </div>

                  <div>
                    <label className="mb-3 block text-sm font-semibold uppercase tracking-wide text-[#667085]">
                      Installation cost (€) *
                    </label>
                    <input
                      type="number"
                      value={formData.installationCost}
                      onChange={(e) => updateField("installationCost", e.target.value)}
                      placeholder="e.g. 9000"
                      className="h-14 w-full rounded-2xl border border-[#DDE3E8] bg-white px-4 text-base text-[#111111] placeholder:text-[#98A2B3] outline-none focus:border-[#159570]"
                    />
                  </div>

                  <div>
                    <label className="mb-3 block text-sm font-semibold uppercase tracking-wide text-[#667085]">
                      Electricity price (€ / kWh) *
                    </label>
                    <input
                      type="number"
                      step="0.01"
                      value={formData.electricityPrice}
                      onChange={(e) => updateField("electricityPrice", e.target.value)}
                      className="h-14 w-full rounded-2xl border border-[#DDE3E8] bg-white px-4 text-base text-[#111111] outline-none focus:border-[#159570]"
                    />
                  </div>

                  <div>
                    <label className="mb-3 block text-sm font-semibold uppercase tracking-wide text-[#667085]">
                      Incentive rate *
                    </label>
                    <input
                      type="number"
                      step="0.01"
                      value={formData.incentiveRate}
                      onChange={(e) => updateField("incentiveRate", e.target.value)}
                      className="h-14 w-full rounded-2xl border border-[#DDE3E8] bg-white px-4 text-base text-[#111111] outline-none focus:border-[#159570]"
                    />
                  </div>
                </div>

                {error && <p className="mt-6 text-sm text-red-500">{error}</p>}

                <div className="mt-8 flex justify-end gap-4">
                  <button
                    type="button"
                    onClick={() => setStep(1)}
                    className="rounded-full border border-[#DDE3E8] bg-white px-6 py-3 text-[#334155]"
                  >
                    ← Back
                  </button>

                  <button
                    type="button"
                    disabled={!canCalculate || isSubmitting}
                    onClick={handleCalculate}
                    className="rounded-full bg-[#159570] px-6 py-3 font-semibold text-white hover:bg-[#127a5c] disabled:opacity-50"
                  >
                    {isSubmitting ? "Calculating..." : "Calculate ROI →"}
                  </button>
                </div>
              </>
            )}

            {step === 3 && (
              <>
                <div className="text-center">
                  <h2 className="text-3xl font-semibold tracking-[-0.02em] text-[#111111]">
                    ROI result
                  </h2>
                  <p className="mt-3 text-[#667085]">
                    Your simulation has been saved successfully.
                  </p>
                </div>

                <div className="mt-8 rounded-2xl border border-[#E5E7EB] bg-white p-6 text-[#111111]">
                  <p><strong>Simulation ID:</strong> {result?.id}</p>
                  <p><strong>Title:</strong> {result?.title}</p>
                  <p><strong>Type:</strong> {result?.simulation_type}</p>
                  <p><strong>Created:</strong> {result?.created_at}</p>
                </div>

                <div className="mt-8 flex justify-center gap-4">
                  <button
                    type="button"
                    onClick={() => setStep(2)}
                    className="rounded-full border border-[#DDE3E8] bg-white px-6 py-3 text-[#334155]"
                  >
                    Back
                  </button>

                  <button
                    type="button"
                    onClick={() => window.location.reload()}
                    className="rounded-full bg-[#159570] px-6 py-3 font-semibold text-white hover:bg-[#127a5c]"
                  >
                    New simulation
                  </button>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}