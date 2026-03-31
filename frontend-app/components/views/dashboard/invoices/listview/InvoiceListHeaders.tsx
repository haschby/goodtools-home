"use client";

import { useDataTable } from '@/lib/contexts/DataTableCustomContext';
import { Invoice } from '@/lib/types/invoice';
import { CheckBoxfilter } from '@/components/atoms/form/items/CheckboxFilter';

interface ColumnProps {
    label: string;
    align: string;
    maxWidth?: string;
    isNumber?: boolean;
    canSticky?: boolean;
}

export default function InvoiceListHeaders() {

    const { columns, activeStatus, pagination } = useDataTable<Invoice>();

    const items: Invoice[] = pagination?.items as Invoice[] | undefined ?? [];

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
                                activeStatus !== 'All' && activeStatus ? 
                                <CheckBoxfilter
                                    keyItems={items?.filter( (invoice: Invoice) => invoice.gc_booking).map( (invoice: Invoice) => invoice.id) ?? []}
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



// const CheckBoxfilter = () => {
//     const checkBoxRef = useRef<HTMLInputElement>(null);
//     const selectRef = useRef<HTMLSpanElement>(null);
//     const [isChecked, setIsChecked] = useState(false);

//     return (
//         <>
//             <input
//                 ref={checkBoxRef}
//                 type="checkbox"
//                 checked={isChecked}
//                 hidden
//                 readOnly
//                 data-id="all-records" />
            
//             <span
//                 ref={selectRef}
//                 className={`p-1 rounded-md bg-white shadow-md `}
//                 onClick={
//                     () => {
//                         setIsChecked(!isChecked);
//                     }
//                 }>
//                     <Icon
//                         Icon={CheckStroke}
//                         size={18}
//                         strokeWidth={4}
//                         className={`${isChecked ? 'bg-green-300/20 text-green-500 transform scale-120 transition-transform duration-300' : 'transform scale-0 transition-transform duration-300'}`} />
                
//             </span>
//         </>
//     )
// }
