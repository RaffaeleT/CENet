import { BrowserRouter as Router, Routes, Route } from "react-router";
import AppLayout from "./layout/AppLayout";
import { ScrollToTop } from "./components/common/ScrollToTop";

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
import SMEOptimizerPage from "./pages/SMEOptimizerPage";
import HUBMatchingPage from "./pages/HUBMatchingPage";
import EnergyServicesPage from "./pages/EnergyServicesPage";

export default function App() {
  return (
    <Router>
      <ScrollToTop />

      <Routes>
        <Route path="/signin" element={<SignIn />} />
        <Route path="/signup" element={<SignUp />} />

        <Route element={<AppLayout />}>
          <Route path="/" element={<LandingPage />} />
          <Route path="/dashboard" element={<Home />} />
          <Route path="/admin-dashboard" element={<AdminDashboardPage />} />
          <Route path="/cer-manager" element={<CERManagerPage />} />
          <Route path="/supplier-dashboard" element={<SupplierDashboardPage />} />

          <Route path="/roi-simulator" element={<ROISimulatorPage />} />
          <Route path="/sme-optimizer" element={<SMEOptimizerPage />} />
          <Route path="/matching" element={<HUBMatchingPage />} />
          <Route path="/services" element={<EnergyServicesPage />} />

          <Route path="/profile" element={<Profile />} />
        </Route>

        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  );
}