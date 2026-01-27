"use client";

import InvoiceListView from '@/components/views/dashboard/invoices/InvoiceListView';
import ImportInvoiceForm from "./form/ImportInvoiceForm";

export default function InvoicePage() {
    return (
        <>
            <InvoiceListView />
            <ImportInvoiceForm />
        </>
    );
}