import { useState } from "react";
import { Link, useNavigate } from "react-router";
import { ChevronLeftIcon, EyeCloseIcon, EyeIcon } from "../../icons";
import Label from "../form/Label";
import Input from "../form/input/InputField";
import Checkbox from "../form/input/Checkbox";
import { registerUser } from "../services/auth";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export default function SignUpForm() {
  const [showPassword, setShowPassword] = useState(false);
  const [isChecked, setIsChecked] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("user");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");

  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError("");

    if (!isChecked) {
      setError("Please accept the terms before creating an account.");
      return;
    }

    setIsSubmitting(true);

    try {
      await registerUser(email, password, role);
      navigate("/signin");
    } catch (err: any) {
      setError(err.message || "Sign up failed");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="flex flex-col flex-1 w-full overflow-y-auto lg:w-1/2 no-scrollbar">
      <div className="w-full max-w-md mx-auto mb-5 sm:pt-10">
        <Link
          to="/"
          className="inline-flex items-center text-sm text-gray-500 hover:text-gray-700"
        >
          <ChevronLeftIcon className="size-5" />
          Back to home
        </Link>
      </div>

      <div className="flex flex-col justify-center flex-1 w-full max-w-md mx-auto">
        <div>
          <div className="mb-6">
            <h1 className="mb-2 text-3xl font-semibold text-gray-800">
              Sign Up
            </h1>
            <p className="text-sm text-gray-500">
              Create your CENet account.
            </p>
          </div>

          <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
          <a
       href={`${API_BASE_URL}/auth/google/login`}
    className="flex items-center justify-center gap-3 rounded-lg bg-gray-100 px-4 py-3 text-sm font-medium text-gray-700 hover:bg-gray-200"
  >
    <img src="/images/brand/brand-05.svg" alt="Google" className="h-5 w-5" />
    Google
  </a>

  <a
    href={`${API_BASE_URL}/auth/microsoft/login`}
    className="flex items-center justify-center gap-3 rounded-lg bg-gray-100 px-4 py-3 text-sm font-medium text-gray-700 hover:bg-gray-200"
  >
    <img src="/images/brand/brand-17.svg" alt="Microsoft" className="h-5 w-5" />
    Microsoft
  </a>

  <a
    href={`${API_BASE_URL}/auth/linkedin/login`}
    className="flex items-center justify-center gap-3 rounded-lg bg-gray-100 px-4 py-3 text-sm font-medium text-gray-700 hover:bg-gray-200"
  >
    <img src="/images/brand/brand-16.svg" alt="LinkedIn" className="h-5 w-5" />
    LinkedIn
  </a>
</div>

          <div className="relative py-5">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-gray-200"></div>
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="bg-white px-4 text-gray-400">Or</span>
            </div>
          </div>

          <form onSubmit={handleSubmit}>
            <div className="space-y-5">
              <div>
                <Label>Email *</Label>
                <Input
                  type="email"
                  placeholder="name@company.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>

              <div>
                <Label>Password *</Label>
                <div className="relative">
                  <Input
                    placeholder="Create a password"
                    type={showPassword ? "text" : "password"}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                  />
                  <span
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-4 top-1/2 z-30 -translate-y-1/2 cursor-pointer"
                  >
                    {showPassword ? (
                      <EyeIcon className="size-5 fill-gray-500" />
                    ) : (
                      <EyeCloseIcon className="size-5 fill-gray-500" />
                    )}
                  </span>
                </div>
              </div>

              <div>
                <Label>Role *</Label>
                <select
                  value={role}
                  onChange={(e) => setRole(e.target.value)}
                  className="h-11 w-full rounded-lg border border-gray-300 bg-white px-4 text-sm text-gray-700 focus:border-[#159570] focus:outline-none focus:ring-1 focus:ring-[#159570]"
                >
                  <option value="user">User</option>
                  <option value="operator">Operator</option>
                  <option value="supplier">Supplier</option>
                </select>
              </div>

              <div className="flex items-start gap-3">
                <Checkbox
                  className="h-5 w-5"
                  checked={isChecked}
                  onChange={setIsChecked}
                />
                <p className="text-sm leading-6 text-gray-500">
                  I agree to the Terms and Conditions and Privacy Policy.
                </p>
              </div>

              {error && <p className="text-sm text-red-500">{error}</p>}

              <button
                type="submit"
                disabled={isSubmitting}
                className="flex w-full items-center justify-center rounded-lg bg-[#159570] px-4 py-3 text-sm font-medium text-white transition hover:bg-[#127a5c] disabled:opacity-60"
              >
                {isSubmitting ? "Creating account..." : "Sign Up"}
              </button>
            </div>
          </form>

          <div className="mt-5">
            <p className="text-sm text-gray-700">
              Already have an account?{" "}
              <Link to="/signin" className="text-[#159570] hover:underline">
                Sign In
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}