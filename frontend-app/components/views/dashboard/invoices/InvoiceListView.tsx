"use client";

import { useMemo, useState, useCallback } from 'react';
import { Invoice } from '@/lib/types/invoice';
import { ListView } from '@/components/atoms/listview/ListView';
import Icon from '@/components/atoms/Icon';
import InvoiceDetailView from './details/InvoiceDetailView';
import { ArrowRightCircleSolid, SlidersHorizontalSquare2Solid, Train3Bulk } from '@lineiconshq/free-icons';
import { useDataTable } from '@/lib/contexts/DataTableCustomContext';

import { 
  InvoiceListHeaders, 
  InvoiceListRowItem,
  InvoiceListStatusBar,
  InvoiceListTitleInfo
} from './listview/InvoiceListViewComponent';

const Filters = () => {
  const [isFiltersOpen, setIsFiltersOpen] = useState(false);
  
  return (
    <div className="flex text-gray-700 p-2">
      <div className="px-6 py-6 flex items-center w-full gap-4 rounded-md">
        <input
          type="Search"
          placeholder="Search"
          className="self-start w-full max-w-[400px] rounded-lg border border-gray-200 p-2 bg-white" />
        <button
          onClick={() => setIsFiltersOpen(!isFiltersOpen)}
          className="bg-gray-700 text-white flex items-center gap-2 justify-center rounded-lg px-2 py-2 w-full max-w-[150px]">
          <Icon
            Icon={SlidersHorizontalSquare2Solid}
            size={20}
            strokeWidth={2} />
          <span className="text-sm font-semibold">Filters</span>
        </button>
      </div>
    </div>
  )
}

export default function InvoiceListView() {

  const { pickedRecord, setPickedRecord, fetchData, data, isLoading } = useDataTable<Invoice>();


  const isDetailViewOpen = useMemo(() => {
    return !!pickedRecord;
  }, [pickedRecord]);

  const handleScrollEnd = useCallback(
    (isEndOfList: boolean) => {
      if (isEndOfList) {
        fetchData({ 
          isEndOfList, 
          cursor: data?.[data.length - 1].created_at as string,
          id: data?.[data.length - 1].id as string
        });
      }
    }, [fetchData, data]);

  return (
    <>
      <div className={`h-screen bg-white`}>
        <div className="flex flex-row">
          <div className={`flex flex-col transition-all duration-300 ${ pickedRecord ? 'w-[30%] lg:flex hidden' : 'w-full'}`}>
      
            <InvoiceListTitleInfo
              title="Invoice Records"
              baseLineText="View detailed invoices records by clicking on the row."
            />      
            <ListView
              onScrollEnd={ 
                (isEndOfList: boolean) =>
                handleScrollEnd(isEndOfList)
              }
              filters={ <Filters /> }
              actionsList={ <></> }
              statuses={ <InvoiceListStatusBar /> }
              headers={ <InvoiceListHeaders /> }
              data={ <InvoiceListRowItem /> } />
              <div className="flex items-center w-full gap-4 justify-center p-4 text-gray-700">
                GOOD
                <Icon
                  className={`${isLoading ? 'animate-spin text-blue-500' : 'text-gray-700'}`}
                  Icon={Train3Bulk}
                  size={20}
                  strokeWidth={2} />
                COLLECT
              </div>
          </div>
          { 
            isDetailViewOpen &&
            <InvoiceDetailView
              closeButton={
                <button
                  className="group cursor-pointer inline-flex items-center gap-2"
                  onClick={() => setPickedRecord(null) }>
                    <Icon
                      Icon={ArrowRightCircleSolid}
                      size={24}
                      strokeWidth={2}
                      className="transition-all duration-300 text-gray-300 group-hover:text-gray-700" />
                      <span className="text-gray-500 group-hover:text-gray-700">close</span>
                </button>
              }
            />
          }
        </div>
      </div>
    </> 
  )
}

          