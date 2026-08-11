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
    const cssClasses = `rounded-xl font-semibold ${className} flex items-center gap-1`;
    switch (status) {
        case EnumInvoiceStatus.TBD:
        case 'archived':
            return <span className={`${cssClasses} bg-gray-300/60 text-gray-500 text-xs`}>
                <Icon Icon={Ticket1Solid} size={12} strokeWidth={2} />
                {status}
            </span>
        case 'Failed':
            return <span className={`${cssClasses} bg-orange-300/60 text-orange-500 text-xs`}>
                <Icon Icon={Ticket1Solid} size={12} strokeWidth={2} />
                {status}
            </span>
        case EnumInvoiceStatus.TO_BE_TRAITED:
        case 'Pending':
            return <span className={`${cssClasses} bg-purple-300/60 text-purple-500 text-xs`}>
                <Icon Icon={Ticket1Solid} size={12} strokeWidth={2} />
                {status}

            </span>
        case 'Skipped':
        case 'Aborted':
            return <span className={`${cssClasses} bg-purple-300/60 text-purple-500 text-xs`}>
                <Icon Icon={Ticket1Solid} size={12} strokeWidth={2} />
                {status}

            </span>
        case EnumInvoiceStatus.NEED_TO_CHECK:
            return <span className={`${cssClasses} bg-fuchsia-300/60 text-fuchsia-500 text-xs`}>
                <Icon Icon={Ticket1Solid} size={12} strokeWidth={2} />
                {status}
            </span>
        case 'Processing':
        case EnumInvoiceStatus.TO_BE_INVOICED:
            return <span className={`${cssClasses} bg-orange-500/60 text-orange-700 text-xs`}>
                <Icon Icon={Ticket1Solid} size={12} strokeWidth={2} />
                {status}
            </span>
        case EnumInvoiceStatus.INVOICED:
            return <span className={`${cssClasses} bg-blue-500/60 text-blue-700 text-xs`}>
                <Icon Icon={Ticket1Solid} size={12} strokeWidth={2} />
                {status}
            </span>
        case 'Completed':
        case EnumInvoiceStatus.VALIDATED:
        case EnumInvoiceStatus.VALIDATED_ONLY:
            return <span className={`${cssClasses} bg-green-500/60 text-green-700 text-xs`}>
                <Icon Icon={Ticket1Solid} size={12} strokeWidth={2} />
                {status}
            </span>
        case EnumInvoiceStatus.TBD:
        default:
            return <span className={`${cssClasses} bg-black text-white text-xs`}>
                <Icon Icon={Ticket1Solid} size={12} strokeWidth={2} />
                {status ?? 'N/A'}
            </span>
    }
}

export { StatusRow };