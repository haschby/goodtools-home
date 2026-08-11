"use client";

import { Rentability } from "@/actions/invoice.actions";

const formatCurrency = (value: number) =>
    new Intl.NumberFormat("fr-FR", {
        style: "currency",
        currency: "EUR",
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    }).format(value);

interface RentabilityRowProps {
    rentability: Rentability;
}


const TypeRow = ({ type }: { type: string }) => {
    switch (type) {
        case "ProviderPrice":
            return <span className="self-start bg-green-400 text-xs text-green-700 p-1 rounded-md">Provider</span>;
        case "GoodcollectPrice":
            return <span className="self-start bg-blue-400 text-xs text-blue-700 p-1 rounded-md">Goodcollect</span>;
        default:
            return <span className="self-start bg-gray-300 text-xs text-white p-1 rounded-md">Unknown</span>;
    }
}

export default function RentabilityRow({ rentability }: RentabilityRowProps) {
    const priceHT = rentability?.priceHT || 0;
    const isNegative = priceHT < 0;

    return (
        <div className="flex items-center justify-between gap-3 rounded-lg bg-gray-50 px-3 py-2 text-sm">
            <div className="flex flex-col leading-tight gap-2">
                <TypeRow type={rentability.type || ""} />
            </div>

            <span
                className={`font-semibold ${isNegative ? "text-red-500" : "text-green-600"}`}
            >
                {formatCurrency(priceHT)}
            </span>
        </div>
    );
}
