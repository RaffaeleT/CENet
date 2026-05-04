import React from "react";
import { Link } from "react-router";
import ThemeTogglerTwo from "../../components/common/ThemeTogglerTwo";

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="relative z-1 bg-white p-6 dark:bg-gray-900 sm:p-0">
      <div className="relative flex min-h-screen w-full flex-col justify-center lg:flex-row dark:bg-gray-900 sm:p-0">
        {children}

        <div className="hidden h-screen w-full items-center justify-center bg-[radial-gradient(circle_at_top_left,#EAFBF5_0%,#F8FBFF_35%,#EAF3FF_100%)] lg:grid lg:w-1/2">
          <div className="flex max-w-md flex-col items-center px-10 text-center">
            <Link to="/" className="mb-6 flex flex-col items-center">
              <img
                src="/images/logo/logo-icon.png"
                alt="CENet Energy HUB"
                className="mb-6 h-48 w-48 object-contain"
              />

              <div className="text-3xl font-semibold leading-none">
                <span className="text-[#0E88D3]">CENet</span>{" "}
                <span className="text-[#20C997]">Energy HUB</span>
              </div>
            </Link>

            <h2 className="mt-6 text-2xl font-medium leading-tight tracking-[-0.03em] text-[#111111]">
              Community energy built for action.
            </h2>

            <p className="mt-5 text-lg leading-8 text-[#667085]">
              Simulate investments, optimize SME energy use, and connect with
              renewable energy communities in one platform.
            </p>
          </div>
        </div>

        <div className="fixed bottom-6 right-6 z-50 hidden sm:block">
          <ThemeTogglerTwo />
        </div>
      </div>
    </div>
  );
}
