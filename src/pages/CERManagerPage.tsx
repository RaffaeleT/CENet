import { useEffect, useMemo, useState } from "react";
import {
  addCommunityMember,
  createCommunity,
  getCommunityDashboard,
  getCommunityMembers,
  getMyCommunities,
} from "../components/services/communities";

type Community = {
  id: number;
  name: string;
  region?: string;
  province?: string;
  description?: string;
  status?: string;
};

type Member = {
  id?: number;
  email?: string;
  role?: string;
  status?: string;
};

export default function CERManagerPage() {
  const [communities, setCommunities] = useState<Community[]>([]);
  const [selectedCommunityId, setSelectedCommunityId] = useState<number | null>(null);
  const [dashboardData, setDashboardData] = useState<any>(null);
  const [members, setMembers] = useState<Member[]>([]);

  const [name, setName] = useState("");
  const [region, setRegion] = useState("");
  const [province, setProvince] = useState("");
  const [description, setDescription] = useState("");

  const [memberEmail, setMemberEmail] = useState("");
  const [memberRole, setMemberRole] = useState("member");

  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [isCreating, setIsCreating] = useState(false);
  const [isAddingMember, setIsAddingMember] = useState(false);

  const selectedCommunity = useMemo(
    () => communities.find((community) => community.id === selectedCommunityId),
    [communities, selectedCommunityId]
  );

  async function loadCommunities() {
    const data = await getMyCommunities();
    const list = Array.isArray(data) ? data : [];

    setCommunities(list);

    if (list.length > 0 && !selectedCommunityId) {
      setSelectedCommunityId(list[0].id);
    }
  }

  async function loadSelectedCommunityData(communityId: number) {
    const [dashboard, memberData] = await Promise.all([
      getCommunityDashboard(communityId),
      getCommunityMembers(communityId),
    ]);

    setDashboardData(dashboard);
    setMembers(Array.isArray(memberData) ? memberData : []);
  }

  useEffect(() => {
    async function init() {
      try {
        setIsLoading(true);
        setError("");
        await loadCommunities();
      } catch (err: any) {
        setError(err.message || "Could not load communities");
      } finally {
        setIsLoading(false);
      }
    }

    init();
  }, []);

  useEffect(() => {
    if (!selectedCommunityId) return;

    async function loadDetails() {
      try {
        setError("");
        await loadSelectedCommunityData(selectedCommunityId!);
      } catch (err: any) {
        setError(err.message || "Could not load community details");
      }
    }

    loadDetails();
  }, [selectedCommunityId]);

  async function handleCreateCommunity() {
    setError("");

    if (!name || !region || !province) {
      setError("Name, region, and province are required.");
      return;
    }

    try {
      setIsCreating(true);

      const created = await createCommunity({
        name,
        region,
        province,
        description,
      });

      setName("");
      setRegion("");
      setProvince("");
      setDescription("");

      await loadCommunities();

      if (created?.id) {
        setSelectedCommunityId(created.id);
      }
    } catch (err: any) {
      setError(err.message || "Could not create community");
    } finally {
      setIsCreating(false);
    }
  }

  async function handleAddMember() {
    if (!selectedCommunityId) {
      setError("Select a community before adding members.");
      return;
    }

    if (!memberEmail) {
      setError("Member email is required.");
      return;
    }

    try {
      setIsAddingMember(true);
      setError("");

      await addCommunityMember(selectedCommunityId!, {
        email: memberEmail,
        role: memberRole,
      });

      setMemberEmail("");
      setMemberRole("member");

      await loadSelectedCommunityData(selectedCommunityId!);
    } catch (err: any) {
      setError(err.message || "Could not add member");
    } finally {
      setIsAddingMember(false);
    }
  }

  const totalCommunities = communities.length;
  const totalMembers =
    dashboardData?.total_members ?? dashboardData?.members_count ?? members.length;
  const totalEvents =
    dashboardData?.total_events ?? dashboardData?.events_count ?? 0;
  const totalSimulations =
    dashboardData?.total_simulations ?? dashboardData?.simulations_count ?? 0;

  return (
    <div className="space-y-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-800 dark:text-white/90">
          CER Manager
        </h1>
        <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
          Manage communities, members, events, simulations, and renewable energy activity.
        </p>
      </div>

      {error && (
        <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-600">
          {error}
        </div>
      )}

      {isLoading && (
        <div className="rounded-xl border border-gray-200 bg-white p-4 text-sm text-gray-500 dark:border-gray-800 dark:bg-white/[0.03] dark:text-gray-400">
          Loading CER manager data...
        </div>
      )}

      <div className="grid grid-cols-12 gap-4 md:gap-6">
        {[
          ["Communities", totalCommunities],
          ["Members", totalMembers],
          ["Events", totalEvents],
          ["CER Simulations", totalSimulations],
        ].map(([label, value]) => (
          <div
            key={label}
            className="col-span-12 rounded-2xl border border-gray-200 bg-white p-5 shadow-sm dark:border-gray-800 dark:bg-white/[0.03] sm:col-span-6 xl:col-span-3"
          >
            <span className="text-sm text-gray-500 dark:text-gray-400">{label}</span>
            <h3 className="mt-3 text-2xl font-bold text-gray-800 dark:text-white/90">
              {value}
            </h3>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-12 gap-4 md:gap-6">
        <div className="col-span-12 rounded-2xl border border-gray-200 bg-white p-5 shadow-sm dark:border-gray-800 dark:bg-white/[0.03] xl:col-span-5">
          <h2 className="text-lg font-semibold text-gray-800 dark:text-white/90">
            Create community
          </h2>

          <div className="mt-5 space-y-4">
            <input
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Community name"
              className="h-11 w-full rounded-lg border border-gray-300 px-4 text-sm outline-none focus:border-[#159570] dark:border-gray-700 dark:bg-gray-900 dark:text-white"
            />

            <input
              value={region}
              onChange={(e) => setRegion(e.target.value)}
              placeholder="Region"
              className="h-11 w-full rounded-lg border border-gray-300 px-4 text-sm outline-none focus:border-[#159570] dark:border-gray-700 dark:bg-gray-900 dark:text-white"
            />

            <input
              value={province}
              onChange={(e) => setProvince(e.target.value)}
              placeholder="Province"
              className="h-11 w-full rounded-lg border border-gray-300 px-4 text-sm outline-none focus:border-[#159570] dark:border-gray-700 dark:bg-gray-900 dark:text-white"
            />

            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Description"
              rows={4}
              className="w-full rounded-lg border border-gray-300 px-4 py-3 text-sm outline-none focus:border-[#159570] dark:border-gray-700 dark:bg-gray-900 dark:text-white"
            />

            <button
              onClick={handleCreateCommunity}
              disabled={isCreating}
              className="rounded-lg bg-[#159570] px-5 py-3 text-sm font-medium text-white hover:bg-[#127a5c] disabled:opacity-60"
            >
              {isCreating ? "Creating..." : "Create community"}
            </button>
          </div>
        </div>

        <div className="col-span-12 rounded-2xl border border-gray-200 bg-white p-5 shadow-sm dark:border-gray-800 dark:bg-white/[0.03] xl:col-span-7">
          <div className="mb-5 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h2 className="text-lg font-semibold text-gray-800 dark:text-white/90">
                My communities
              </h2>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                Select a community to load dashboard and members.
              </p>
            </div>

            {communities.length > 0 && (
              <select
                value={selectedCommunityId ?? ""}
                onChange={(e) => setSelectedCommunityId(Number(e.target.value))}
                className="h-11 rounded-lg border border-gray-300 bg-white px-4 text-sm text-gray-700 outline-none dark:border-gray-700 dark:bg-gray-900 dark:text-white"
              >
                {communities.map((community) => (
                  <option key={community.id} value={community.id}>
                    {community.name}
                  </option>
                ))}
              </select>
            )}
          </div>

          {communities.length === 0 ? (
            <div className="rounded-xl border border-dashed border-gray-300 bg-gray-50 p-8 text-center dark:border-gray-700 dark:bg-gray-900">
              <p className="text-sm font-medium text-gray-800 dark:text-white/90">
                No communities yet
              </p>
              <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
                Create your first CER community to start managing members and events.
              </p>
            </div>
          ) : (
            <div className="space-y-3">
              {communities.map((community) => (
                <button
                  key={community.id}
                  onClick={() => setSelectedCommunityId(community.id)}
                  className={`w-full rounded-xl border p-4 text-left transition ${
                    selectedCommunityId === community.id
                      ? "border-[#159570] bg-[#F0FBF7]"
                      : "border-gray-200 bg-gray-50 hover:border-[#159570]"
                  }`}
                >
                  <div className="flex items-start justify-between gap-4">
                    <div>
                      <h3 className="font-semibold text-gray-800">{community.name}</h3>
                      <p className="mt-1 text-sm text-gray-500">
                        {community.region || "No region"} · {community.province || "No province"}
                      </p>
                    </div>
                    <span className="rounded-full bg-white px-3 py-1 text-xs font-medium text-[#159570]">
                      {community.status || "Active"}
                    </span>
                  </div>
                </button>
              ))}
            </div>
          )}
        </div>
      </div>

      <div className="grid grid-cols-12 gap-4 md:gap-6">
        <div className="col-span-12 rounded-2xl border border-gray-200 bg-white p-5 shadow-sm dark:border-gray-800 dark:bg-white/[0.03] xl:col-span-5">
          <h2 className="text-lg font-semibold text-gray-800 dark:text-white/90">
            Add member
          </h2>
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
            {selectedCommunity
              ? `Invite a member to ${selectedCommunity.name}.`
              : "Select a community first."}
          </p>

          <div className="mt-5 space-y-4">
            <input
              value={memberEmail}
              onChange={(e) => setMemberEmail(e.target.value)}
              placeholder="member@email.com"
              className="h-11 w-full rounded-lg border border-gray-300 px-4 text-sm outline-none focus:border-[#159570] dark:border-gray-700 dark:bg-gray-900 dark:text-white"
            />

            <select
              value={memberRole}
              onChange={(e) => setMemberRole(e.target.value)}
              className="h-11 w-full rounded-lg border border-gray-300 bg-white px-4 text-sm text-gray-700 outline-none focus:border-[#159570] dark:border-gray-700 dark:bg-gray-900 dark:text-white"
            >
              <option value="member">Member</option>
              <option value="manager">Manager</option>
              <option value="viewer">Viewer</option>
            </select>

            <button
              onClick={handleAddMember}
              disabled={isAddingMember || !selectedCommunityId}
              className="rounded-lg bg-[#159570] px-5 py-3 text-sm font-medium text-white hover:bg-[#127a5c] disabled:opacity-60"
            >
              {isAddingMember ? "Adding..." : "Add member"}
            </button>
          </div>
        </div>

        <div className="col-span-12 rounded-2xl border border-gray-200 bg-white p-5 shadow-sm dark:border-gray-800 dark:bg-white/[0.03] xl:col-span-7">
          <h2 className="text-lg font-semibold text-gray-800 dark:text-white/90">
            Members
          </h2>

          <div className="mt-5 overflow-hidden rounded-xl border border-gray-200 dark:border-gray-800">
            <table className="w-full text-left text-sm">
              <thead className="bg-gray-50 text-gray-500 dark:bg-gray-900 dark:text-gray-400">
                <tr>
                  <th className="px-5 py-4 font-medium">Email</th>
                  <th className="px-5 py-4 font-medium">Role</th>
                  <th className="px-5 py-4 font-medium">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 dark:divide-gray-800">
                {members.length === 0 ? (
                  <tr>
                    <td colSpan={3} className="px-5 py-6 text-center text-gray-500">
                      No members found.
                    </td>
                  </tr>
                ) : (
                  members.map((member, index) => (
                    <tr key={member.id ?? index}>
                      <td className="px-5 py-4 text-gray-800 dark:text-white/90">
                        {member.email || "No email"}
                      </td>
                      <td className="px-5 py-4 text-gray-500">{member.role || "member"}</td>
                      <td className="px-5 py-4">
                        <span className="rounded-full bg-[#F0FBF7] px-3 py-1 text-xs text-[#159570]">
                          {member.status || "Active"}
                        </span>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {dashboardData && (
        <div className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm dark:border-gray-800 dark:bg-white/[0.03]">
          <h2 className="text-lg font-semibold text-gray-800 dark:text-white/90">
            Community dashboard data
          </h2>
          <pre className="mt-4 max-h-80 overflow-auto rounded-xl bg-gray-900 p-4 text-xs text-white">
            {JSON.stringify(dashboardData, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}