import { ReactNode } from "react";

interface CandidatesLayoutProps {
    children: ReactNode;
    modal: ReactNode;
}

export default function CandidatesLayout({ children, modal }: CandidatesLayoutProps) {
    return (
        <section className="text-slate-800 flex flex-col h-screen">
            {children}
            {modal}
        </section>
    )
}