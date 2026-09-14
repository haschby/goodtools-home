"use client";

import { useState } from "react";
import Icon from "@/components/atoms/Icon";
import { Cloud2Stroke } from "@lineiconshq/free-icons";
import { BuybackImportModal } from "./importmodal";
import { useDataTable } from "@/lib/contexts/DataTableCustomContext";
import { Buyback } from "@/lib/types/buyback";


export function BuybackImport() {
    const [isOpen, setIsOpen] = useState(false);
    const { refreshTableData } = useDataTable<Buyback>();
    return (
        <>
            <button
                className="group hover:bg-purple-600 bg-purple-500 text-white group cursor-pointer py-2 px-4 rounded-md border border-purple-800"
                onClick={() => setIsOpen(true)}>
                <span className="text-xs flex items-center gap-2 font-semibold">
                    <Icon
                        Icon={Cloud2Stroke}
                        size={16}
                        strokeWidth={3}
                        className="" />
                    Bordereaux de rachats
                </span>
            </button>

            {isOpen && (
                <BuybackImportModal
                    onClose={() => setIsOpen(false)}
                    refreshTable={refreshTableData}
                />
            )}
        </>
    );
}
