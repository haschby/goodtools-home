"use client";

import { ReactNode } from "react";
import { EnumInvoiceStatus } from "@/lib/types/invoice";

interface StatusRowProps {
    status: string;
    className?: string;
}

const StatusRow = ({ status, className } :StatusRowProps ): ReactNode => {
    const cssClasses = `self-start rounded-full font-semibold ${className}`;
    switch (status) {
        case 'Skipped':
        case EnumInvoiceStatus.TO_BE_TRAITED:
            return <span className={`${cssClasses} bg-purple-400/10 text-purple-800/80 border border-purple-200`}>
                {status}
            </span>
        case EnumInvoiceStatus.NEED_TO_CHECK:
            return <span className={`${cssClasses} bg-emerald-400/10 text-emerald-800/80 border border-emerald-200`}>
                {status}
            </span>
        case 'Processing':
        case EnumInvoiceStatus.TO_BE_INVOICED:
            return <span className={`${cssClasses} bg-indigo-400/10 text-indigo-800/80 border border-indigo-200`}>
                {status}
            </span>
        case 'Pending':
        case EnumInvoiceStatus.INVOICED:
            return <span className={`${cssClasses} bg-amber-400/10 text-amber-800/80 border border-amber-200`}>
                {status}
            </span>
        case 'Completed':
        case EnumInvoiceStatus.VALIDATED:
            return <span className={`${cssClasses} bg-lime-400/10 text-lime-800/80 border border-lime-200`}>
                {status}
            </span>
        case EnumInvoiceStatus.TBD:
        default:
            return <span className={`${cssClasses} bg-red-400/10 text-red-800/80 border border-red-200`}>
                {status ?? 'N/A'}
            </span>
    }
}

export { StatusRow };