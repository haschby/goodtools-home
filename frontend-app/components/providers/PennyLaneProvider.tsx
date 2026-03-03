import { PennyLanerCursorType, PennyLanerCursorContext } from "@/lib/contexts/PennyLanerCursorContext";
import { useState } from "react";

interface PennyLanerCursorContextType {
    pennyLaneCursor: PennyLanerCursorType | null;
    setPennyLanerCursor: (cursor: PennyLanerCursorType) => void;
}

export default function PennyLaneProvider(
    { children }: { children: React.ReactNode }
) {

    const [pennyLaneCursor, setPennyLanerCursor] = useState<PennyLanerCursorType | null>(null);

    const contextValue: PennyLanerCursorContextType = {
        pennyLaneCursor,
        setPennyLanerCursor,
    };

    return (
        <PennyLanerCursorContext.Provider
            value={contextValue as PennyLanerCursorContextType}>
            {children}
        </PennyLanerCursorContext.Provider>
    );
}