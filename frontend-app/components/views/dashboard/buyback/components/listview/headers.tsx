import { useDataTable } from "@/lib/contexts/DataTableCustomContext";
import { Buyback } from "@/lib/types/buyback";
import { CheckBoxfilter } from '@/components/atoms/form/items/CheckboxFilter';
import { BaseEntity } from "@/lib/types/base";

interface ColumnProps {
    label: string;
    align: string;
    maxWidth?: string;
    isNumber?: boolean;
    canSticky?: boolean;
}

interface HeadersProps<T> {
    getSelectableIds?: (items: T[]) => string[] | undefined;
}

type headersModel = BaseEntity & { id: string };

export function ListHeaders<T extends headersModel>(
    { getSelectableIds }: HeadersProps<T>
) {

    const { columns, activeStatus, pagination, pickRecordById } = useDataTable<T>();

    const items: T[] = pagination?.items as T[] | undefined ?? [];

    return (
        <>
           {
            (columns as ColumnProps[]).map(
                ({ label, maxWidth, isNumber, canSticky }: ColumnProps, index: number) => {

                const paddingSide = (
                    index === 0 && 'pl-6 rounded-tl-xl'
                    ||
                    index === columns.length - 1 && 'pr-6 rounded-tr-xl'
                ) || '';

                if (canSticky) {
                    return (
                        <th
                            key={index}
                            style={{ width: maxWidth, minWidth: maxWidth }}
                            className={`sticky left-0 bg-gray-50 text-gray-800`}>
                            <span className="h-13 flex items-center justify-center border-r border-b border-gray-200">
                            {
                                activeStatus !== 'All'
                                && activeStatus
                                && getSelectableIds ? 
                                <CheckBoxfilter
                                    click={
                                        (state: boolean) => {
                                        if (state) {
                                            pickRecordById(null);
                                        }
                                    }}
                                    keyItems={
                                        getSelectableIds(items) ?? []
                                    }
                                    id={'All'} /> 
                                :  <>{label}</>
                            }
                            </span>
                        </th>
                    )
                }
                return (    
                    <th
                        key={index}
                        style={{ width: maxWidth, minWidth: maxWidth }}
                        className={`whitespace-nowrap text-sm font-bold bg-gray-100 text-gray-800`}>
                        <span
                            className={`border-r border-b border-gray-200 px-6 ${paddingSide} flex py-4 ${isNumber ? 'justify-end' : 'justify-start'}`}>
                            {label} 
                        </span>
                    </th>
                )
            })
           }
        </>
    );
}