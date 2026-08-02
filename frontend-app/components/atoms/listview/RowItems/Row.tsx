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
    
    let cssStyle = `h-14 border-r border-b border-gray-100 truncate ${canSticky ? 'justify-center' : ' pl-6'} flex items-center ${isNumber ? 'justify-end pr-6' : ''} text-sm font-normal`;

    if (isLast) {
        cssStyle += " pr-6";
    }

    const cssForNumber = isNumber ? '!justify-end' : '';
    const cssForCanSticky = canSticky ? '!sticky !left-0 !bg-white' : '';
    const globalCssStyle = `relative flex items-center ${cssForNumber} ${cssForCanSticky}`;

    return (
        <td
            style={{ width: maxWidth }}
            className={`px-6 py-3 border border-gray-100 min-w-fit w-fit ${canSticky ? 'sticky left-0 bg-white' : ''}`}>
            <aside className={globalCssStyle}>
                { renderItem }
            </aside>
        </td>
    )
}