"use client";


import RangePriceInvoiceFilter from "./filters/RangePriceInvoiceFilter";

interface SearchFiltersProps {
    closeButton: React.ReactNode;
}

export function SearchFilters(
    { closeButton }: SearchFiltersProps
) {

    return (
        <>

            {/* {
                userSelectedFilters.length > 0 && (

                    <ul className={`${setBorderWhenOpenFilters()} transition-all duration-300 relative z-[99999] h-full overflow-hidden overflow-x-scroll flex flex-row w-full items-center justify-start gap-2 px-2 max-w-[120px]`}> 
                        {
                            userSelectedFilters.map(
                                (filter, index) => (
                                <li key={filter.name} className="relative whitespace-nowrap flex flex-row items-center gap-2 text-amber-400 border border-amber-400 text-sm bg-amber-50 p-1 rounded-md relative">
                                    <p className="flex flex-col text-xs font-semibold">
                                        {`${filter.name}: `}
                                        <span>{`${filter.value.min} - ${filter.value.max}`}</span>
                                    </p>
                                    <span
                                        className="absolute top-0 right-1 cursor-pointer text-black text-xs font-semibold"
                                        onClick={
                                            () =>
                                            removeFilter(filter.name)
                                        }>x</span>
                                </li>
                            ))
                        }
                    </ul>
                )
            }   */}
            <span className="text-sm font-semibold underline">Filters Params</span>
            {closeButton}
            <aside className="flex flex-col">
                <div className="flex flex-col gap-4">
                    <span className="text-sm font-semibold">Price:</span>
                    <RangePriceInvoiceFilter dbMax={4589} />
                </div>
            </aside>
        </>
    )
}