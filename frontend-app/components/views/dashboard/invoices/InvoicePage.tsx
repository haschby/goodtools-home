"use client";

import InvoiceListView from '@/components/views/dashboard/invoices/InvoiceListView';
import ImportInvoiceForm from "./form/ImportInvoiceForm";
// import { useSearchParams } from 'next/navigation';
// import { useEffect } from 'react';
// import { getInvoices } from '@/actions/invoice.actions';

export default function InvoicePage() {
    // const searchParams = useSearchParams();
    // const status = searchParams.get('status');

    // useEffect(() => {
    //     console.log('@STATUS', status);
    //     const fetchInvoices = async () => {
    //         const invoices = await getInvoices({
    //             label: status ?? 'All',
    //             options: {
    //                 cursor: '',
    //                 id: ''
    //             }
    //         });
    //         console.log('@INVOICES', invoices);
    //     };
    //     fetchInvoices();
    // }, [status]); 

    return (
        // <Suspense fallback={<div>Loading...</div>}>
        //     <SearchComponentProvider>
        <>
            <InvoiceListView />
            <ImportInvoiceForm />
        </>
        //     </SearchComponentProvider>
        // </Suspense>
    );
}