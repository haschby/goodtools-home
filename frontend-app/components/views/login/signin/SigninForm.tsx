"use client";

import { useActionState, useMemo, useState } from "react";
import Icon from "@/components/atoms/Icon";
import { Bell1Solid } from "@lineiconshq/free-icons";
import { signin, SigninState } from "@/actions/auth.actions";

interface UserModel {
    username: string;
    password: string;
}

const initialState: SigninState = { errors: [] };

export default function SigninForm({ callbackUrl }: { callbackUrl: string }) {
    const [user, setUser] = useState<UserModel>({
        username: "",
        password: "",
    });

    const [state, formAction, isPending] = useActionState(signin, initialState);
    const [hideErrors, setHideErrors] = useState(false);
    const errors = hideErrors ? [] : state.errors;

    const canActiveSignInButton = useMemo(
        () => {
        if(user.username.length > 0 && user.password.length > 0 && !isPending) {
            return { css: "text-green-300 bg-green-500 cursor-pointer", disabled: false };
        }
        return { css: "bg-gray-700 text-white cursor-not-allowed opacity-10", disabled: true };
    }, [user, isPending]);

    const handleAction = (formData: FormData) => {
        setHideErrors(false);
        setUser((prev) => ({ ...prev, password: "" }));
        formAction(formData);
    };

    return (
        <form
            action={handleAction}
            className="max-w-[40%] w-full shadow-xl rounded-md p-6 flex flex-col gap-6 bg-white">
            <div className="flex flex-col text-left gap-2">
                <h2 className="text-gray-700 text-2xl font-bold">Welcome Back !</h2>
                <p className="text-gray-500 text-sm">Enter your username and password to continue</p>
            </div>
            <input type="hidden" name="callbackUrl" value={callbackUrl} />
            <aside className="text-gray-700 flex flex-col items-center justify-center rounded-lg gap-2">
                <input
                    type="email"
                    name="username"
                    autoComplete="username"
                    required
                    value={user.username}
                    onFocus={() => setHideErrors(true)}
                    onChange={(e) => setUser({ ...user, username: e.target.value })}
                    placeholder="Email"
                    className="w-full h-14 border border-gray-100 rounded-md p-2 focus:outline-none focus:ring-1 focus:ring-gray-300 transition-all duration-300" />
                <input
                    type="password"
                    name="password"
                    autoComplete="current-password"
                    required
                    value={user.password}
                    onFocus={() => setHideErrors(true)}
                    onChange={(e) => setUser({ ...user, password: e.target.value })}
                    placeholder="Password"
                    className="w-full h-14 border border-gray-100 rounded-md p-2 focus:outline-none focus:ring-1 focus:ring-gray-300 transition-all duration-300" />
            </aside>
            {errors.length > 0 && (
                <div className="transform translate-x-0 opacity-100 flex flex-row items-start justify-start gap-4 bg-red-200/20 text-red-500 p-4 rounded-md">
                    <Icon
                        Icon={Bell1Solid}
                        size={28}
                        strokeWidth={1.5}
                        className="bg-red-300/20 text-red-500 rounded-full p-1" />
                    <div>
                        <span className="font-semibold">Authentication failed</span>
                        <ul>
                        {errors.map((error, index) => (
                            <li key={index} className="text-red-500 text-sm">- {error}</li>
                        ))}
                        </ul>
                    </div>
                </div>
            )}
            <button
                type="submit"
                disabled={canActiveSignInButton.disabled}
                className={`w-full h-14 font-semibold rounded-md p-2 transition-all duration-300 ${canActiveSignInButton.css}`}>
                {isPending ? "Signing in..." : "Sign In"}
            </button>
        </form>
    );
}
