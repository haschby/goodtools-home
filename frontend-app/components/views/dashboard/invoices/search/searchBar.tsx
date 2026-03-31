"use client";

import { useState, useEffect } from "react";
import { SearchBox } from "./searchBox";
import { SearchFilters } from "./searchFiltersContainer";
// import { searchInvoices, getInvoices } from '@/actions/invoice.actions';
import { useDataTable } from "@/lib/contexts/DataTableCustomContext";
import { Invoice } from "@/lib/types/invoice";
import { useQueryClient } from "@/lib/contexts/QueryClientContext";

export default function SearchBar() {

    const [isOpenFilters, setIsOpenFilters] = useState(false);

    const { fetchData, activeStatus, pagination } = useDataTable<Invoice>();
    const { queryParams } = useQueryClient();
    const queryString = queryParams?.toString() ?? null;

    useEffect(() => {
        fetchData({
            status: activeStatus ?? 'All',
            page: pagination?.page ?? 1,
            limit: pagination?.limit ?? 30,
            query: queryString
        });
    }, [queryString]);

    return (
        <div className="flex flex-col relative my-4">
            <div className="">
                <SearchBox />
                {/* <div className="text-md flex items-center z-[99999] w-1/2">
                    <button
                        onClick={ () => { setIsOpenFilters(!isOpenFilters) }}
                        className="mr-2 cursor-pointer sticky left-0 text-md max-w-[180px] bg-gray-50 py-6 px-4 flex items-center gap-2 font-semibold">
                        <Icon Icon={FileMultipleStroke} size={20} strokeWidth={2} />
                        Filters
                    </button>
                    {
                        haveFilters.length > 0 && (
                            <div className="flex flex-row items-center gap-2 overflow-hidden overflow-x-scroll">
                                <SelectedFiltersContainer />
                            </div>
                        )
                    }
                    <button
                        onClick={() => { setIsOpenFilters(false) }}
                        className="ml-2 px-2 py-1 whitespace-nowrap flex bg-gray-200 rounded-md cursor-pointer text-md flex items-center gap-2">
                        Clear filters
                    </button>
                    
                </div> */}
            </div>
            <div className="relative">
            {
                isOpenFilters && (
                    <div className="flex flex-col gap-4 bg-black absolute top-[0.8] left-0 w-full shadow-md bg-white rounded-b-md p-6 z-[88888]">
                        <SearchFilters
                            closeButton={
                                <button
                                    onClick={() => setIsOpenFilters(false)}
                                    className="cursor-pointer text-md flex items-center gap-2 absolute top-4 right-6">
                                        X
                                </button>
                            }
                        />
                    </div>
                )
            }
            </div>
        </div>
    );
}