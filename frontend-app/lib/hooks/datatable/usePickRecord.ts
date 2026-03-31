import { useState, useRef, useCallback } from "react";
import { BaseEntity, GenericResponseAPI } from "@/lib/types/base";

interface UsePickRecordProps<T> {
    pickedRecord: T | null;
    pickedId: string | null;
    pickRecordById: (id: string | null) => void;
    pickedIsLoading: boolean;
    fetchRecord: () => Promise<void>;
    setPickedRecord: (record: T | null) => void;
}

interface UsePickRecordParams<T> {
    getRecordById: (id: string) => Promise<GenericResponseAPI<T>>;
}

export function usePickRecord<T extends BaseEntity>(
    { getRecordById }: UsePickRecordParams<T>
): UsePickRecordProps<T> {

    const [pickedIsLoading, setPickedIsLoading] = useState<boolean>(false);
    const [pickedRecord, setPickedRecord] = useState<T | null>(null);
    const [pickedId, setPickedId] = useState<string | null>(null);
    const pickedRecordIdRef = useRef<string | undefined>(undefined);

    const fetchRecord = useCallback(
        async () => {
        if (!pickedRecordIdRef.current) {
            setPickedRecord(null);
            return;
        };

        setPickedIsLoading(true);
        try {
            const response = await getRecordById(`${pickedRecordIdRef.current}`);
            console.log('@RECORD : ', response);
            if (response.status_code === 201) {
                setPickedRecord(response.data as T);
                setPickedId((response.data as T)?.id ?? null);
                pickedRecordIdRef.current = (response.data as T)?.id ?? null;
            }
        } catch (error) {
            console.log('@ERROR', error);
            setPickedRecord(null);
            setPickedId(null);
            setPickedIsLoading(false);
            pickedRecordIdRef.current = undefined;
        } finally {
            setPickedIsLoading(false);
        }
    }, [getRecordById, pickedRecordIdRef]);

    return {
        pickedRecord, 
        pickedId,
        pickRecordById: (pickedId: string | null) => { 
            pickedRecordIdRef.current = pickedId ?? undefined;  
            fetchRecord();
        },
        pickedIsLoading,
        fetchRecord,
        setPickedRecord
    };
}