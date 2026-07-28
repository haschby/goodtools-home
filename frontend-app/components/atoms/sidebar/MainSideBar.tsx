"use client";

import Icon from '@/components/atoms/Icon';
import { DollarCircleSolid, CloudIot2Solid, BeatStroke, Cart2Solid, Leaf1Solid  } from '@lineiconshq/free-icons';
import { SideBarItem } from './SideBarItem';

const routes = [
    {
        label: 'Invoices',
        href: '/invoices',
        icon: DollarCircleSolid
    },
    {
        label: 'buyback',
        href: '/buyback',
        icon: Cart2Solid
    },
    {
        label: 'Workflows',
        href: '/workflows',
        icon: CloudIot2Solid
    }
]

export default function MainSideBar() {

    return (
    <div className="relative z-[999999] flex flex-col border-r border-gray-200 h-full items-start max-w-[180px] w-full bg-gray-100">
        <h1 className="font-bold tracking-tight relative text-gray-700 py-6 pl-4 flex flex-row justify-start w-full text-black items-center text-2xl gap-1">
            {/* <LogoGoodTools /> OODTOOLS */}
            <Icon
                Icon={Leaf1Solid}
                size={22}
                strokeWidth={1.5}
                className="bg-gray-700 p-1 text-white rounded-lg relative left-0 top-0 inline-block" />
            Goodtools
        </h1>
        <nav className="w-full h-full text-sm mt-2">

            <ul className="flex flex-col text-gray-700">
                {routes.map(
                    (route, index) => (
                    <SideBarItem
                        key={index}
                        label={route.label}
                        href={route.href}
                        icon={route.icon} />
                ))}
            </ul>
        </nav>
    </div>
  );
}