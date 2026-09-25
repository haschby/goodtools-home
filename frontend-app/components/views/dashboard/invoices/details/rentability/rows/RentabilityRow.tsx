"use client";

import { useMemo } from "react";
import { Rentability } from "@/actions/invoice.actions";
import { StatusRow } from "@/components/atoms/listview/RowItems/StatusRow";
import Link from "next/link";

const formatCurrency = (value: number) =>
    new Intl.NumberFormat("fr-FR", {
        style: "currency",
        currency: "EUR",
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    }).format(value);

interface RentabilityRowProps {
    bookingId: string;
    rentability: Rentability;
}


const TypeRow = ({ type, bookingId }: { type: string, bookingId: string }) => {
    switch (type) {
        case "provider":
            return <span className="self-start bg-gray-100 border border-gray-200 text-xs text-gray-700 px-2 py-1 rounded-full">
                Fournisseur
            </span>;
        case "buyback":
            return <span className="self-start bg-gray-100 border border-gray-200 text-xs text-gray-700 px-2 py-1 rounded-full">Rachat</span>;
        case "ProviderPrice":
            return <span className="self-start bg-gray-100 border border-gray-200 text-xs text-gray-700 px-2 py-1 rounded-full">Provider</span>;
        case "GoodcollectPrice":
            return <Link href={`https://goodcollect.co/admin/bookings/${bookingId}/rentability`}
            className="self-start bg-green-400 border text-xs text-white px-2 py-1 rounded-full">Goodcollect</Link>;
        default:
            return <span className="self-start bg-gray-300 text-xs text-white px-2 py-1 rounded-full">Unknown</span>;
    }
}

export default function RentabilityRow({ bookingId, rentability }: RentabilityRowProps) {

    const priceHT = rentability?.totalPriceHT || 0;

    const priceToDisplay = useMemo(() => {
        if (rentability.type === "GoodcollectPrice") {
            return rentability.totalPriceHT;
        }

        const isNegative = priceHT > 0;
        const priceToDisplay = isNegative ? -priceHT : priceHT;

        return priceToDisplay;
    }, [priceHT, rentability.type, rentability.totalPriceHT]);

    return (
        <div className="flex items-center justify-between gap-3 bg-gray-50 border border-t-0 border-l-0 border-r-0 border-gray-200 text-sm shadow-xs p-2">
            <div className="flex flex-row leading-tight gap-2 items-center">
                <TypeRow type={rentability.type || ""} bookingId={bookingId} />
                <StatusRow className="self-start" status={rentability?.status || ""} />
            </div>

            <span
                className={`font-semibold text-gray-700`}
            >
                {formatCurrency(priceToDisplay || 0)}
            </span>
        </div>
    );
    
}
