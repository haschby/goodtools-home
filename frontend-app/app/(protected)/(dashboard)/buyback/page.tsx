"use server";

import { QueryClientProvider } from "@/components/providers/QueryClientProvider";
import { Suspense } from "react";
import { DataListProvider } from "@/components/providers/DataListProvider";
import { configHeaders } from "@/components/views/dashboard/buyback/config/headers.config";
import { Buyback } from '@/lib/types/buyback';
import { getBuybacks, getBuybackById } from "@/actions/buyback.action";

import BuybackPage from "@/components/views/dashboard/buyback/BuybackPage";

export default async function BuybackPageComponent() {

    return (
        <QueryClientProvider entity="buyback">
            <Suspense fallback={<div>Loading...</div>}>
                <DataListProvider<Buyback>
                    statuses={configHeaders.statuses}
                    fetchFunction={getBuybacks}
                    columns={configHeaders.columns}
                    getRecordById={getBuybackById}
                >
                    <BuybackPage />
                </DataListProvider>
            </Suspense>
        </QueryClientProvider>
    )
}