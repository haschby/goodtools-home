import { useCallback, useState } from "react";
import { BaseEntity, GenericResponseAPI } from "@/lib/types/base";

interface UseRefreshRecordParams<T> {
    pickedId: string | null;
    refreshRecord: (id: string) => Promise<GenericResponseAPI<T>>;
    setPickedRecord: (record: T | null) => void;
}

interface UseRefreshRecordResponse {
    isLoading: boolean;
    refreshData: () => Promise<void>;
}

export function useRefreshRecord<T extends BaseEntity>(
    { pickedId, refreshRecord, setPickedRecord }: UseRefreshRecordParams<T>
): UseRefreshRecordResponse {
    const [isLoading, setIsLoading] = useState<boolean>(false);

    const refreshData = useCallback(async () => {
        if (!pickedId) {
            return;
        }

        setIsLoading(true);
        try {
            const response = await refreshRecord(`${pickedId}`);
            if (response.status_code === 200 || response.status_code === 201) {
                setPickedRecord((response.data as T) ?? null);
            }
        } catch (error) {
            console.error('@REFRESH RECORD ERROR : ', error);
        } finally {
            setIsLoading(false);
        }
    }, [pickedId, refreshRecord, setPickedRecord]);

    return {
        isLoading,
        refreshData,
    };
}
