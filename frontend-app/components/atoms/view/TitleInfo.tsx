"use client";

interface TitleInfoProps {
    title: string;
    totalRows?: number | null;
    baseLineText: string;
    buttonActions?: React.ElementType[] | null;
}

export default function TitleInfo(
    { title, totalRows = null, baseLineText, buttonActions = null }: TitleInfoProps
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
        <div className="flex items-center gap-4 w-full justify-between py-6">
            <div className="flex flex-col w-full">
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
            { buttonActions && (
                <div className="flex items-center gap-2 w-full justify-end">
                    { 
                        buttonActions.map(
                            (component: React.ElementType, index: number) => {
                            const Component = component;
                            return (
                                <Component key={`button-action-${index}`} />
                            )
                            }
                        )
                    }
                </div>
            ) }
        </div>
    );
}

