"use client";

import TitleInfo from "@/components/atoms/view/TitleInfo";
import BuybackListView from "./BuybackListView";
import { BuybackImport } from "./components/listview/import";

export default function BuybackPage() {

    const buttonActions = [ BuybackImport ];

    return (
        <div className="px-6">
            <div className="w-full flex flex-col items-center justify-between text-gray-700 gap-4">

                <TitleInfo
                    title="Buyback"
                    baseLineText="View detailed buyback by clicking on the row."
                    totalRows={0}
                    buttonActions={ buttonActions }
                />

                <BuybackListView />                
            </div>
        </div>
    )
}