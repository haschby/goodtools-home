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
    const cssClasses = `px-3 py-1.5 rounded-full font-semibold ${className} flex items-center gap-1`;
    switch (status) {
        case EnumInvoiceStatus.TBD:
        case 'archived':
            return <span className={`${cssClasses} bg-gray-200 text-gray-500 text-xs`}>
                <Icon Icon={Ticket1Solid} size={12} strokeWidth={2} />
                <span className="hidden xl:inline">{status}</span>
            </span>
        case 'Failed':
            return <span className={`${cssClasses} bg-orange-200 text-orange-500 text-xs`}>
                <Icon Icon={Ticket1Solid} size={12} strokeWidth={2} />
                <span className="hidden xl:inline">{status}</span>
            </span>
        case EnumInvoiceStatus.TO_BE_TRAITED:
        case 'Pending':
            return <span className={`${cssClasses} bg-purple-200 text-purple-500 text-xs`}>
                <Icon Icon={Ticket1Solid} size={12} strokeWidth={2} />
                <span className="hidden xl:inline">{status}</span>

            </span>
        case 'Skipped':
        case 'Aborted':
            return <span className={`${cssClasses} bg-purple-200 text-purple-500 text-xs`}>
                <Icon Icon={Ticket1Solid} size={12} strokeWidth={2} />
                <span className="hidden xl:inline">{status}</span>

            </span>
        case EnumInvoiceStatus.NEED_TO_CHECK:
            return <span className={`${cssClasses} bg-fuchsia-200 text-fuchsia-500 text-xs`}>
                <Icon Icon={Ticket1Solid} size={12} strokeWidth={2} />
                <span className="hidden xl:inline">{status}</span>
            </span>
        case 'Processing':
        case EnumInvoiceStatus.TO_BE_INVOICED:
            return <span className={`${cssClasses} bg-orange-200 text-orange-500 text-xs`}>
                <Icon Icon={Ticket1Solid} size={12} strokeWidth={2} />
                <span className="hidden xl:inline">{status}</span>
            </span>
        case EnumInvoiceStatus.INVOICED:
            return <span className={`${cssClasses} bg-blue-200 text-blue-500 text-xs`}>
                <Icon Icon={Ticket1Solid} size={12} strokeWidth={2} />
                <span className="hidden xl:inline">{status}</span>
            </span>
        case 'Completed':
        case 'Valider':
        case EnumInvoiceStatus.VALIDATED:
        case EnumInvoiceStatus.VALIDATED_ONLY:
            return <span className={`${cssClasses} bg-green-200 text-green-500 text-xs`}>
                <Icon Icon={Ticket1Solid} size={12} strokeWidth={2} />
                <span className="hidden xl:inline">{status}</span>
            </span>
        case EnumInvoiceStatus.TBD:
        default:
            return <span className={`${cssClasses} bg-black text-white text-xs`}>
                <Icon Icon={Ticket1Solid} size={12} strokeWidth={2} />
                <span className="hidden xl:inline">{status ?? 'N/A'}</span>
            </span>
    }
}

export { StatusRow };