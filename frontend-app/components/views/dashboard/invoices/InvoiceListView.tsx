"use client";

import { useState, useCallback, useEffect, useRef, useMemo } from 'react';
import { Select } from '@/components/atoms/form/items/Select';
import { Invoice } from '@/lib/types/invoice';
import { ListView } from '@/components/atoms/listview/ListView';
import Icon from '@/components/atoms/Icon';
import InvoiceDetailView from './details/InvoiceDetailView';
import { ArrowRightCircleSolid, Train3Bulk } from '@lineiconshq/free-icons';
import { useDataTable } from '@/lib/contexts/DataTableCustomContext';
import SearchBar from './search/searchBar';
import { MultiSelectProvider } from '@/components/providers/MultiSelectProvider';

import { 
  InvoiceListHeaders, 
  InvoiceListRowItem,
  InvoiceListStatusBar,
  InvoiceDetailViewActions
} from './listview/InvoiceListViewComponent';

import TitleInfo from '@/components/atoms/view/TitleInfo';

export default function InvoiceListView() {

  const {
    pickedRecord,
    pickRecordById, 
    fetchData, 
    data, 
    isLoading, 
    totalRows,
    hasMore,
    activeStatus } = useDataTable<Invoice>();

  const dataRef = useRef(data);
  const refStatus = useRef(activeStatus);

  const statusResetCallback = useCallback(() => {
    if (pickedRecord) {
      return true;
    }

    if (refStatus.current !== activeStatus) {
      return true;
    }
    return false;
  }, [activeStatus, pickedRecord]);

  useEffect(() => {
      dataRef.current = data;
  }, [data]);

  const handleScrollEnd = useCallback(
    (isEndOfList: boolean) => {
      if (!isEndOfList || isLoading || !hasMore) return;

      const lastItem = dataRef.current?.[dataRef.current.length - 1];
      if (!lastItem) return;

      fetchData({ 
          isEndOfList: true, 
          cursor: lastItem.created_at as string,
          id: lastItem.id as string
      });
    },
    [fetchData, isLoading, hasMore] );

  const handleScrollEndCallback = useCallback(
    (isEndOfList: boolean) => {
    handleScrollEnd(isEndOfList);
  }, [handleScrollEnd]);

  const RowItems = useMemo(() => <InvoiceListRowItem />, []);
  const ActionsList = useMemo(() => !pickedRecord && <InvoiceDetailViewActions /> || <></>, [pickedRecord]);
  const StatusBar = useMemo(() => <InvoiceListStatusBar />, []);
  const Filters = useMemo(() => <SearchBar />, []);
  const Headers = useMemo(() => <InvoiceListHeaders />, []);

  return (
    <MultiSelectProvider reset={statusResetCallback}>
      <div className={`h-screen`}>
        <div className="flex flex-row">
          <div className={`px-6 relative h-screen flex flex-col transition-all duration-300 ${ pickedRecord ? 'w-[35%] lg:flex hidden' : 'w-full'}`}>
      
            <TitleInfo
              title="Invoice Records"
              baseLineText="View detailed invoices records by clicking on the row."
              totalRows={totalRows}
            />
              <ListView
                onScrollEnd={handleScrollEndCallback}
                filters={ Filters }
                actionsList={ <></> }
                statuses={ StatusBar }
                headers={ Headers }
                data={ RowItems }
                controlTableActions={
                  <div
                    id="footer-loader-container"
                    className="bg-white border-t border-gray-200 absolute bottom-0 left-0 right-0 flex items-center w-full gap-4 justify-center p-4 text-gray-700">
                    GOOD
                    <Icon
                      className={`${isLoading ? 'animate-spin text-blue-500' : 'text-gray-700'}`}
                      Icon={Train3Bulk}
                      size={20}
                      strokeWidth={2} />
                    COLLECT
                  </div>
                }
                />
              { ActionsList }
          </div>
          { 
            pickedRecord &&
            <InvoiceDetailView
              closeButton={
                <button
                  className="group cursor-pointer inline-flex items-center gap-2"
                  onClick={() => {
                    pickRecordById(null);
                  }}>
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
    </MultiSelectProvider>
  )
}