"use client";

import { useState, useEffect } from "react";
import { useMultiSelectContext } from "@/lib/contexts/MultiSelectContext";
import { Select } from "@/components/atoms/form/items/Select";
import { statuses } from "../details/configCard";
import { useDataTable } from "@/lib/contexts/DataTableCustomContext";
import { Invoice } from "@/lib/types/invoice";

export default function InvoiceDetailViewActions () {

    const { hasSelection, count, recordBucket, save } = useMultiSelectContext();
    const { pagination, fetchData, activeStatus } = useDataTable<Invoice>();
    const items = pagination?.items as Invoice[] | undefined ?? [];
    const filteredData = items?.filter((invoice: Invoice) => recordBucket.has(invoice.id) );
    const totalAmountHT = filteredData?.reduce((acc: number, invoice: Invoice) => acc + invoice.amount_ht, 0);
    const totalAmountTTC = filteredData?.reduce((acc: number, invoice: Invoice) => acc + invoice.amount_ttc, 0);
    const [status, setStatus] = useState<string>('TBD');
    const [shouldRender, setShouldRender] = useState<boolean>(false);
    const [classNames, setClassNames] = useState<string>('translate-y-0 duration-100');
  
    useEffect(() => {
      let timer: ReturnType<typeof setTimeout>;
  
      if (hasSelection) {
        setShouldRender(true); // eslint-disable-line
        timer = setTimeout(() => {
          setClassNames('-translate-y-12 duration-200');
        }, 80);
      } else {
        setClassNames('translate-y-30 duration-200');
        timer = setTimeout(() => {
          setShouldRender(false);
        }, 300);
      }
    
      return () => clearTimeout(timer);
    }, [hasSelection, count]);

    async function handleAction(status: string) {
      const success = await save(status);
      
      if (success) {
        fetchData({
          status: `${activeStatus ?? 'All'}`,
          page: pagination?.page ?? 1,
          limit: pagination?.limit ?? 30
        });
      }
    }
  
    if (!shouldRender) return null;
  
    return (
      <section className={`${classNames} px-8 absolute z-[8888] right-30 left-30 w-[50%] mx-auto bottom-0`}>
        <div className="flex flex-col bg-white rounded-lg shadow-md border border-gray-200">
          <div className="flex flex-row p-2 gap-2 justify-between">
            <div className="flex flex-row gap-2"> 
            <Select
              label=""
              isEditable={count > 0}
              options={statuses}
              register={{
                  onChange: (newValue: string) => {
                    setStatus(newValue);
                  },
                  name: 'status',
                  value:  status,
                  className: `${count > 0 ? '' : 'opacity-30 !cursor-not-allowed'} rounded-md focus:outline-none transition-all p-2 bg-white border border-gray-200 text-gray-900 text-sm`
              }}
              name="status" />
            <input 
              name="gc_booking"
              disabled={count === 0}
              id="gc_booking"
              placeholder="GC Booking"
              type="text"
              onChange={(e) => {
                  const isNotNumber = !/^\d+$/.test(e.target.value);
                  e.target.value = isNotNumber ? e.target.value.slice(0, -1) : e.target.value;
                  if (isNotNumber) {
                      return;
                  }
              }}
              className={`${count > 0 ? '' : 'opacity-30 !cursor-not-allowed'} bg-white rounded-md focus:outline-none transition-all duration-300 p-2 border border-gray-200 text-gray-900 text-sm`}/>
            </div>
            <div className="flex flex-row gap-2">
              <button
                disabled={count === 0}
                onClick={() => handleAction(status)}
                className={`text-gray-600 border border-gray-200 px-4 py-1 rounded-md ${count === 0 ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}>
                  save
              </button>
              <button
                disabled={count === 0}
                onClick={() => handleAction('archived')}
                className={`text-gray-600 border border-gray-200 px-4 py-1 rounded-md ${count === 0 ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}>
                  archived
              </button>
            </div>
          </div>
          <div className="text-sm flex flex-row justify-between bg-slate-800 rounded-b-lg p-3 text-white gap-1">
            <p className="text-right flex items-center justify-end gap-2">
              Total amount HT
              <span className="font-bold items-center justify-end inline-flex min-w-[70px] bg-green-300/20 text-green-500 p-1 rounded-md">
                {totalAmountHT?.toFixed(2) ?? '0'}
              </span> €
            </p>
            <p className="text-right flex items-center justify-end gap-2">
              Total amount TTC
              <span className="font-bold items-center justify-end inline-flex min-w-[70px] bg-green-300/20 text-green-500 p-1 rounded-md">
                {totalAmountTTC?.toFixed(2) ?? '0'}
              </span> €
            </p>
          </div>
        </div>
      </section>
    )
}