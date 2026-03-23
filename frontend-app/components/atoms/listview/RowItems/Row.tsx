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
        isLast = false,
        maxWidth = '200px',
        canSticky = false,
        renderItem
    }: RowItemProps
): ReactNode {
    
    let cssStyle = `h-14 border-r border-b border-gray-100 ${canSticky ? 'justify-center' : 'truncate pl-6'} flex items-center ${isNumber ? 'justify-end pr-6' : ''} text-sm font-normal`;

    if (isLast) {
        cssStyle += " pr-6";
    }

    return (
        <td
            style={{ width: maxWidth }}
            className={`min-w-fit w-fit ${canSticky ? 'sticky left-0 bg-white' : ''}`}>
            <p className={cssStyle}>
                { renderItem }
            </p>
        </td>
    )
}