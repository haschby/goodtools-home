"use client";

import { useState } from "react";

interface RegisterProps {
    onChange: (item:string) => void;
    onBlur?: (e: React.FocusEvent<HTMLSelectElement>) => void;
    name: string;
    value: string;
    ref?: React.RefObject<HTMLSelectElement>;
    className: string;
}

interface SelectProps {
    isEditable?: boolean;
    label: string;
    options: { label: string, value: string }[];
    register: RegisterProps;
    name: string;
}

const Select = ({
    isEditable = false,
    label,
    options,
    register,
    name,
}: SelectProps) => {
    const [isOpen, setIsOpen] = useState(false);
    return (
    <>
        <label className="text-sm py-2" htmlFor={name}>
            <span className="w-full font-semibold">{label}</span>
        </label>
        <input
            onFocus={() => setIsOpen(true)}
            onBlur={() => setIsOpen(false)}
            onChange={() => {}}
            type="text"
            name={name}
            className={register.className}
            value={register.value}
            disabled={!isEditable}
        />
        {
            (isOpen) && (
            <ul className="border border-gray-300 bg-white shadow-lg absolute top-[calc(100%+10px)] rounded-md left-0 w-full max-h-[200px] overflow-y-auto z-[9999]"
                id={name}
            >
                {
                    options && options.length > 0 && options.map(
                        (item: { label: string, value: string }, index: number) => {
                            const isLast = index === options.length - 1;
                            return (
                                <li key={index}
                                    onMouseDown={() => register.onChange(item.value)}
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
};

export { Select };