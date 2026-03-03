import { useState, useRef, useCallback } from "react";
import { BaseResponse, BaseEntity } from "@/lib/types/base";

interface UsePickRecordProps<T> {
    pickedRecord: T | null;
    pickedId: string | null;
    pickRecordById: (id: string | null) => void;
    isLoading: boolean;
    fetchRecord: () => Promise<void>;
    setPickedRecord: (record: T | null) => void;
}

interface UsePickRecordParams<T> {
    getRecordById: (id: string) => Promise<BaseResponse<T>>;
}

export function usePickRecord<T extends BaseEntity>(
    { getRecordById }: UsePickRecordParams<T>
): UsePickRecordProps<T> {

    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [pickedRecord, setPickedRecord] = useState<T | null>(null);
    const [pickedId, setPickedId] = useState<string | null>(null);
    const pickedRecordIdRef = useRef<string | undefined>(undefined);

    const fetchRecord = useCallback(
        async () => {
        if (!pickedRecordIdRef.current) {
            setPickedRecord(null);
            return;
        };

        setIsLoading(true);
        try {
            const { data: record } = await getRecordById(`${pickedRecordIdRef.current}`);
            if (record) {
                setPickedRecord(record as T);
                setPickedId(record.id);
                pickedRecordIdRef.current = record.id;
            }
        } catch (error) {
            console.log('@ERROR', error);
            setPickedRecord(null);
            setPickedId(null);
            pickedRecordIdRef.current = undefined;
        } finally {
            setIsLoading(false);
        }
    }, [getRecordById, pickedRecordIdRef]);

//    useEffect(
//     () => {
//         let isMounted = true;
//         if (isMounted) {
//             fetchRecord();
//         }
//         return () => {
//             isMounted = false;
//         };

//     }, [pickedId, fetchRecord]);

    

    return {
        pickedRecord, 
        pickedId,
        pickRecordById: (pickedId: string | null) => { 
            console.log('@PICKEDRECORDID :', pickedId);
            pickedRecordIdRef.current = pickedId ?? undefined;
            console.log('@PICKEDRECORDID REF :', pickedRecordIdRef.current);
            fetchRecord();
        },
        isLoading,
        fetchRecord,
        setPickedRecord
    };
}