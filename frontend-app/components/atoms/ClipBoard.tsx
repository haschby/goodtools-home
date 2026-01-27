"use client";
import { useState } from "react";
import Icon from "@/components/atoms/Icon";
import { ClipboardSolid } from "@lineiconshq/free-icons";

interface ClipBoardProps {
    text: string;
    color?: { tone: string, level: number };
}

export default function ClipBoard(
    { text, color = { tone: 'gray', level: 300 } }: ClipBoardProps
) {
    const [isCopied, setIsCopied] = useState(false);
    const cssIcon = `text-${color.tone}-${color.level} transition-all duration-300 group-hover:text-${color.tone}-${color.level+200}`;

    const copyToClipboard = async (text: string) => {
        setIsCopied(true);
        await navigator.clipboard.writeText(text);
        setTimeout(() => {
            setIsCopied(false);
        }, 500);
    }

    return (
        <span
            className="absolute group cursor-pointer inline-flex items-center gap-2"
            onClick={() => copyToClipboard(text)}>
            <Icon
                Icon={ClipboardSolid}
                size={20}
                strokeWidth={2}
                className={cssIcon} />
            { isCopied &&
                <span className="text-xs text-gray-500">
                    Copied
                </span>
            }
        </span>
    )
}