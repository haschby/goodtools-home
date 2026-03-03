"use client";

import { useState, useEffect, useRef } from "react";
import { useAsyncSearchQuery } from "@/lib/hooks/useAsyncSearchQuery";
import Icon from "../Icon";
import { Spinner2SacleBulk } from "@lineiconshq/free-icons";
import { BaseResponse } from "@/lib/types/base";
import { SearchQueryMockData } from "@/mockData/common";

interface SearchQueryFunctionProps {
    entity: string;
    query: string;
}

interface AsyncSelectFieldProps<T> {
    renderInput: (
        props: React.InputHTMLAttributes<HTMLInputElement>,
        ref: React.RefObject<HTMLInputElement | null>
    ) => React.ReactNode;
    defaultValue?: string;
    searchQueryFunction: (props: SearchQueryFunctionProps) => Promise<BaseResponse<T[]>>;
    entity: string;
    onSelectedValue: (value: string) => void;
}

export function AsyncSelectField<T extends { name: string; label: string }>(
    { onSelectedValue, defaultValue = "", searchQueryFunction, entity, renderInput }: AsyncSelectFieldProps<T>
) {
    const [inputValue, setInputValue] = useState<string>(defaultValue);
    const [query, setQuery] = useState<string>("");
    const [debouncedQuery, setDebouncedQuery] = useState<string>("");
    const [isFocused, setIsFocused] = useState(false);

    const searchInputQueryRef = useRef<HTMLInputElement>(null);

    const { isLoading, data, setIsLoading } = useAsyncSearchQuery({
        query: debouncedQuery,
        entity,
        searchQueryFunction,
    });

    useEffect(() => {
        if (!query) {
            return;
        }

        const timeout = setTimeout(() => setDebouncedQuery(query), 500);
        return () => clearTimeout(timeout);
    }, [query]);

    function handleSelectItem(item: string) {
        setInputValue(item);
        setQuery(item);
        onSelectedValue(item);
        setIsFocused(false);
    }

    const inputProps: React.InputHTMLAttributes<HTMLInputElement> = {
        value: inputValue,
        onChange: (e) => {
            const value = e.target.value;
            setInputValue(value);
            setQuery(value);

            if (!value) {
                setIsLoading(false);
            }
        },
        onFocus: () => setIsFocused(true),
        onBlur: () => setIsFocused(false),
    };

    const shouldShowDropdown =
        isFocused &&
        inputValue.length > 0 &&
        (isLoading || (data && data.length > 0));

    return (
        <>
            <input type="hidden" value={defaultValue} />
            {renderInput(inputProps, searchInputQueryRef)}

            {shouldShowDropdown && (
                <ul className="border border-gray-300 bg-white shadow-lg absolute top-[calc(100%+10px)] rounded-md left-0 w-full max-h-[200px] overflow-y-auto z-[9999]">
                    {isLoading && (
                        <li className="flex items-center justify-center p-2 min-h-[200px]">
                            <Icon
                                Icon={Spinner2SacleBulk}
                                size={20}
                                strokeWidth={2}
                                className="text-gray-800 animate-spin"
                            />
                        </li>
                    )}
                    {!isLoading && data && data.length > 0 &&
                    data.map(
                        (item: SearchQueryMockData, index: number) => {
                        const isLast = index === data.length - 1;
                        return (
                            <li
                                key={index}
                                onMouseDown={() => handleSelectItem(item.name)}
                                className={`${isLast ? "" : "border-b border-gray-200"} text-sm p-2 hover:bg-green-300/60 hover:text-green-700 cursor-pointer`}
                            >
                                {item.label}
                            </li>
                        );
                    })}
                    {!isLoading && (!data || data.length === 0) && (
                        <li className="p-2 text-sm text-gray-500">Aucun résultat</li>
                    )}
                </ul>
            )}
        </>
    );
}