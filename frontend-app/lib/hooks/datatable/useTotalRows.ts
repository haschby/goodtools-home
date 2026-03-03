import { useState, useEffect } from "react";
import { BaseResponse } from "@/lib/types/base";

interface UseTotalRowsProps {
    fetchFunction: ({ entity }: { entity: string }) => Promise<BaseResponse<unknown>>;
    entity: string;
}

export function useTotalRows(
    { fetchFunction, entity }: UseTotalRowsProps
) {
    const [totalRows, setTotalRows] = useState<number>(0);
    

    useEffect(
        () => {
            let isMounted = true;
            async function getTotalRows() {
                const response = await fetchFunction({ entity });
                if (isMounted) {
                    if (typeof response?.data === 'number') {
                        setTotalRows(response?.data);
                    } else {
                        setTotalRows(0);
                    }
                }
            }
            getTotalRows();
            
            return () => {
                isMounted = false;
            }
        }, [fetchFunction, entity]);
    
    return totalRows;
}