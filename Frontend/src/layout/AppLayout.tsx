import { SidebarProvider, useSidebar } from "../context/SidebarContext";
import { Outlet } from "react-router";
import AppHeader from "./AppHeader";
import Backdrop from "./Backdrop";
import AppSidebar from "./AppSidebar";

const LayoutContent: React.FC = () => {
  const { isExpanded, isHovered, isMobileOpen } = useSidebar();

  return (
    <div className="min-h-screen bg-[#F7F8F7]">
      {/* Global top banner */}
     <div className="w-full bg-gradient-to-r from-[#F5DDD0] to-[#E3E3F5] py-2 text-center text-sm text-[#0F172A]">
        Explore renewable energy tools, matching, and simulations in one platform
      </div>

      <div className="xl:flex">
        <div>
          <AppSidebar />
          <Backdrop />
        </div>

        <div
          className={`flex-1 transition-all duration-300 ease-in-out ${
            isExpanded || isHovered ? "lg:ml-[290px]" : "lg:ml-[90px]"
          } ${isMobileOpen ? "ml-0" : ""}`}
        >
          <AppHeader />

          <main className="mx-auto max-w-(--breakpoint-2xl) p-4 md:p-6">
            <Outlet />
          </main>
        </div>
      </div>
    </div>
  );
};

const AppLayout: React.FC = () => {
  return (
    <SidebarProvider>
      <LayoutContent />
    </SidebarProvider>
  );
};

export default AppLayout;
