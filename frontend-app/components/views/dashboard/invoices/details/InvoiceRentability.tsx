"use client";
import Icon from "@/components/atoms/Icon";
import { ArrowAngularTopRightSolid, Spinner3Solid } from "@lineiconshq/free-icons";

const formatCurrency = (value: number) =>
    new Intl.NumberFormat("fr-FR", {
        style: "currency",
        currency: "EUR",
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    }).format(value);

function InfoIcon() {
    return (
        <span className="flex h-3.5 w-3.5 items-center justify-center rounded-full bg-gray-300 text-[9px] font-bold text-white">
            i
        </span>
    );
}

function SubMetric({
    label,
    value,
    format = "currency",
}: {
    label: string;
    value: number;
    format?: "currency" | "percent";
}) {
    const isNegative = value < 0;
    const valueClass = isNegative ? "text-red-500" : "text-green-500";
    const displayValue =
        format === "percent" ? `${value.toFixed(0)}%` : formatCurrency(value);

    return (
        <div className="flex flex-col gap-1">
            <div className="flex items-center gap-1.5 text-sm text-gray-800">
                <span>{label}</span>
                <InfoIcon />
            </div>
            <span className={`text-lg font-semibold ${valueClass}`}>
                {displayValue}
            </span>
        </div>
    );
}

interface InvoiceRentabilityProps {
    profit?: number;
    ca?: number;
    charges?: number;
    margin?: number;
}

export default function InvoiceRentability({
    profit = 0,
    ca = 0,
    charges = 0,
    margin = 0,
}: InvoiceRentabilityProps) {

    const isTotalNegative = ca < 0;
    const isMargingNegative = margin < 0;

    return (
        <div className="flex w-full flex-col gap-2">
            <div className="flex flex-row gap-2">
                <div className="w-full flex flex-col gap-1 bg-white border border-gray-200 rounded-2xl px-3 py-2">
                    <span className="text-xl font-medium font-semibold">Total</span>
                    <div className="flex items-start gap-1">
                        <span className="text-right text-3xl font-normal tracking-tight">
                            { 
                                ca === 0
                                ? <Icon Icon={Spinner3Solid}
                                size={24}
                                className="animate-spin duration-300 text-gray-600" />
                                : formatCurrency(ca)
                            }
                        </span>
                        { ca !== 0 && (
                            <Icon
                                Icon={ArrowAngularTopRightSolid}
                                size={16}
                                className={`mt-1 ${isTotalNegative ? "text-red-500 rotate-90" : "text-green-500"}`} />
                        )}
                    </div>
                </div>
                <div className="w-full flex flex-col gap-1 bg-white border border-gray-200 rounded-2xl px-3 py-2">
                    <span className="text-xl font-medium text-gray-800 font-semibold">Marge</span>
                    <div className="flex items-start gap-1">
                        <span className="text-3xl font-normal">
                            { 
                                margin === 0
                                ? <Icon Icon={Spinner3Solid}
                                    size={24}
                                    className="animate-spin duration-300 text-gray-600" />
                                : margin.toFixed(2) + " %"
                            }
                        </span>
                        { margin !== 0 && (
                        <Icon
                            Icon={ArrowAngularTopRightSolid}
                            size={16}
                            className={`mt-1 ${isMargingNegative ? "text-red-500 rotate-90" : "text-green-500"}`} />
                        )}
                    </div>
                </div>
            </div>
            {/* <div className="text-xs text-gray-600 italic px-3">
                La rentabilité de cette facture s&apos;élève à 
                <span className="font-semibold"> {margin.toFixed(2)}%</span> de marge,
                avec un total de
                <span className="font-semibold"> {formatCurrency(ca)} </span> de chiffre d&apos;affaires
                et <span className="font-semibold">{formatCurrency(charges)}</span> de charges, pour un profit net de
                <span className="font-semibold"> {formatCurrency(profit)}</span>.
            </div> */}
        </div>
    );
}
