"use server";

import { QueryClientProvider } from "@/components/providers/QueryClientProvider";
import { Suspense } from "react";
import { DataListProvider } from "@/components/providers/DataListProvider";
import { configHeaders } from "@/components/views/dashboard/buyback/config/headers.config";
import { Invoice } from '@/lib/types/invoice';
import { getBuybacks, getBuybackById } from "@/actions/buyback.action";

import BuybackPage from "@/components/views/dashboard/buyback/BuybackPage";

export default async function BuybackPageComponent() {

    return (
        <div>Hello</div>
        // <QueryClientProvider entity="Invoice">
        //     <Suspense fallback={<div>Loading...</div>}>
        //         <DataListProvider<Invoice>
        //             statuses={configHeaders.statuses}
        //             fetchFunction={getInvoices}
        //             columns={configHeaders.columns}
        //             getRecordById={getBuybackById}
        //         >
        //             <BuybackPage />
        //         </DataListProvider>
        //     </Suspense>
        // </QueryClientProvider>
    )
}