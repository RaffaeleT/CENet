import { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router";
import { getMe } from "../../components/services/auth";

export default function AuthCallback() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [error, setError] = useState("");

  useEffect(() => {
    const token = searchParams.get("token");

    if (!token) {
      setError("No token received from provider.");
      return;
    }

    localStorage.setItem("token", token);

    getMe(token)
      .then((user) => {
        if (user.role === "admin") navigate("/admin-dashboard", { replace: true });
        else if (user.role === "operator") navigate("/cer-manager", { replace: true });
        else if (user.role === "supplier") navigate("/supplier-dashboard", { replace: true });
        else navigate("/dashboard", { replace: true });
      })
      .catch(() => {
        localStorage.removeItem("token");
        setError("Authentication failed. Please try signing in again.");
      });
  }, []);

  if (error) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-center">
          <p className="text-red-500 mb-4">{error}</p>
          <a href="/signin" className="text-[#159570] hover:underline">
            Back to Sign In
          </a>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen items-center justify-center">
      <p className="text-gray-500">Signing you in…</p>
    </div>
  );
}
