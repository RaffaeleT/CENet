import { BrowserRouter as Router, Routes, Route } from "react-router";
import AppLayout from "./layout/AppLayout";
import { ScrollToTop } from "./components/common/ScrollToTop";

// Pages
import LandingPage from "./pages/LandingPage";
import Home from "./pages/Dashboard/Home";
import SignIn from "./pages/AuthPages/SignIn";
import SignUp from "./pages/AuthPages/SignUp";
import NotFound from "./pages/OtherPage/NotFound";
import Profile from "./pages/Profile";
import ROISimulatorPage from "./pages/ROISimulatorPage";
import CERManagerPage from "./pages/CERManagerPage";
import AdminDashboardPage from "./pages/AdminDashboardPage";
import SupplierDashboardPage from "./pages/SupplierDashboardPage";

function SmeOptimizer() {
  return <div className="p-6 text-xl">SME Optimizer</div>;
}

function MatchingPage() {
  return <div className="p-6 text-xl">HUB Matching</div>;
}

function ServicesPage() {
  return <div className="p-6 text-xl">Energy Services</div>;
}

export default function App() {
  return (
    <Router>
      <ScrollToTop />

      <Routes>
        {/* Public routes */}
        <Route path="/signin" element={<SignIn />} />
        <Route path="/signup" element={<SignUp />} />

        {/* App layout routes */}
        <Route element={<AppLayout />}>
          <Route path="/" element={<LandingPage />} />

          {/* Role dashboards */}
          <Route path="/dashboard" element={<Home />} />
          <Route path="/admin-dashboard" element={<AdminDashboardPage />} />
          <Route path="/cer-manager" element={<CERManagerPage />} />
          <Route path="/supplier-dashboard" element={<SupplierDashboardPage />} />

          {/* Platform modules */}
          <Route path="/roi-simulator" element={<ROISimulatorPage />} />
          <Route path="/sme-optimizer" element={<SmeOptimizer />} />
          <Route path="/matching" element={<MatchingPage />} />
          <Route path="/services" element={<ServicesPage />} />

          {/* Account */}
          <Route path="/profile" element={<Profile />} />
        </Route>

        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  );
}