"use client";

import { useState, useEffect, useRef } from "react";
import { useAsyncSearchQuery } from "@/lib/hooks/useAsyncSearchQuery";
import Icon from "../Icon";
import { Spinner2SacleBulk } from "@lineiconshq/free-icons";
import { BaseResponse } from "@/lib/types/base";

interface SearchQueryFunctionProps {
    entity: string;
    query: string;
}

interface AsyncSelectFieldProps<T> {
    renderInput: (
        props: React.InputHTMLAttributes<HTMLInputElement>,
        ref: React.RefObject<HTMLInputElement | null>
    ) => React.ReactNode;

    defaultValue: string;

    searchQueryFunction: (props: SearchQueryFunctionProps) => Promise<BaseResponse<T[]>>;
    entity: string;
}


export function AsyncSelectField<T extends { name: string; label: string }>(
    { defaultValue, searchQueryFunction, entity, renderInput }: AsyncSelectFieldProps<T>
) {


    const [query, setQuery] = useState<string | null>(null);
    const [debouncedQuery, setDebouncedQuery] = useState<string | null>(null)
    const [isOpen, setIsOpen] = useState<boolean>(false);
    const searchInputQueryRef = useRef<HTMLInputElement>(null);
    const inputValue = query ?? defaultValue;

    const { isLoading, data, setIsLoading, setData } = useAsyncSearchQuery<T>({
        query: debouncedQuery,
        entity: entity,
        searchQueryFunction: searchQueryFunction
    });


    function handleSelectItem(item: string) {
        setQuery(item);
        setIsOpen(false);
    }

    useEffect(() => {

        if (!isOpen || !query || query === defaultValue) {
            return;
        };

        const timeOutDebounce = setTimeout(() => {
            setDebouncedQuery(query);
        }, 500);

        return () => {
            clearTimeout(timeOutDebounce);
        }
    }, [query, isOpen, defaultValue, setIsLoading]);

    const inputProps: React.InputHTMLAttributes<HTMLInputElement> = {
        value: inputValue,
        onChange: (e) => {
            setIsOpen(true);
            const value = e.target.value;
            setData([]);
            if (value === '') {
                setIsLoading(false);
                setQuery(defaultValue);
                setIsOpen(false);
                return;
            }
            setIsLoading(true);
            setQuery(value);
        },
        onBlur: () => {
            setIsOpen(false);
        }
    };

    return (
        <>
            <input type="hidden" defaultValue={defaultValue} />
            { renderInput(inputProps, searchInputQueryRef) }

            {
                ( isOpen ) && (
                    <ul className="border border-gray-300 bg-white shadow-lg absolute top-[calc(100%+10px)] rounded-md left-0 w-full max-h-[200px] overflow-y-auto z-[9999]">
                        {
                            isLoading &&
                            <li className="flex items-center justify-center p-2 min-h-[200px]">
                                <Icon
                                    Icon={Spinner2SacleBulk}
                                    size={20}
                                    strokeWidth={2}
                                    className="text-gray-800 animate-spin"
                                />
                            </li>
                        }
                        {
                            data && data.length > 0 && data.map(
                                (item: T, index: number) => {
                                const isLast = index === data.length - 1;
                                return (
                                    <li key={index}
                                        onMouseDown={() => handleSelectItem(item.name) }
                                        className={`${isLast ? '' : 'border-b border-gray-200'} text-sm p-2 hover:bg-green-300/60 hover:text-green-700 cursor-pointer`}>
                                        {item.label}
                                    </li>
                                )}
                            )
                        }
                    </ul>
                )
            }
        </>
    )
}