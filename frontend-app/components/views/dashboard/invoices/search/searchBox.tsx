"use client";

import { useRef, useCallback } from "react";
import Icon from "@/components/atoms/Icon";
import { Database2Stroke } from "@lineiconshq/free-icons";
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


    return (
        <>
            <label
                htmlFor="search-box"
                className={`w-full text-md flex items-center h-full text-gray-800`}>
                <span className="flex items-center justify-center p-4 bg-gray-200 rounded-l-xl">
                    <Icon
                        Icon={Database2Stroke}
                        size={22}
                        strokeWidth={2}
                        className="text-gray-600" />
                </span>
                <input
                    name="provider"
                    id="search-box"
                    type="search"
                    onChange={handleChange}
                    placeholder="Search for invoices..."
                    className="font-semibold border-l-0 border border-gray-200 rounded-r-xl px-7 h-full bg-white placeholder:text-sm placeholder:text-gray-400 text-xl focus:outline-none active:outline-none w-full"
                />
            </label>
        </>
    )
}