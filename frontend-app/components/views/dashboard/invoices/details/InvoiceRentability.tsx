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

const formatPercent = (value: number) =>
    new Intl.NumberFormat("fr-FR", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    }).format(value) + " %";

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
    ca,
    charges,
    margin,
}: InvoiceRentabilityProps) {

    console.log(ca, charges, margin);

    const isTotalNegative = ca ? ca < 0 : false;
    const isMargingNegative = margin ? margin < 0 : false;

    // Barre proportionnelle : deux segments côte à côte (CA en vert, Charges en purple).
    // Chaque segment occupe un pourcentage de la barre en fonction de son montant
    // relatif au total (CA + Charges), afin que les deux couleurs soient toujours visibles.
    const total = (ca ?? 0) + (charges ?? 0);
    const caWidth = total > 0 ? ((ca ?? 0) / total) * 100 : 0;
    const chargesWidth = total > 0 ? ((charges ?? 0) / total) * 100 : 0;

    return (
        <div className="flex w-full flex-col gap-2 rounded-t-md bg-gray-100">
            <div className="flex flex-col text-black">
                <div className="flex flex-row">
                    <div className="w-full flex flex-col gap-1 justify-between border border-t-0 border-l-0 border-r-0 border-gray-200 px-3 py-2">
                        <span className="text-xs font-medium text-gray-500">Total CA</span>
                        <div className="flex items-start gap-1">
                            <span className="text-xl tracking-tight">
                                { 
                                    ca === 0
                                    ? <Icon Icon={Spinner3Solid}
                                    size={24}
                                    className="animate-spin duration-300 text-gray-600" />
                                    : formatCurrency(ca ?? 0)
                                }
                            </span>
                        </div>
                    </div>
                    <div className="w-full flex flex-col gap-1 justify-between border border-t-0 border-r-0 border-gray-200 px-3 py-2">
                        <span className="text-xs font-medium text-gray-500">Total Charges</span>
                        <div className="flex items-start gap-1">
                            <span className="text-xl font-normal tracking-tight">
                                { 
                                    charges === 0
                                    ? <Icon Icon={Spinner3Solid}
                                    size={24}
                                    className="animate-spin duration-300 text-gray-600" />
                                    : formatCurrency(charges ?? 0)
                                }
                            </span>
                        </div>
                    </div>
                </div>
                <div className="flex flex-row">
                    <div className="w-full flex flex-col gap-1 justify-between px-3 py-2">
                        <span className="text-xs font-medium text-gray-500">Résultat</span>
                        <div className="flex gap-1">
                            <span className="text-xl font-normal">
                                { 
                                    margin === 0
                                    ? <Icon Icon={Spinner3Solid}
                                        size={24}
                                        className="animate-spin duration-300 text-gray-600" />
                                    : formatCurrency(-((ca ?? 0) - (charges ?? 0)))
                                }
                            </span>
                        </div>
                    </div>
                    <div className="w-full flex flex-col gap-1 justify-between border border-b-0 border-t-0 border-r-0 border-gray-200 px-3 py-2">
                        <span className="text-xs font-medium text-gray-500">Marge</span>
                        <div className="flex gap-1">
                            <span className="text-xl font-normal">
                                { 
                                    margin === 0
                                    ? <Icon Icon={Spinner3Solid}
                                        size={24}
                                        className="animate-spin duration-300 text-gray-600" />
                                    : formatPercent((margin) ?? 0)
                                }
                            </span>
                        </div>
                    </div>
                </div>
                <div className="flex flex-row">
                    <div className="w-full flex flex-col gap-1.5 justify-between border border-l-0 border-r-0 border-gray-200 px-3 py-2">
                        <div className="text-xs font-medium text-gray-500 flex flex-row gap-1 justify-between">
                            <span>Ratio Charges / CA</span>
                            <span className="text-sm font-semibold text-gray-600 bg-gray-200 px-2 py-1 rounded-md">
                                x {ca ? parseFloat(((charges ?? 0) / (ca ?? 0)).toFixed(2)) : 0}
                            </span>
                        </div>
                        <div className="flex flex-col gap-2">
                            <div className="relative flex h-2.5 w-full overflow-hidden rounded-full bg-gray-200">
                                <div
                                    className="absolute left-0 top-0 h-full bg-purple-500 transition-all duration-500"
                                    style={{ width: `${chargesWidth}%` }}
                                />
                                <div
                                    className="absolute right-0 top-0 h-full bg-green-500 transition-all duration-500"
                                    style={{ width: `${caWidth}%` }}
                                />
                            </div>
                            <div className="flex flex-row items-center justify-between text-[10px] text-gray-500">
                                <span className="flex items-center gap-1">
                                    <span className="h-2 w-2 rounded-full bg-purple-500" />
                                    Charges ({formatCurrency(charges ?? 0)})
                                </span>
                                <span className="flex items-center gap-1">
                                    <span className="h-2 w-2 rounded-full bg-green-500" />
                                    CA ({formatCurrency(ca ?? 0)})
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
