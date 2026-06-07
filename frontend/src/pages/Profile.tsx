import { useEffect, useState } from "react";
import { useNavigate } from "react-router";
import { getMe, type MeResponse } from "../components/services/auth";

export default function Profile() {
  const navigate = useNavigate();
  const [user, setUser] = useState<MeResponse | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadProfile() {
      const token = localStorage.getItem("token");

      if (!token) {
        navigate("/signin");
        return;
      }

      try {
        const data = await getMe(token);
        setUser(data);
      } catch (err: any) {
        setError(err.message || "Could not load profile");
      }
    }

    loadProfile();
  }, [navigate]);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-800 dark:text-white/90">
          Profile
        </h1>
        <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
          Your account information from CENet backend.
        </p>
      </div>

      {error && (
        <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-600">
          {error}
        </div>
      )}

      <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-800 dark:bg-white/[0.03]">
        <h2 className="text-lg font-semibold text-gray-800 dark:text-white/90">
          Personal Information
        </h2>

        {!user ? (
          <p className="mt-4 text-sm text-gray-500">Loading profile...</p>
        ) : (
          <div className="mt-6 grid gap-6 md:grid-cols-2">
            <div>
              <p className="text-xs text-gray-500">Email</p>
              <p className="mt-2 text-sm font-medium text-gray-800 dark:text-white/90">
                {user.email}
              </p>
            </div>

            <div>
              <p className="text-xs text-gray-500">Role</p>
              <p className="mt-2 text-sm font-medium capitalize text-gray-800 dark:text-white/90">
                {user.role}
              </p>
            </div>

            <div>
              <p className="text-xs text-gray-500">Full name</p>
              <p className="mt-2 text-sm font-medium text-gray-800 dark:text-white/90">
                {user.full_name || "Not added yet"}
              </p>
            </div>

            <div>
              <p className="text-xs text-gray-500">Auth provider</p>
              <p className="mt-2 text-sm font-medium text-gray-800 dark:text-white/90">
                {user.auth_provider || "Email / password"}
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}