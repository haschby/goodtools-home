"use client";

import { useMultiSelectContext } from "@/lib/contexts/MultiSelectContext";
import { useRef } from "react";
import { useCallback } from "react";
import Icon from "@/components/atoms/Icon";
import { CheckStroke, Spinner3Bulk } from "@lineiconshq/free-icons";

interface CheckBoxfilterProps {
    id: string;
    disabled?: boolean;
    keyItems: string[];
    click?: (state: boolean) => void;
}

export function CheckBoxfilter(
    { id, disabled = false, keyItems, click }: CheckBoxfilterProps ) {

    const { actions, recordBucket, isSaving } = useMultiSelectContext();
    // const { data } = useDataTable<T>();
    const checkBoxRef = useRef<HTMLInputElement>(null);
    const selectRef = useRef<HTMLSpanElement>(null);

    const isChecked = id === 'All' 
    ? recordBucket.has('All')
    : recordBucket.has(id);

    const handleCheckBoxClick = useCallback(
        (event: React.MouseEvent) => {
        event.preventDefault();
        event.stopPropagation();

        if (id === 'All') {
            if (isChecked) {
                actions.clear();
            } else {
                actions.addNewRecord('All');
                keyItems.forEach(key => actions.addNewRecord(key));
            }
            console.log('recordBucket.size : ', isChecked);
            click?.(!isChecked);
            return;
        }

        if (!isChecked) {
            actions.addNewRecord(id);
        } else {
            actions.removeRecord(id);
        }

        click?.(isChecked);

    }, [id, isChecked, actions, keyItems, click]);

    if (disabled) {
        return (
            <span className="p-1 bg-gray-300/20 font-semibold text-gray-500 text-xs rounded-md">
            </span>
        )
    }

    return (
        <label
            className="cursor-pointer w-full h-full flex items-center justify-center"
            onClick={handleCheckBoxClick}>
            <input
                id={`checkbox-${id}`}
                ref={checkBoxRef}
                type="checkbox"
                checked={isChecked}
                hidden
                readOnly
                data-id="all-records" />
            {
                isSaving &&
                recordBucket.has(id) ? (
                    <Icon
                        Icon={Spinner3Bulk}
                        size={20}
                        strokeWidth={2}
                        className="animate-spin text-green-500" />
                ) : (
                    <span
                    ref={selectRef}
                    className={`h-6 w-6 border ${isChecked ? 'border-green-500 bg-green-300/20' : 'border-gray-200'} transition-all duration-300 rounded-md overflow-hidden flex items-center justify-center`}
                    >
                    <Icon
                        Icon={CheckStroke}
                        size={16}
                        strokeWidth={4}
                        className={`p-[3px] h-full w-full rounded-md ${isChecked ? 'text-green-500 transform scale-100 transition-transform duration-300' : 'bg-white transform scale-0 transition-transform duration-300'}`} />
                
                    </span>       
                )
            }
        </label>
    )
}