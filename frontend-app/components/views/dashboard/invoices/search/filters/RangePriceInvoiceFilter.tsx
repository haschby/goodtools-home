"use client";

import RangeSlider from "@/components/atoms/form/RangeSlider";
import { PriceRange } from "@/lib/types/common";
import { useQueryClient } from "@/lib/contexts/QueryClientContext";
import { useDebouncedCallback } from "@/lib/hooks/UseDebounceQueryText";

interface RangePriceInvoiceFilterProps {
    dbMax: number
}

export default function RangePriceInvoiceFilter(
    { dbMax }: RangePriceInvoiceFilterProps
) {

    const { setQueryParams } = useQueryClient();
  
    const priceRangeRef = [0, dbMax];
    const priceRange: PriceRange = { min: priceRangeRef[0], max: priceRangeRef[1] };

    const priceRangeCallback = (priceRange: PriceRange) => {
        const { min, max } = priceRange;
        if (min === 0 && max === dbMax) {
            setQueryParams("price", null);
        } else {
            setQueryParams("price", `${min}-${max}`);
        }
    }
  
    const handleChangePriceRange = useDebouncedCallback(priceRangeCallback, 600);
    
    return (
        <>
            <RangeSlider
                max={priceRange.max}
                min={priceRange.min}
                dbMax={dbMax}
                onChangePriceRange={
                    (priceRange: PriceRange) =>
                    handleChangePriceRange(priceRange)
                }
            />
        </>
    )
}