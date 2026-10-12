import SigninGobalLayer from "@/components/views/login/signin/SigninGobalLayer";
import { sanitizeCallbackUrl } from "@/lib/auth/config";

interface SignInPageProps {
    searchParams: Promise<{ callbackUrl?: string }>;
}

export default async function SignInPage({ searchParams }: SignInPageProps) {
    const { callbackUrl } = await searchParams;

    return (
        <SigninGobalLayer callbackUrl={sanitizeCallbackUrl(callbackUrl)} />
    )
}
