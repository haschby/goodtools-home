"use client";

import Icon from '@/components/atoms/Icon';
import { DollarCircleSolid, CloudIot2Solid, Cart2Solid, Leaf1Solid  } from '@lineiconshq/free-icons';
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
    <div className="relative z-[999999] flex flex-col border-r border-gray-200 h-full items-start max-w-[60px] xl:max-w-[130px] w-full bg-gray-100">
        <h1 className="p-3 flex w-full xl:p-4">
            {/* <LogoGoodTools /> OODTOOLS */}
            {/* <Icon
                Icon={Leaf1Solid}
                size={16}
                strokeWidth={1.5}
                className="text-gray-700 rounded-lg relative left-0 top-0 inline-block" /> */}
            <span className="xl:flex items-center justify-center m-auto hidden font-extrabold tracking-tight rounded-md bg-green-500 p-2">
                GoodTools
            </span>
            <span className="xl:hidden flex font-extrabold bg-green-500 text-white rounded-md p-2">
                GT
            </span>
        </h1>
        <nav className="w-full h-full text-sm mt-2">
            <ul className="flex flex-col text-gray-700 px-2">
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