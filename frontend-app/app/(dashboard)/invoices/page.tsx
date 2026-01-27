"use server";

import { Suspense } from "react";
import { Invoice } from "@/lib/types/invoice";
import InvoicePage from "@/components/views/dashboard/invoices/InvoicePage";
import { DashBoardPageLayout } from "@/components/layouts/dashboard/Layout"
import { DataListProvider } from "@/components/providers/DataListProvider";
import { getTotalRecordsByEntity } from "@/actions/common";
import { getInvoices } from "@/actions/invoices";
import { configTable } from "@/components/views/dashboard/invoices/config/config.table";


export default async function InvoicesPage() {

    return (
        <Suspense fallback={<div>Loading...</div>}>
            <DataListProvider<Invoice>
                fetchTotalRowsFunction={getTotalRecordsByEntity}
                statuses={configTable.statuses}
                fetchFunction={getInvoices}
                columns={configTable.columns}
                entity="invoice"
            >
                <DashBoardPageLayout
                    title="Invoices">
                    
                        <InvoicePage />
                </DashBoardPageLayout>
            </DataListProvider>
        </Suspense>
    )
}