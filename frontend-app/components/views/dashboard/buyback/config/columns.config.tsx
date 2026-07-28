import { ColumnProps } from "@/lib/types/common";
import { Buyback } from "@/lib/types/buyback";
import { StatusRow } from "@/components/atoms/listview/RowItems/StatusRow";

export const buybackColumns: ColumnProps<Buyback>[] = [
    {
        keyfield: '',
        align: 'left',
        canSticky: true,
        isFirst: true,
        maxWidth: '150px',
        renderItem: (buyback: Buyback) => <span className="text-gray-500">1</span>,
    },
    {
        keyfield: 'id',
        align: 'left',
        maxWidth: '120px',
        renderItem: (buyback: Buyback) => buyback.id,
    },
    {
        keyfield: 'status',
        align: 'left',
        maxWidth: '120px',
        renderItem: (buyback: Buyback) =>
        <StatusRow className="px-2 py-1 rounded-md" status={buyback.status.toString()} />
    },
    {
        keyfield: 'gc_booking',
        align: 'right',
        isNumber: true,
        maxWidth: '150px',
        renderItem: (buyback: Buyback) => buyback.gc_booking,
    },
    {
        keyfield: 'amount',
        align: 'right',
        isLast: true,
        isNumber: true,
        maxWidth: '150px',
        renderItem: (buyback: Buyback) => buyback.amount,
    },
];