"use client";

import { ReactNode, useState } from "react";

export interface TabItem {
    key: string;
    label: string;
    content: ReactNode;
}

interface TabsProps {
    tabs: TabItem[];
    defaultTabKey?: string;
    className?: string;
    onTabChange?: (key: string) => void;
}

export default function Tabs(
    { tabs, defaultTabKey, className = "", onTabChange }: TabsProps
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
                className="flex flex-row items-center gap-1 border-b border-slate-200 bg-slate-50 px-3">
                {
                    tabs.map((tab) => {
                        const isActive = tab.key === activeTab?.key;
                        return (
                            <button
                                key={tab.key}
                                type="button"
                                role="tab"
                                aria-selected={isActive}
                                onClick={() => handleTabChange(tab.key)}
                                className={`cursor-pointer text-sm font-semibold px-4 py-3 -mb-px border-b-2 transition-colors ${
                                    isActive
                                        ? 'border-gray-800 text-gray-800'
                                        : 'border-transparent text-gray-400 hover:text-gray-600'
                                }`}>
                                {tab.label}
                            </button>
                        );
                    })
                }
            </nav>

            <div role="tabpanel" className="flex flex-col h-full">
                {activeTab?.content}
            </div>
        </div>
    );
}
