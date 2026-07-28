"use client";

import { useCallback, useMemo } from "react";
import { useDataTable } from "@/lib/contexts/DataTableCustomContext";
import { Buyback } from "@/lib/types/buyback";
import { Select } from "@/components/atoms/form/items/Select";
import { buybackStatuses } from "@/components/views/dashboard/buyback/config/statuses.config";
import { StampStroke } from "@lineiconshq/free-icons";
import Icon from "@/components/atoms/Icon";

const ALL_STATUS = "All";

export function BuybackStatusFilter() {

    const {
        activeStatus,
        setActiveStatus,
        fetchData,
        pagination
    } = useDataTable<Buyback>();

    const options = useMemo(
        () => [{ label: ALL_STATUS, value: ALL_STATUS }, ...buybackStatuses],
        []
    );

    const currentStatus = activeStatus ?? ALL_STATUS;

    const handleSelectStatus = useCallback(
        (status: string) => {
            setActiveStatus(status);
            fetchData({
                status: status,
                page: 1,
                limit: pagination?.limit ?? 30
            });
        },
        [setActiveStatus, fetchData, pagination?.limit]
    );

    return (
        <div className="flex items-end justify-end">
            <Select
                icon={{
                    position: 'left',
                    icon: <Icon Icon={StampStroke} size={16} strokeWidth={2} />
                }}
                isEditable
                label=""
                options={options}
                name="status-filter"
                register={{
                    onChange: handleSelectStatus,
                    name: "status-filter",
                    value: currentStatus,
                    className: "rounded-md focus:outline-none transition-all p-2 border border-gray-200 w-full text-gray-900 text-sm"
                }}
            />
        </div>
    );
}
