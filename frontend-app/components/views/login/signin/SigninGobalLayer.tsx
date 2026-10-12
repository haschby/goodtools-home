"use client";
import SigninForm from "./SigninForm";

export default function SigninGobalLayer({ callbackUrl }: { callbackUrl: string }) {
    return (
        <section className="flex flex-col items-start justify-start h-full w-full bg-gray-50">
            <h1 className="font-bold tracking-tight text-gray-700 py-6 pl-4 flex flex-row justify-start w-full text-black items-center text-2xl gap-1">
                {/* <LogoGoodTools /> OODTOOLS */}
                {/* <Icon
                    Icon={Leaf1Solid}
                    size={22}
                    strokeWidth={1.5}
                    className="bg-gray-700 p-1 text-white rounded-lg relative left-0 top-0 inline-block" /> */}
                Goodtools
            </h1>
            <aside className="flex items-center justify-center w-full h-full">
                <SigninForm callbackUrl={callbackUrl} />
            </aside>
        </section>
    );
}