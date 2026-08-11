"use client";

interface RentabilityMetric {
    label: string;
    value: number;
    trend: number;
}

const formatCurrency = (value: number) =>
    new Intl.NumberFormat("fr-FR", {
        style: "currency",
        currency: "EUR",
        maximumFractionDigits: 0,
    }).format(value);

function TrendChart({
    color = "#22c55e",
    gradientId,
    isNegative = false,
}: {
    color?: string;
    gradientId: string;
    isNegative?: boolean;
}) {
    const line = isNegative
        ? "M2 18 C 18 18, 22 46, 40 46 S 62 20, 78 26 S 100 54, 118 54"
        : "M2 42 C 18 42, 22 14, 40 14 S 62 40, 78 34 S 100 6, 118 6";
    const area = `${line} L 118 60 L 2 60 Z`;
    const endY = isNegative ? 54 : 6;

    return (
        <svg
            className="h-6 w-14 shrink-0"
            viewBox="0 0 120 60"
            fill="none"
            preserveAspectRatio="none"
        >
            <defs>
                <linearGradient id={gradientId} x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor={color} stopOpacity="0.25" />
                    <stop offset="100%" stopColor={color} stopOpacity="0" />
                </linearGradient>
            </defs>
            <path
                d={line}
                stroke={color}
                strokeWidth="3"
                strokeLinecap="round"
                fill="none"
            />
            <path d={area} fill={`url(#${gradientId})`} />
            <circle cx="118" cy={endY} r="3.5" fill="#fff" stroke={color} strokeWidth="2.5" />
        </svg>
    );
}

function RentabilityCard({ label, value, trend }: RentabilityMetric) {

    const noPrice = value === 0 && trend === 0;
    const isNegative = value < 0 || trend < 0;
    const accentColor = isNegative ? "#ef4444" : "#22c55e";
    const trendTextClass = isNegative ? "text-red-500" : "text-green-500";
    const gradientId = `rentability-fill-${label.replace(/\s+/g, "-").toLowerCase()}`;

    return (
        <div className="flex w-full flex-col bg-white gap-1 rounded-2xl border border-gray-200 p-3">
            <div className="flex items-center gap-1.5 text-gray-400">
                <span className="text-xs font-medium">{label}</span>
                <span className="flex h-4 w-4 items-center justify-center rounded-full border border-gray-300 text-[10px] font-semibold">
                    i
                </span>
            </div>

            <div className="flex items-center justify-end gap-2">
                {
                    noPrice && (
                        <span className="text-xs font-bold tracking-tight text-gray-900 pr-4">aucune donnee disponible</span>
                    ) || (
                        <>
                            <span className="text-base font-bold tracking-tight text-gray-900 pr-4">
                                {formatCurrency(value)}
                            </span>
                            <TrendChart color={accentColor} gradientId={gradientId} isNegative={isNegative} />
                        </>
                    )
                }
                
            </div>

            <p className="flex items-center gap-1.5 text-xs text-gray-400">
                <span className={`flex items-center gap-1 font-semibold ${trendTextClass}`}>
                    <svg
                        className={isNegative ? "rotate-90" : ""}
                        viewBox="0 0 4 4"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                    >
                        <path d="M3 11 L7 6 L10 9 L14 4" />
                        <path d="M14 4 L14 8 M14 4 L10 4" />
                    </svg>
                    {/* {trend ? `${trend.toFixed(0)}%` : ""} */}
                </span>
            </p>
        </div>
    );
}

interface InvoiceRentabilityProps {
    profit?: number;
    ca?: number;
    charges?: number;
    marging?: number;
}

export default function InvoiceRentability({
    profit = 0,
    ca = 0,
    charges = 0,
    marging = 0,
}: InvoiceRentabilityProps) {
    return (
        <div className="flex flex-col gap-2">
            <div className="flex w-full gap-2">
                <RentabilityCard label="Chiffre d'affaires" value={ca} trend={marging} />
                <RentabilityCard label="Charges" value={charges} trend={marging} />
            </div>
            <div className="flex items-center justify-between rounded-2xl border border-gray-200 p-3 bg-white">
                <p className="text-gray-800 flex items-center gap-1">
                    <span className="font-bold">Profit :</span>
                    <span className="text-gray-400">{formatCurrency(profit)}</span>
                </p>
                <span className="text-gray-400">
                    {marging ? `${marging.toFixed(0)}%` : "0%"}
                </span>
            </div>
        </div>
    );
}
