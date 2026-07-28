"use client";

import { useCallback, useRef, useState, useMemo } from "react";

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
    label?: string;
    options: { label: string, value: string }[];
    register: RegisterProps;
    name: string;
    icon?: {
        position: 'left' | 'right';
        icon: React.ReactNode;
    } | null;
}

const Select = ({
    isEditable = false,
    label,
    options,
    register,
    name,
    icon = null
}: SelectProps) => {
    const [isOpen, setIsOpen] = useState(false);
    const containerRef = useRef<HTMLDivElement>(null);
    const [dropdownPosition, setDropdownPosition] = useState<'top' | 'bottom'>('bottom');

    const handleFocus = useCallback(
        () => {
        if (containerRef.current) {
            const { bottom } = containerRef.current.getBoundingClientRect();
            const spaceBelow = window.innerHeight - bottom;
            console.log(spaceBelow < 220 ? 'top' : 'bottom');
            // ✅ Si moins de 220px en bas, ouvre en haut
            setDropdownPosition(spaceBelow < 220 ? 'top' : 'bottom');
        }
        setIsOpen(true);
    },[])

    const labelOrIcon = useMemo(() => {
        const isPosition = Boolean(icon?.position);
        return (
            <label
                htmlFor={`${name}`}
                className={` ${isPosition ? 'mb-3' : undefined } text-sm py-2 flex flex-row items-center gap-2`}>
                { icon && 
                    <span className="px-2">
                        { icon?.icon && icon.icon }
                    </span>
                }
                { label && <span className="w-full font-semibold">{label}</span> }
            </label>
        );
    }, [icon, label, name]);

    return (
    <>
        {labelOrIcon}
        <div ref={containerRef} className="relative mb-3"> 
            <input
                id={name}
                onFocus={handleFocus}
                onBlur={() => setIsOpen(false)}
                onChange={() => {}}
                type="text"
                name={name}
                className={`cursor-pointer ${register.className}`}
                value={register.value}
                disabled={!isEditable}
            />
            {
                (isOpen) && (
                <ul className={`border border-gray-300 bg-white shadow-lg absolute ${dropdownPosition === 'top' ? 'bottom-[calc(100%+10px)]' : 'top-[calc(100%+10px)]'} rounded-md left-0 w-full max-h-[80px] overflow-y-auto z-[99999]`}
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
        </div>
    </>
    )
};

export { Select };