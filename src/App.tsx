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

// Temporary placeholders (we replace later)
function RoiSimulator() {
  return <div className="p-6 text-xl">ROI Simulator</div>;
}

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

        {/* Layout routes */}
        <Route element={<AppLayout />}>
          <Route path="/" element={<LandingPage />} />
          <Route path="/dashboard" element={<Home />} />

          {/* YOUR PLATFORM */}
          <Route path="/roi" element={<RoiSimulator />} />
          <Route path="/sme" element={<SmeOptimizer />} />
          <Route path="/matching" element={<MatchingPage />} />
          <Route path="/services" element={<ServicesPage />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/roi-simulator" element={<ROISimulatorPage />} />
        </Route>

        {/* Fallback */}
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  );
}