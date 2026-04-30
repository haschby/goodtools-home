"use client";

import Link from "next/link";
import Icon from "../Icon";
import { usePathname } from "next/navigation";
import { IconData  } from "../Icon";
import { ComponentType, SVGProps } from "react";

interface SideBarItemProps {
    label: string;
    href: string;
    icon: ComponentType<SVGProps<SVGSVGElement>> & IconData
}

export function SideBarItem({ label, href, icon }: SideBarItemProps) {
    const pathname = usePathname();
    const isActive = pathname === href;
    const cssActive = "bg-gray-300/20 text-gray-800";

    return (
        <li className="mx-auto w-full px-2 text-sm">
            <Link
                href={href}
                className={`${ isActive && cssActive } transition-all duration-300 border border-transparent rounded-md w-full cursor-pointer px-2 py-2 flex items-center`}>
                <Icon
                    Icon={icon}
                    size={24}
                    strokeWidth={2}
                    className={`transition-all duration-300 p-0.5 inline-block mr-2`} />
                {label}
            </Link>
        </li>
    )
}