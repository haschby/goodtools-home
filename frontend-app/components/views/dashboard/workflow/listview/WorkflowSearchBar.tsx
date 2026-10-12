"use client";

import { useEffect, useRef } from "react";
import { SearchBox } from "@/components/views/dashboard/invoices/search/searchBox";
import { useDataTable } from "@/lib/contexts/DataTableCustomContext";
import { useQueryClient } from "@/lib/contexts/QueryClientContext";
import { Workflow } from "@/lib/types/workflow";

export default function WorkflowSearchBar() {

    const { fetchData, activeStatus, pagination } = useDataTable<Workflow>();
    const { queryParams } = useQueryClient();
    const queryString = queryParams?.toString() ?? null;

    // The initial load is already handled by the DataListProvider; only
    // re-fetch when the search query actually changes.
    const previousQuery = useRef<string | null>(queryString);

    useEffect(() => {
        if (previousQuery.current === queryString) return;
        previousQuery.current = queryString;

        fetchData({
            status: activeStatus ?? 'All',
            page: 1,
            limit: pagination?.limit ?? 30,
            query: queryString
        });
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [queryString]);

    return (
        <div className="flex flex-col relative my-3 px-6">
            <SearchBox placeholder="Search for workflows (id, provider, status, message)..." />
        </div>
    );
}
