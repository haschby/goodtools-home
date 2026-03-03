"use client";

import { useRef, ChangeEvent } from "react";
import { useRouter } from "next/navigation";
import Icon from "@/components/atoms/Icon";
import { Cloud2Stroke } from "@lineiconshq/free-icons";
import { startWorkflow } from "@/actions/workflow";

export default function ImportInvoiceForm() {
    const inputRef = useRef<HTMLInputElement>(null);
    const router = useRouter();
    
    const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
        const files = event.target.files;
        if (!files) return;
        const newFormData = new FormData();
        for( let i = 0; i < files.length; i++ ) {
            newFormData.append("files", files[i]);
        }
    }

    const handleSync = async () => {
        const uniqueId = Math.random().toString(36).substring(2, 15);
        const provider = "pennylane";
        await startWorkflow({ provider, id: uniqueId, workflowName: 'syncPennyLaneWorkflow' });
        router.push(`/workflows/${provider}/sync/${uniqueId}`);
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
            {/* <button
                className="cursor-pointer py-2 px-2 bg-gray-200 shadow-md shadow-gray-200 rounded-sm"
                onClick={() => inputRef.current?.click()}>
                <span className="flex items-center gap-2 text-gray-500 text-md font-normal">
                    <Icon Icon={Download1Solid} size={16} strokeWidth={2} className="text-gray-500" />
                    import files
                </span>
            </button> */}

            <button
                className="bg-[#f9f8f0] border-2 border-amber-500 group cursor-pointer p-2 rounded-md text-amber-500"
                onClick={handleSync}>
                <span className="text-xs flex items-center gap-2 font-semibold">
                    <Icon
                        Icon={Cloud2Stroke}
                        size={16}
                        strokeWidth={3}
                        className="" />
                    Pennylane Sync
                </span>
            </button>
        </aside>
    )
}