"use client";

import { ComponentType, ReactNode, SVGProps, useState } from "react";
import Icon, { IconData } from "@/components/atoms/Icon";

export interface TabItem {
    key: string;
    label: string;
    content: ReactNode;
    icon?: ComponentType<SVGProps<SVGSVGElement>> & IconData;
}

interface TabsProps {
    tabs: TabItem[];
    defaultTabKey?: string;
    className?: string;
    navClassName?: string;
    stretch?: boolean;
    onTabChange?: (key: string) => void;
}

export default function Tabs(
    { tabs, defaultTabKey, className = "", navClassName = "", stretch = true, onTabChange }: TabsProps
) {
    const [ activeKey, setActiveKey ] = useState<string>(
        defaultTabKey || tabs[0]?.key
    );

    const activeTab = tabs.find((tab) => tab.key === activeKey) || tabs[0];

    const handleTabChange = (key: string) => {
        setActiveKey(key);
        onTabChange?.(key);
    };

    return (
        <div className={`flex flex-col ${className}`}>
            <nav
                role="tablist"
                className={`flex flex-row items-center gap-1 rounded-xl bg-gray-100 p-1 border border-gray-200 w-fit self-start ${navClassName} ${stretch ? 'w-full' : 'w-fit'}`}>
                {
                    tabs.map((tab, index) => {
                        const isActive = tab.key === activeTab?.key;
                        const previousActive = tabs[index - 1]?.key === activeTab?.key;
                        const showDivider = index > 0 && !isActive && !previousActive;
                        return (
                            <button
                                key={tab.key}
                                type="button"
                                role="tab"
                                aria-selected={isActive}
                                onClick={() => handleTabChange(tab.key)}
                                className={`relative cursor-pointer flex flex-row items-center justify-center gap-2 rounded-lg p-2 text-xs font-semibold transition-all duration-200 ${stretch ? 'flex-1' : 'flex-none'} ${
                                    isActive
                                        ? 'bg-white text-gray-900 shadow-sm border border-gray-200'
                                        : 'border border-transparent text-gray-400 hover:text-gray-600'
                                }`}>
                                {
                                    showDivider && (
                                        <span className="absolute left-0 top-1/2 h-4 w-px -translate-y-1/2 bg-gray-200" />
                                    )
                                }
                                {
                                    tab.icon && (
                                        <Icon
                                            Icon={tab.icon}
                                            size={16}
                                            strokeWidth={2}
                                            className={isActive ? 'text-gray-900' : 'text-gray-400'} />
                                    )
                                }
                                {tab.label}
                            </button>
                        );
                    })
                }
            </nav>

            <div role="tabpanel" className="flex flex-col h-full gap-4">
                {activeTab?.content}
            </div>
        </div>
    );
}
