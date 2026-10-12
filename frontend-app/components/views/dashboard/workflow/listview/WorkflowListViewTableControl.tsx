"use client";

import { useCallback } from "react";
import { useDataTable } from "@/lib/contexts/DataTableCustomContext";
import { useQueryClient } from "@/lib/contexts/QueryClientContext";
import { Workflow } from "@/lib/types/workflow";
import Icon from "@/components/atoms/Icon";
import { ArrowLeftBulk, ArrowRightBulk } from '@lineiconshq/free-icons';

const LIMIT_OPTIONS = ['30', '70', '100'];

export default function WorkflowListViewTableControl() {

    const { pagination, fetchData, activeStatus, isLoading } = useDataTable<Workflow>();
    const { queryParams } = useQueryClient();
    const query = queryParams?.toString() ?? null;

    const page = pagination?.page ?? 1;
    const limit = pagination?.limit ?? 30;
    const totalPages = Math.max(pagination?.total_pages ?? 1, 1);

    const goTo = useCallback(
        (nextPage: number, nextLimit: number = limit) => {
            fetchData({
                status: activeStatus ?? 'All',
                page: nextPage,
                limit: nextLimit,
                query
            });
        },
        [fetchData, activeStatus, limit, query]
    );

    const isFirst = page <= 1;
    const isLast = page >= totalPages;

    return (
        <section className="bg-gray-50 p-3 flex flex-row gap-2 items-center justify-between border-t border-b border-gray-200">
            <div className="flex flex-row gap-2 items-center">
                <div className="font-bold text-sm flex flex-row gap-2 items-center bg-gray-200 rounded-md p-1 border border-gray-200">
                    { LIMIT_OPTIONS.map((option) => (
                        <button
                            key={option}
                            disabled={isLoading}
                            onClick={() => goTo(1, parseInt(option))}
                            className={`cursor-pointer ${limit.toString() === option ? 'shadow-md bg-white text-gray-800' : 'text-gray-500'} rounded-md p-1`}
                        >
                            {option}
                        </button>
                    ))}
                </div>
                <span className="text-xs">Workflows per page</span>
            </div>
            <div className="flex flex-row gap-2 items-center text-gray-600">
                <button
                    onClick={() => goTo(page - 1)}
                    disabled={isFirst || isLoading}
                    className={`${isFirst ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'} shadow-md border border-gray-200 flex flex-row gap-2 items-center bg-white p-2 rounded-md`}>
                    <Icon Icon={ArrowLeftBulk} size={16} strokeWidth={2} />
                </button>
                <p className="text-sm text-gray-500 flex flex-row gap-2 items-center">
                    <input
                        readOnly={true}
                        type="text"
                        className="p-1 w-10 border border-gray-200 rounded-md font-bold text-right bg-white"
                        value={page.toString()}
                    />
                    / {totalPages}
                </p>
                <button
                    onClick={() => goTo(page + 1)}
                    disabled={isLast || isLoading}
                    className={`${isLast ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'} shadow-md border border-gray-200 flex flex-row gap-2 items-center bg-white p-2 rounded-md`}>
                    <Icon Icon={ArrowRightBulk} size={16} strokeWidth={2} />
                </button>
            </div>
        </section>
    )
}
