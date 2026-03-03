"use server";

import { Suspense } from "react";
import { Invoice } from "@/lib/types/invoice";
import { DataListProvider } from "@/components/providers/DataListProvider";
import { QueryClientProvider } from "@/components/providers/QueryClientProvider";
import { getTotalRecordsByEntity } from "@/actions/common";
import { getInvoiceById, getInvoices } from "@/actions/invoice.actions";
import { configTable } from "@/components/views/dashboard/invoices/config/config.table";

import InvoicePage from "@/components/views/dashboard/invoices/InvoicePage";

export default async function InvoicesPage() {
    return (
        <QueryClientProvider entity="invoice">
            <Suspense fallback={<div>Loading...</div>}>
                <DataListProvider<Invoice>
                    fetchTotalRowsFunction={getTotalRecordsByEntity}
                    statuses={configTable.statuses}
                    fetchFunction={getInvoices}
                    columns={configTable.columns}
                    entity="invoice"
                    getRecordById={getInvoiceById}
                >
                    <InvoicePage />
                </DataListProvider>
            </Suspense>
        </QueryClientProvider>
    )
}