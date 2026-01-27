"use client";

import { useState } from "react";

export default function SigninForm() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    return (
        <div className="shadow-lg flex flex-col items-center justify-center text-amber-800 bg-white p-4 rounded-lg">
            <input type="email" onChange={(e) => setEmail(e.target.value)} placeholder="Email" className="w-full" />
            <input type="password" onChange={(e) => setPassword(e.target.value)} placeholder="Password" className="w-full" />
            <button className="w-full" onClick={() => console.log(email, password)}>Sign In</button>
            <div>{email} {password}</div>
        </div>
    );
}