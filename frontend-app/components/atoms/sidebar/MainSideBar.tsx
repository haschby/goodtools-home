"use client";

import Link from 'next/link';
import Icon from '@/components/atoms/Icon';
import { DollarSolid, PlaySolid, BeatStroke } from '@lineiconshq/free-icons';
import { usePathname } from 'next/navigation';

export default function MainSideBar() {

    const pathname = usePathname();

    const cssActive = "bg-green-300/20 text-green-500 font-bold";

    return (
    <div className="relative z-[999999] flex flex-col border-r border-gray-200 h-full items-start max-w-[150px] w-full">
        <h1 className="relative text-green-500 py-5 flex flex-row justify-center w-full text-black font-bold items-center text-lg">
            {/* <LogoGoodTools /> OODTOOLS */}
            
            Goodtools
            <Icon Icon={BeatStroke} size={24} strokeWidth={2} className="relative -left-1 -top-1 text-green-500 inline-block" />
            
        </h1>
        <nav className="w-full h-full text-sm pt-4">
            <ul className="flex flex-col gap-2 text-gray-300">
                <li className="mx-auto w-full px-2">
                    <Link
                        href="/invoices"
                        className={`${pathname === '/invoices' && cssActive } group transition-all duration-300 border border-transparent rounded-md w-full cursor-pointer px-3 py-2 flex items-center`}>
                        <Icon
                            Icon={DollarSolid}
                            size={14}
                            strokeWidth={2}
                            className="inline-block mr-2"
                        />
                        Invoices
                    </Link>
                </li>
                <li className="mx-auto w-full px-2">
                    <Link
                        href="/workflows"
                        className={`${pathname.includes('/workflows') && cssActive} transition-all duration-300 border border-transparent rounded-md w-full cursor-pointer px-3 py-2 flex items-center`}>
                        <Icon
                            Icon={PlaySolid}
                            size={14}
                            strokeWidth={2}
                            className="inline-block mr-2"
                        />
                        Workflows
                    </Link>
                </li>
            </ul>
        </nav>
    </div>
  );
}