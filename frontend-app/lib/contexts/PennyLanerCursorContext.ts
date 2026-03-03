import { createContext, useContext } from "react";

export type PennyLanerCursorType = {
    id: string | null;
    created_at: string | null;
}

export interface PennyLanerCursorContextType {
    setPennyLanerCursor: (cursor: PennyLanerCursorType) => void;
    pennyLaneCursor: PennyLanerCursorType | null;
}

export const PennyLanerCursorContext = createContext<PennyLanerCursorContextType | null>(null);

export const usePennyLanerCursor = () => {
    const context = useContext(PennyLanerCursorContext);
    if (!context) {
        throw new Error('usePennyLanerCursor must be used within a PennyLanerCursorProvider');
    }
    return context;
};