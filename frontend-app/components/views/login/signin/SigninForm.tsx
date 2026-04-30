"use client";

import { useMemo, useState } from "react";
import Icon from "@/components/atoms/Icon";
import { Bell1Solid } from "@lineiconshq/free-icons";

interface UserModel {
    username: string;
    password: string;
}

export default function SigninForm() {
    const [username, setUsername] = useState<UserModel>({
        username: "",
        password: "",
    });

    const [errors, setErrors] = useState<string[]>([]);

    const canActiveSignInButton = useMemo(
        () => {
        if(username.username.length > 0 && username.password.length > 0) {
            return { css: "text-green-300 bg-green-500 cursor-pointer", disabled: false };
        }
        return { css: "bg-gray-700 text-white cursor-not-allowed opacity-10", disabled: true };
    }, [username]);

    const handleSubmit = (e: React.MouseEvent<HTMLButtonElement>) => {
        e.preventDefault();
        console.log(username.username, username.password);
    };

    return (
        <div className="max-w-[40%] w-full shadow-xl rounded-md p-6 flex flex-col gap-6 bg-white">
            <div className="flex flex-col text-left gap-2">
                <h2 className="text-gray-700 text-2xl font-bold">Welcome Back !</h2>
                <p className="text-gray-500 text-sm">Enter your username and password to continue</p>
            </div>
            <aside className="flex flex-col items-center justify-center rounded-lg gap-2" onSubmit={handleSubmit}>
                <input
                    type="email"
                    onFocus={() => setErrors([])}
                    onChange={(e) => setUsername({ ...username, username: e.target.value })}
                    placeholder="Email"
                    className="w-full h-14 border border-gray-100 rounded-md p-2 focus:outline-none focus:ring-1 focus:ring-gray-300 transition-all duration-300" />
                <input
                    type="password"
                    onFocus={() => setErrors([])}
                    onChange={(e) => setUsername({ ...username, password: e.target.value })}
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
                disabled={canActiveSignInButton.disabled}
                className={`w-full h-14 font-semibold rounded-md p-2 transition-all duration-300 ${canActiveSignInButton.css}`}
                onClick={handleSubmit}>Sign In
            </button>
        </div>
    );
}