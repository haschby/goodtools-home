"use client";

import { ReactNode } from "react";

type RowItemProps = {
    isNumber?: boolean;
    isFirst?: boolean;
    isLast?: boolean;
    maxWidth?: string;
    canSticky?: boolean;
    renderItem: ReactNode;
}

export function RowItem(
    { 
        isNumber = false,
        isFirst = false,
        isLast = false,
        canSticky = false,
        renderItem
    }: RowItemProps
): ReactNode {
    
    let cssStyle = `${canSticky ? 'z-[99999] border-r border-gray-100' : ''} px-6 flex items-center ${isNumber ? 'justify-end' : 'justify-start'}  overflow-hidden whitespace-normal break-words py-3 text-sm font-normal`;

    if (isFirst) {
        cssStyle += " pl-6";
    }
    if (isLast) {
        cssStyle += " pr-6";
    }


    return (
        <td className={`min-w-fit w-fit border-r border-gray-100 ${canSticky ? 'sticky left-0 bg-white border-r-0' : ''}`}>
            <p className={cssStyle}>
                { renderItem }
            </p>
        </td>
    )
}