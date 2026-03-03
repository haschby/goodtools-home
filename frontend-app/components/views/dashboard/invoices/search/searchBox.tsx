"use client";

import { useRef, useCallback } from "react";
import Icon from "@/components/atoms/Icon";
import { Search1Outlined } from "@lineiconshq/free-icons";
import { useQueryClient } from "@/lib/contexts/QueryClientContext";

export function SearchBox() {

    const { setQueryParams } = useQueryClient();
    const debounceRef = useRef<NodeJS.Timeout | null>(null);

    const handleChange = useCallback(
        (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        const name = e.target.name;
    
        if (debounceRef.current) {
          clearTimeout(debounceRef.current);
        }
    
        debounceRef.current = setTimeout(() => {
          setQueryParams(name, value || null);
        }, 500);
    }, [setQueryParams]);

    function setBorderWhenOpenFilters() {
        if (false) {
            return "border-r border-b border-gray-200";
        }
        return "border-r border-gray-200";
    }

    return (
        <>
            <label
                htmlFor="search-box"
                className={`${setBorderWhenOpenFilters()} py-6 pl-4 pr-2 relative w-full text-md flex items-center gap-2 z-[99999]`}>
                <Icon Icon={Search1Outlined} size={20} strokeWidth={2} />
                <input
                    name="provider"
                    id="search-box"
                    type="search"
                    onChange={handleChange}
                    placeholder="Search for invoices"
                    className="focus:outline-none active:outline-none w-full border-none"
                />
            </label>
        </>
    )
}