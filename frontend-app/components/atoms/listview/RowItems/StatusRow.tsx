"use client";

import { ReactNode } from "react";
import { EnumInvoiceStatus } from "@/lib/types/invoice";
import Icon from "@/components/atoms/Icon";
import { Flag1Solid as Ticket1Solid } from "@lineiconshq/free-icons";

interface StatusRowProps {
    status: string;
    className?: string;
}

const StatusRow = ({ status, className } :StatusRowProps ): ReactNode => {
    const cssClasses = `rounded-full font-semibold ${className} flex items-center gap-1`;
    switch (status) {
        case 'Skipped':
        case 'Aborted':
        case EnumInvoiceStatus.TO_BE_TRAITED:
            return <span className={`${cssClasses} bg-purple-300/20 text-purple-500 text-xs`}>
                <Icon Icon={Ticket1Solid} size={16} strokeWidth={2} />
                {status}

            </span>
        case EnumInvoiceStatus.NEED_TO_CHECK:
            return <span className={`${cssClasses} bg-fuchsia-300/20 text-fuchsia-500 text-xs`}>
                <Icon Icon={Ticket1Solid} size={16} strokeWidth={2} />
                {status}
            </span>
        case 'Processing':
        case EnumInvoiceStatus.TO_BE_INVOICED:
            return <span className={`${cssClasses} bg-indigo-300/20 text-indigo-500 text-xs`}>
                <Icon Icon={Ticket1Solid} size={16} strokeWidth={2} />
                {status}
            </span>
        case 'Pending':
        case EnumInvoiceStatus.INVOICED:
            return <span className={`${cssClasses} bg-amber-300/20 text-amber-500 text-xs`}>
                <Icon Icon={Ticket1Solid} size={16} strokeWidth={2} />
                {status}
            </span>
        case 'Completed':
        case EnumInvoiceStatus.VALIDATED:
            return <span className={`${cssClasses} bg-green-400/20 text-green-600 text-xs`}>
                <Icon Icon={Ticket1Solid} size={16} strokeWidth={2} />
                {status}
            </span>
        case EnumInvoiceStatus.TBD:
        default:
            return <span className={`${cssClasses} bg-amber-300/20 text-amber-500 text-xs`}>
                <Icon Icon={Ticket1Solid} size={16} strokeWidth={2} />
                {status ?? 'N/A'}
            </span>
    }
}

export { StatusRow };