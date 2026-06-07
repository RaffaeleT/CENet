import PageMeta from "../../components/common/PageMeta";
import AuthLayout from "./AuthPageLayout";
import SignUpForm from "../../components/auth/SignUpForm";

export default function SignUp() {
  return (
    <>
      <PageMeta
        title="CENet - Sign Up"
        description="Join CENet - Create your community energy platform account"
      />
      <AuthLayout>
        <SignUpForm />
      </AuthLayout>
    </>
  );
}
