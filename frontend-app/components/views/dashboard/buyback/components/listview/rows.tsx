import { useDataTable } from "@/lib/contexts/DataTableCustomContext";
import { ColumnProps } from '@/lib/types/common';
import { RowItem } from "@/components/atoms/listview/RowItems/Row";

interface BuybackListRowProps<T extends { id: string }> {
    columns: ColumnProps<T>[];
}

export function BuybackListRow<T extends { id: string }>
({ columns }: BuybackListRowProps<T>) {

    const {
        pagination,
        pickedRecord,
        pickRecordById, isLoading } = useDataTable<T>();

    const fetchedItems: T[] = pagination?.items as T[] | undefined ?? [];

    const handlePickRecord = (item: T) => {
        if (pickedRecord?.id === item.id) pickRecordById(null);
        else pickRecordById(item.id);
    }

    return (
        <>
            { 
                fetchedItems?.map(
                (item: T, index: number) => {
                    const isPicked = pickedRecord?.id === item.id;
                    return (
                        <tr
                            id={item.id}
                            key={`${item.id}-${index}`}
                            className={`${isPicked ? 'bg-green-300/50' : 'bg-white'} cursor-pointer hover:bg-green-300/20 transition-all duration-300`}
                            onClick={() => handlePickRecord(item)}>
                                { columns.map(
                                    (column: ColumnProps<T>) =>
                                        <RowItem
                                            canSticky={column?.canSticky || false}
                                            key={column.keyfield}
                                            isFirst={column.isFirst}
                                            isLast={column.isLast}
                                            maxWidth={column.maxWidth}
                                            isNumber={column.isNumber}
                                            renderItem={
                                                column.renderItem(item as T)
                                            } />
                                )}
                        </tr> 
                    )
                })
            }
        </>
    )
}