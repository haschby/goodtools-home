"use server";

import { Suspense } from "react";
import { Invoice } from "@/lib/types/invoice";
import { DataListProvider } from "@/components/providers/DataListProvider";
import { QueryClientProvider } from "@/components/providers/QueryClientProvider";
import { getInvoiceById, getInvoices } from "@/actions/invoice.actions";
import { configHeaders } from "@/components/views/dashboard/invoices/config/config.headers";

import InvoicePage from "@/components/views/dashboard/invoices/InvoicePage";

export default async function InvoicesPage() {
    return (
        <QueryClientProvider entity="invoice">
            <Suspense fallback={<div>Loading...</div>}>
                <DataListProvider<Invoice>
                    statuses={configHeaders.statuses}
                    fetchFunction={getInvoices}
                    columns={configHeaders.columns}
                    getRecordById={getInvoiceById}
                >
                    <InvoicePage />
                </DataListProvider>
            </Suspense>
        </QueryClientProvider>
    )
}