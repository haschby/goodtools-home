"use client";

import { ListView } from '@/components/atoms/listview/ListView';
import { Buyback } from '@/lib/types/buyback';
import { useDataTable } from '@/lib/contexts/DataTableCustomContext';
import { ListHeaders } from './components/listview/headers';
import { BuybackListRow } from './components/listview/rows';
import { BuyBackTabs } from './components/listview/tabs';
import { PaginationAction } from './components/listview/pagination';
import { BuybackStatusFilter } from './components/listview/filter';

import { useMemo } from 'react';
import { buybackColumns } from './config/columns.config';
import { BuybackDetailCard } from './components/details/BuybackDetailCard';


export default function BuybackListView() {

    const {
        pickedRecord } = useDataTable<Buyback>();
        

    const Headers = useMemo(() => <ListHeaders<Buyback>  />, []);
    const Rows = useMemo(() => <BuybackListRow columns={ buybackColumns } />, []);
    const Tabs = useMemo(() => <BuyBackTabs />, []);
    const Pagination = useMemo(() => <PaginationAction<Buyback> />, []);
    const Filters = useMemo(() => <BuybackStatusFilter />, []);

    return (
        <div className="flex flex-col gap-4 h-full">
            <div className="flex gap-4">
            <div className="flex flex-col w-1/2 h-full relative overflow-hidden">
                <ListView
                    filters={ Filters }
                    paginationActions={ Pagination }
                    statuses={ <></> }
                    headers={ Headers }
                    data={ Rows }
                    controlTableActions={ undefined} />
            </div>
            <div className="w-1/2">
                <div className="h-2/3">
                    { pickedRecord && pickedRecord?.document?.url && (
                    <iframe
                        src={ pickedRecord?.document?.url}
                        className="w-full h-full"
                        title="Buyback Details Iframe">
                    </iframe>
                    ) ||
                    <div className="w-full h-full flex items-center justify-center bg-gray-100 border border-b-0 border-gray-200 rounded-t-lg">
                        No Preview Available, please select a record to view the details.
                    </div>}
              </div>

              <div className="h-1/3 rounded-b-lg bg-white border border-gray-200 overflow-auto">
                  { pickedRecord ? (
                    <BuybackDetailCard key={ pickedRecord.id } />
                  ) : (
                    <div className="flex flex-col gap-2 p-4 text-gray-500 text-sm">
                        Select a record to view and edit its details.
                    </div>
                  )}
              </div>
            </div>
            </div>
        </div>
    )
}