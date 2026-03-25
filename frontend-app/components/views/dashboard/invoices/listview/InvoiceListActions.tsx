"use client";

import { useState, useEffect } from "react";
import { useMultiSelectContext } from "@/lib/contexts/MultiSelectContext";
import { useDataTable } from "@/lib/contexts/DataTableCustomContext";
import { Invoice } from "@/lib/types/invoice";
import { Select } from "@/components/atoms/form/items/Select";
import { statuses } from "../details/configCard";


export default function InvoiceDetailViewActions () {

    const { save, hasSelection, count, recordBucket } = useMultiSelectContext();
    const { data } = useDataTable<Invoice>();
    const filteredData = data.filter(invoice => recordBucket.has(invoice.id) );
    const totalAmount = filteredData.reduce((acc, invoice) => acc + invoice.amount_ttc, 0);
    const [status, setStatus] = useState<string>('TBD');
    const [shouldRender, setShouldRender] = useState<boolean>(false);
    const [classNames, setClassNames] = useState<string>('opacity-0 translate-y-40 duration-300');
  
    useEffect(() => {
      let timer: ReturnType<typeof setTimeout>;
  
      if (hasSelection) {
        setShouldRender(true); // eslint-disable-line
        timer = setTimeout(() => {
          setClassNames('opacity-100 -translate-y-5 duration-300');
        }, 80);
      } else {
        setClassNames('opacity-0 translate-y-40 duration-300');
        timer = setTimeout(() => {
          setShouldRender(false);
        }, 300);
      }
    
      return () => clearTimeout(timer);
    }, [hasSelection]);
  
    if (!shouldRender) return null;
  
    return (
      <section
        className={`${classNames} bottom-4 left-0 right-0 mx-auto absolute z-[99999] flex flex-col w-1/2`}>
        <div className="w-full shadow-[0_0_20px_-8px_rgba(0,0,0,0.5)] flex flex-col w-[300px] text-black rounded-md">
          <div className="bg-white w-full flex flex-row items-end pb-4 px-4 justify-between border border-gray-200 rounded-t-md">
            <div className="relative text-gray-900 flex flex-row gap-4">
              <div className="flex flex-col">
                <Select
                  isEditable={count > 0}
                  label="Status"
                  options={statuses}
                  register={{
                      onChange: (newValue: string) => {
                        setStatus(newValue);
                      },
                      name: 'status',
                      value:  status,
                      className: `${count > 0 ? '' : 'opacity-30 !cursor-not-allowed'} rounded-md focus:outline-none transition-all p-1 bg-white border border-gray-200 text-gray-900 text-sm`
                  }}
                  name="status" />
              </div>
  
              <div className="flex flex-col">
                  <label className="text-sm py-2" htmlFor="gc_booking">
                      <span className="w-full font-semibold">Booking Reference</span>
                  </label>
                  <input 
                      name="gc_booking"
                      disabled={count === 0}
                      id="gc_booking"
                      type="text"
                      onChange={(e) => {
                          const isNotNumber = !/^\d+$/.test(e.target.value);
                          e.target.value = isNotNumber ? e.target.value.slice(0, -1) : e.target.value;
                          if (isNotNumber) {
                              return;
                          }
                      }}
                      className={`${count > 0 ? '' : 'opacity-30 !cursor-not-allowed'} bg-white text-right rounded-md focus:outline-none transition-all duration-300 p-1 border border-gray-200 text-gray-900 text-sm`}
                  />
              </div>     
            </div>   
            <div className="flex gap-2 items-center justify-start">
              <button
                disabled={count === 0}
                onClick={() => save(status)}
                className={`font-bold bg-green-300/20 text-green-500 px-4 py-1 rounded-md ${count === 0 ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}>
                  save
              </button>
              <button
                disabled={count === 0}
                onClick={() => save('archived')}
                className={`font-bold bg-violet-300/20 text-violet-500 px-4 py-1 rounded-md ${count === 0 ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}>
                  archived
              </button>
            </div>
          </div>
          <div className="flex items-center justify-between bg-slate-800 text-slate-500 p-2 px-4 rounded-b-md text-white">
            <p className={`flex items-center gap-2 text-xl font-bold text-green-500 px-2 rounded-md ${count === 0 ? 'bg-orange-300/20 text-orange-500' : 'bg-green-300/20 text-green-500'}`}>
              {count}
              <span className="text-xs">{count === 0 ? 'Any records available to process' : 'records selected to process'}</span>
            </p>
            <p className="flex gap-2 items-center font-semibold">
              Total Amount: <span className="text-xl bg-green-300/20 text-green-500 px-2 py-1 rounded-md">{parseInt(totalAmount.toFixed(2))}</span> €
            </p>
          </div>
        </div>
      </section>
    )
}