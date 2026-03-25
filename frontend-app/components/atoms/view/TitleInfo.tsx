"use client";

interface TitleInfoProps {
    title: string;
    totalRows?: number | null;
    baseLineText: string;
}

export default function TitleInfo(
    { title, totalRows = null, baseLineText }: TitleInfoProps
) {
    const setBGcolorToRows = (length: unknown | number) => {
        if (length === 0) return 'bg-gray-200 text-gray-500';
        return 'bg-green-300/20 text-green-500';
    }

    const printTotalRows = () => {
        return (
            <span className={`text-xs rounded-md px-2 py-1 ${setBGcolorToRows(totalRows)}`}>
                { totalRows } data
            </span>
        )
    }

    return (
        <div className="flex flex-col w-full mt-6 mb-12">
            <h1 className="flex items-center text-2xl font-semibold text-gray-800 gap-4">
                { title }
                { printTotalRows() }
            </h1>
            <p>
                <span className="text-sm text-gray-400">
                    { baseLineText }
                </span>
            </p>
        </div>
    );
}

