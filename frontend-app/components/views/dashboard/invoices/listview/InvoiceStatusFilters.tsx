"use client";

import InvoiceTypeFilter from './filters/InvoiceTypeFilter';
import InvoiceStatusFilter from './filters/InvoiceStatusFilter';

export default function InvoiceStatusFilters() {
    return (
        <div className="relative border-b border-gray-200 w-full px-6 py-3 flex flex-row items-center gap-3">
            <InvoiceTypeFilter />
            <InvoiceStatusFilter />
        </div>
    );
}
