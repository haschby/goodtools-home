"use client";

import { Invoice } from "@/lib/types/invoice";
import { StatusRow } from '@/components/atoms/listview/RowItems/StatusRow';
import { ColumnProps } from "@/lib/types/common";
import { CheckBoxfilter } from "@/components/atoms/form/items/CheckboxFilter";
import Link from "next/link";
import Icon from "@/components/atoms/Icon";
import { Paperclip1Solid } from "@lineiconshq/free-icons";
import { useRef, useState } from "react";

const ProviderCell = ({ item }: { item: Invoice }) => {
    const [isHovered, setIsHovered] = useState<boolean>(false);
    const [isTruncated, setIsTruncated] = useState<boolean>(false);
    const spanRef = useRef<HTMLSpanElement>(null);

    const handleMouseEnter = () => {
        const el = spanRef.current;
        if (el) setIsTruncated(el.scrollWidth > el.clientWidth);
        setIsHovered(true);
    };

    const showTooltip = isHovered && isTruncated;

    return (
        <span
        ref={spanRef}
        onMouseEnter={handleMouseEnter}
        onMouseLeave={() => setIsHovered(false)}
        className={`font-semibold text-gray-500 whitespace-nowrap ${showTooltip ? 'absolute z-10 w-max bg-white rounded-md px-2 py-1 shadow-lg' : 'truncate'}`}>
            {item.issuer_name}
        </span>
    );
};

export const invoicesColumns: ColumnProps<Invoice>[] = [
    {
        keyfield: '#',
        canSticky: true,
        align: 'left',
        // maxWidth: '200px',
        isFirst: true,
        renderItem: (item: Invoice) =>
            <p className="flex items-center justify-center gap-2 w-full">
            <CheckBoxfilter
                keyItems={item.gc_booking ? [item.id] : []}
                id={item.id} />
            </p>
    },
    // {
    //     keyfield: 'id',
    //     align: 'left',
    //     maxWidth: '0',
    //     renderItem: (item: Invoice) =>
    //         <span className="p-1 bg-gray-300/20 font-semibold text-gray-500 text-xs rounded-md">
    //             {item.id.substring(3)}
    //         </span>
    // },
    // {
    //     keyfield: 'external_id',
    //     align: 'left',
    //     maxWidth: '180px',
    //     isNumber: false,
    //     renderItem: (item: Invoice) =>
    //         <span className="text-sm font-normal text-gray-500">
    //             {item.external_id}
    //         </span>
    // },
    {
        keyfield: 'status',
        align: 'left',
        // maxWidth: '150px',
        isNumber: false,
        renderItem: (item: Invoice) =>
            <p className="flex items-center justify-center gap-2">
            <StatusRow className="px-2 py-1 rounded-md" status={item.status.toString()} />
            </p>
    },
    {
        keyfield: 'provider',
        align: 'left',
        // maxWidth: '400px',
        isNumber: false,
        renderItem: (item: Invoice) => <ProviderCell item={item} />
    },
    // {
    //     keyfield: 'last_modified',
    //     align: 'left',
    //     maxWidth: '150px',
    //     isNumber: false,
    //     renderItem: (item: Invoice) => {
    //         return (
    //             <span className="text-sm font-normal text-gray-500">
    //                 {new Date(item.updated_at).toLocaleDateString('fr-FR')}
    //             </span>
    //         )
    //     }
    // },
    {
        keyfield: 'booking_number',
        align: 'left',
        // maxWidth: '150px',
        isNumber: false,
        renderItem: (item: Invoice) => {
            return (
                <>
                {
                    item?.gc_booking && (
                        <Link
                            href={`https://goodcollect.com/booking/${item.gc_booking}`}
                            target="_blank"
                            className="relative z-900 flex items-center gap-2 text-sm font-normal text-orange-500">
                            <Icon
                                Icon={Paperclip1Solid}
                                size={16}
                                strokeWidth={2}
                                 />
                            <span className={`${item.gc_booking ? 'text-sm font-normal text-white bg-orange-500 w-auto h-4 flex items-center justify-center p-1 rounded-md' : 'text-sm font-normal text-gray-500'}`}>
                                {item.gc_booking}
                            </span>
                        </Link>
                    ) || (
                        <span className={`${item.gc_booking ? 'text-sm font-normal text-white bg-orange-500 w-auto h-4 flex items-center justify-center p-1 rounded-md' : 'text-sm font-normal text-gray-500'}`}>
                            {item.gc_booking}
                        </span>
                    )
                }
                </>
                // <span className="text-sm font-normal text-gray-500">
                //     {item.gc_booking}
                // </span>
            )
        }
            // <span className="text-sm font-normal text-gray-500">
            //     {item.gc_booking}
            // </span>
    },
    {
        keyfield: 'invoice_number',
        align: 'right',
        // maxWidth: '150px',
        isNumber: true,
        renderItem: (item: Invoice) =>
            <span className="text-sm font-normal text-gray-500">
                {item.invoice_number}
            </span>
    },
    // {
    //     keyfield: 'invoice_date',
    //     align: 'left',
    //     maxWidth: '150px',
    //     isNumber: false,
    //     renderItem: (item: Invoice) =>
    //         <span className="text-sm font-normal text-gray-500">
    //             {new Date(item.invoice_date).toLocaleDateString('fr-FR')}
    //         </span>
    // },
    {
        keyfield: 'amount_ht',
        align: 'right',
        // maxWidth: '150px',
        isNumber: true,
        renderItem: (item: Invoice) =>
            <span className="text-sm font-normal text-gray-500">
                {item.amount_ht}
            </span>
    },
    {
        keyfield: 'amount_ttc',
        align: 'right',
        // maxWidth: '150px',
        isNumber: true,
        renderItem: (item: Invoice) =>
            <span className="text-sm font-normal text-gray-500">
                {item.amount_ttc}
            </span>
    },
    {
        keyfield: 'amount_tva',
        align: 'right',
        maxWidth: '150px',
        isLast: true,
        isNumber: true,
        renderItem: (item: Invoice) =>
            <span className="text-sm font-normal text-gray-500">
                {item.amount_tva}
            </span>
    }
];