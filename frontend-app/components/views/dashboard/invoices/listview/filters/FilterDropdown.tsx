"use client";

import { ReactNode, useRef, useState, useEffect } from 'react';
import Icon from '@/components/atoms/Icon';
import { ChevronDownSolid } from '@lineiconshq/free-icons';

interface FilterDropdownProps {
    label: string;
    selectedText: string;
    badge?: string | number | null;
    multiselect?: boolean;
    children: ReactNode;
}

export default function FilterDropdown({
    label,
    selectedText,
    badge = null,
    multiselect = false,
    children
}: FilterDropdownProps) {

    const containerRef = useRef<HTMLDivElement>(null);
    const [isOpen, setIsOpen] = useState<boolean>(false);

    useEffect(() => {
        if (!isOpen) return;

        const handleClickOutside = (event: MouseEvent) => {
            if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
                setIsOpen(false);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, [isOpen]);

    return (
        <div ref={containerRef} className="relative inline-block w-full xl:max-w-xs">
            <button
                type="button"
                aria-haspopup="listbox"
                aria-expanded={isOpen}
                onClick={() => setIsOpen(prev => !prev)}
                className="cursor-pointer w-full flex flex-row items-center justify-between gap-2 rounded-md border border-gray-200 bg-white px-3 py-2 text-sm font-semibold text-gray-800 transition-all duration-200 hover:border-gray-300">
                <span className="flex flex-row items-center gap-2 min-w-0">
                    <span className="text-gray-500 text-sm font-semibold">{label}</span>
                    <span className="truncate text-gray-800 text-sm font-semibold">{selectedText}</span>
                    {
                        badge !== null && badge !== undefined && (
                            <span className="text-green-600 font-semibold flex items-center justify-center px-1.5 py-0.5 text-[11px] rounded-lg bg-green-300/20">
                                {badge.toString()}
                            </span>
                        )
                    }
                </span>
                <Icon
                    Icon={ChevronDownSolid}
                    size={16}
                    strokeWidth={2}
                    className={`transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`} />
            </button>

            {
                isOpen && (
                    <ul
                        role="listbox"
                        aria-multiselectable={multiselect || undefined}
                        onClick={multiselect ? undefined : () => setIsOpen(false)}
                        className="absolute w-max-[200px] top-[calc(100%+6px)] left-0 w-full z-[99999] max-h-[280px] overflow-y-auto rounded-md border border-gray-200 bg-white shadow-lg">
                        {children}
                    </ul>
                )
            }
        </div>
    );
}
