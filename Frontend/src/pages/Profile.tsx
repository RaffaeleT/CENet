import { useEffect, useState } from "react";
import { getMe, logout } from "../components/services/auth";
import UserInfoCard from "../components/UserProfile/UserInfoCard";
import UserMetaCard from "../components/UserProfile/UserMetaCard";

export default function Profile() {
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (token) {
      getMe(token)
        .then((data) => setUser(data))
        .catch(() => setUser(null));
    }
  }, []);

  return (
    <div className="space-y-6 p-6">
      <h1 className="text-2xl font-semibold text-gray-800">Profile</h1>

      {user ? (
        <>
          <UserMetaCard />
          <UserInfoCard />
        </>
      ) : (
        <p className="text-gray-500">Loading profile...</p>
      )}

      <button
        onClick={() => {
          logout();
          window.location.href = "/";
        }}
        className="rounded-lg bg-[#159570] px-5 py-3 text-sm font-medium text-white hover:bg-[#127a5c]"
      >
        Logout
      </button>
    </div>
  );
}