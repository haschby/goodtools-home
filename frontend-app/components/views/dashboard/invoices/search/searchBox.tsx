"use client";

import { useRef, useCallback } from "react";
import Icon from "@/components/atoms/Icon";
import { Database2Outlined } from "@lineiconshq/free-icons";
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
                className={`border-r border-white bg-white w-full text-md z-[99999] flex items-center`}>
                <span className="pl-7 py-4">
                    <Icon
                        Icon={Database2Outlined}
                        size={24}
                        strokeWidth={2}
                        className="text-green-500" />
                </span>
                <input
                    name="provider"
                    id="search-box"
                    type="search"
                    onChange={handleChange}
                    placeholder="Search for invoices"
                    className="text-gray-500 placeholder:text-sm text-xl focus:outline-none active:outline-none w-full border-none px-7 py-4"
                />
            </label>
        </>
    )
}