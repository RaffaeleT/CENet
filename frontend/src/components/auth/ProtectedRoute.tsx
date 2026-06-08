import { Navigate, Outlet } from "react-router";
import { isLoggedIn } from "../services/auth";

export default function ProtectedRoute() {
  if (!isLoggedIn()) {
    return <Navigate to="/signin" replace />;
  }
  return <Outlet />;
}
