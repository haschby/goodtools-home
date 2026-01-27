"use client";

import { useRef, ChangeEvent } from "react";
import Icon from "@/components/atoms/Icon";
import { Download1Solid } from "@lineiconshq/free-icons";

export default function ImportInvoiceForm() {
    const inputRef = useRef<HTMLInputElement>(null);
    
    const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
        const files = event.target.files;
        if (!files) return;
        const newFormData = new FormData();
        for( let i = 0; i < files.length; i++ ) {
            newFormData.append("files", files[i]);
        }
    }

    return (
        <aside className="absolute right-4 top-3 inline-flex gap-4 items-center text-gray-700">
            <input
                ref={inputRef}
                type="file"
                accept="application/pdf,zip,application/octet-stream,application/zip,application/x-zip,application/x-zip-compressed"
                multiple
                onChange={handleFileChange}
                className="hidden" />
            <p className="border-r border-gray-800 pr-2">
                https://www.goodcollect.co
            </p>
            <button
                className="cursor-pointer py-2 px-4 bg-black shadow-md shadow-gray-600 rounded-lg"
                onClick={() => inputRef.current?.click()}>
                <span className="flex items-center gap-2 text-white text-md font-normal">
                    <Icon Icon={Download1Solid} size={20} strokeWidth={2} className="text-white" />
                    IMPORT
                </span>
            </button>
        </aside>
    )
}