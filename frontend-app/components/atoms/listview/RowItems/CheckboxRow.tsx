"use client";

import { ReactNode } from "react";

type CheckboxRowProps = {
    renderItem: ReactNode;
}

export function CheckboxRow() {
    return (
        <div>
            <input type="checkbox" />
        </div>
    )
}