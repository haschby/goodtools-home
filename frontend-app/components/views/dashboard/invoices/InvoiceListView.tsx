"use client";

import { useState, useCallback, useEffect, useRef, useMemo } from 'react';
import { Invoice } from '@/lib/types/invoice';
import { ListView } from '@/components/atoms/listview/ListView';
import Icon from '@/components/atoms/Icon';
import InvoiceDetailView from './details/InvoiceDetailView';
import { ArrowRightCircleSolid, Train3Bulk } from '@lineiconshq/free-icons';
import { useDataTable } from '@/lib/contexts/DataTableCustomContext';
import SearchBar from './search/searchBar';

import { 
  InvoiceListHeaders, 
  InvoiceListRowItem,
  InvoiceListStatusBar
} from './listview/InvoiceListViewComponent';

import TitleInfo from '@/components/atoms/view/TitleInfo';


export default function InvoiceListView() {

  const {
    pickedId,
    pickedRecord,
    pickRecordById, 
    fetchData, 
    data, 
    isLoading, 
    totalRows,
    hasMore } = useDataTable<Invoice>();


  const [isDetailViewOpen, setIsDetailViewOpen] = useState(false);
    
  useEffect(() => {
    let cancel = false;
    
    const openLeftPanel = async () => {
      if (pickedId && !cancel) {
        setIsDetailViewOpen(true);
      }
    };

    openLeftPanel();

    return () => { 
      cancel = true; 
      setIsDetailViewOpen(false);
    };
  }, [pickedId]);

  const dataRef = useRef(data);

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
    }, [fetchData, isLoading, hasMore] // ✅ stable
  );

  const handleScrollEndCallback = useCallback((isEndOfList: boolean) => {
    handleScrollEnd(isEndOfList);
  }, [handleScrollEnd]);

  const rowItems = useMemo(() => <InvoiceListRowItem />, []);


  return (
    <>
      <div className={`h-screen`}>
        <div className="flex flex-row">
          <div className={`relative h-screen flex flex-col transition-all duration-300 ${ pickedRecord ? 'w-[35%] lg:flex hidden' : 'w-full'}`}>
      
            <TitleInfo
              title="Invoice Records"
              baseLineText="View detailed invoices records by clicking on the row."
              totalRows={totalRows}
            />

            <ListView
              onScrollEnd={handleScrollEndCallback}
              filters={ <SearchBar /> }
              actionsList={ <></> }
              statuses={ <InvoiceListStatusBar /> }
              headers={ <InvoiceListHeaders /> }
              data={ rowItems }
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
          </div>
          { 
            pickedRecord &&
            <InvoiceDetailView
              closeButton={
                <button
                  className="group cursor-pointer inline-flex items-center gap-2"
                  onClick={() => {
                    pickRecordById(null);
                    setIsDetailViewOpen(false);
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
    </> 
  )
}

          