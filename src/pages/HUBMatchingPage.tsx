import { useState } from "react";
import { useNavigate } from "react-router";

export default function HUBMatchingPage() {
  const navigate = useNavigate();

  const [region, setRegion] = useState("");
  const [goal, setGoal] = useState("");

  const handleMatching = () => {
    const token = localStorage.getItem("token");

    if (!token) {
      navigate("/signin");
      return;
    }

    console.log("Run matching:", { region, goal });
  };

  return (
    <div className="min-h-screen bg-[#F7F8F7] px-4 py-10 md:px-8">
      <div className="mx-auto max-w-6xl">
        <p className="mb-4 text-sm font-semibold uppercase tracking-[0.22em] text-[#20C997]">
          Matching
        </p>

        <h1 className="text-4xl font-semibold tracking-tight text-[#111111] md:text-5xl">
          Find the right solution for you
        </h1>

        <p className="mt-4 text-lg text-[#667085]">
          Indicate your territory and need: CENet suggests the optimal path.
        </p>

        <section className="mt-10 rounded-[28px] border border-[#BDEFE1] bg-gradient-to-br from-white to-[#EAF7FF] p-6 shadow-sm md:p-8">
          <div className="grid gap-6 md:grid-cols-2">
            <div>
              <label className="mb-3 block text-sm font-semibold text-[#667085]">
                Region
              </label>
              <select
                value={region}
                onChange={(e) => setRegion(e.target.value)}
                className="h-14 w-full rounded-2xl border border-[#DDE3E8] bg-white px-5 text-base text-[#111111] outline-none focus:border-[#159570]"
              >
                <option value="">Select your region...</option>
                <option>Lombardia</option>
                <option>Lazio</option>
                <option>Piemonte</option>
                <option>Emilia-Romagna</option>
                <option>Sicilia</option>
                <option>Puglia</option>
              </select>
            </div>

            <div>
              <label className="mb-3 block text-sm font-semibold text-[#667085]">
                What are you looking for?
              </label>
              <select
                value={goal}
                onChange={(e) => setGoal(e.target.value)}
                className="h-14 w-full rounded-2xl border border-[#DDE3E8] bg-white px-5 text-base text-[#111111] outline-none focus:border-[#159570]"
              >
                <option value="">Select your goal...</option>
                <option>Join a CER</option>
                <option>Find a supplier</option>
                <option>Install PV</option>
                <option>Energy audit</option>
                <option>Storage solution</option>
              </select>
            </div>
          </div>

          <div className="mt-8 flex flex-col gap-4 md:flex-row md:items-center">
            <button
              onClick={handleMatching}
              className="rounded-full bg-gradient-to-r from-[#159570] to-[#20C997] px-7 py-4 text-sm font-semibold text-white shadow-lg hover:opacity-90"
            >
              Run matching →
            </button>

            <p className="text-sm text-[#667085]">
              To send contact requests you must be registered and logged in.
            </p>
          </div>
        </section>
      </div>
    </div>
  );
}