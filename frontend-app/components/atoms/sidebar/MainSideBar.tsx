"use client";
import { LogoGoodTools } from '@/components/atoms/LogoGoodTools';
import Link from 'next/link';
import Icon from '@/components/atoms/Icon';
import { Cart1Solid } from '@lineiconshq/free-icons';
import { usePathname } from 'next/navigation';

export default function MainSideBar() {

    const pathname = usePathname();

    const cssActive = "bg-white text-gray-900 !border-gray-200 hover:!text-gray-900";

    return (
    <div className="flex flex-col border-r bg-[#f9f8f0] border-gray-200 h-full items-start max-w-[150px] w-full">
        <h1 className="py-8 flex flex-row justify-center w-full gap-1 text-gray-700 text-lg font-bold">
            <LogoGoodTools /> OODTOOLS
        </h1>
        <nav className="w-full text-sm">
            <ul className="flex flex-col gap-2 text-gray-700">
                <li className="mx-auto w-full px-2">
                    <Link
                        href="/invoices"
                        className={`${pathname === '/invoices' && cssActive } hover:text-gray-500 transition-all duration-300 border border-transparent rounded-md w-full cursor-pointer p-3 flex items-center`}>
                        <Icon
                            Icon={Cart1Solid}
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
                        className={`${pathname.includes('/workflows') && cssActive} hover:text-gray-500 transition-all duration-300 border border-transparent rounded-md w-full cursor-pointer p-3 flex items-center`}>
                        <Icon
                            Icon={Cart1Solid}
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