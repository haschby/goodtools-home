"use client";

import Link from 'next/link';
import Icon from '@/components/atoms/Icon';
import { DollarSolid, PlaySolid } from '@lineiconshq/free-icons';
import { usePathname } from 'next/navigation';

export default function MainSideBar() {

    const pathname = usePathname();

    const cssActive = "bg-green-300/20 text-green-500 font-bold";

    return (
    <div className="relative z-[999999] flex flex-col border-r border-gray-200 h-full items-start max-w-[150px] w-full">
        <h1 className="py-8 flex flex-row justify-center w-full text-black font-bold items-center text-xl">
            {/* <LogoGoodTools /> OODTOOLS */}
            Runwa
            <span className="transform -rotate-35 rounded-full ml-1 relative h-4 w-[4px] flex bg-green-300 -left-.5 -top-1">
            </span>
            <span className="transform rotate-20 rounded-full mr-1 relative h-8 w-[4px] flex bg-green-300">
            </span>
            {/* <span className="rounded-full mr-2 ml-[0px] relative h-9 w-[4px] flex bg-green-300 -top-1.5">
                <pre className="absolute top-0 left-0 w-4 h-[4px] flex bg-green-300 rounded-full">
                </pre>
                <pre className="absolute top-1.5 left-0 w-3 h-[4px] flex bg-green-300 rounded-full">
                </pre>
            </span> */}
            {/* <pre className="rounded-full ml-[2px] mr-1 relative top-1 h-4 w-[4px] flex bg-green-400"></pre> */}
        </h1>
        <nav className="w-full text-sm mt-5">
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