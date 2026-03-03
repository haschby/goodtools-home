"use client";
import { useRef, useState } from "react";

interface PriceRange {
    min: number;
    max: number;
}

interface RangeSliderProps {
    min: number;
    max: number;
    dbMax: number;
    onChangePriceRange?: (range: PriceRange) => void;
}

export default function RangeSlider(
    { 
        min = 0, 
        max = 0, 
        dbMax, 
        onChangePriceRange
    }: RangeSliderProps
) {

    const sliderRef = useRef<HTMLDivElement>(null);
    const draggingRef = useRef<"left" | "right" | null>(null);

    const [range, setRange] = useState<PriceRange>({ min, max });
    const rangeRef = useRef<PriceRange>(range);

    const valueToPercent = (v: number) => (v / dbMax) * 100;
    const percentToValue = (p: number) => Math.round((p / 100) * dbMax);

    const onPointerMove = (e: PointerEvent) => {
        if (!draggingRef.current || !sliderRef.current) return;

        const rect = sliderRef.current.getBoundingClientRect();
        let percent = ((e.clientX - rect.left) / rect.width) * 100;
        percent = Math.max(0, Math.min(100, percent));

        const value = percentToValue(percent);


        const newMin = Math.min(value, rangeRef.current.max);
        const newMax = Math.max(value, rangeRef.current.min);

        setRange((prev) => {
            const newRange = draggingRef.current === "left"
            ? { min: newMin, max: prev.max }
            : { min: prev.min, max: newMax };
            rangeRef.current = newRange;
            return newRange;
        });
    };

    const stopDrag = () => {
        draggingRef.current = null;
        document.removeEventListener("pointermove", onPointerMove);
        document.removeEventListener("pointerup", stopDrag);
        const { min:minRef, max: maxRef } = rangeRef.current;
        const { min: min, max: max } = range;

        if (minRef === min && maxRef === max) {
            return;
        }

        handleSendEventChangeValue();
    };

    const startDrag = (side: "left" | "right") => () => {
        draggingRef.current = side;
        document.addEventListener("pointermove", onPointerMove);
        document.addEventListener("pointerup", stopDrag);
    };

    const onchangeValue = (side: "min" | "max") => (e: React.ChangeEvent<HTMLInputElement>) => {
        let value = Number(e.target.value);
        if (isNaN(value)) return;

        if (side === "max" && value > dbMax) value = dbMax;

        if (side === "min") {
            if (value > rangeRef.current.max) {
                setRange((prev) => ({ ...prev, min: rangeRef.current.max }));
                return;
            }
            rangeRef.current.min = value;
            setRange((prev) => ({ ...prev, min: value }));
        } else {
            if (value < rangeRef.current.min && value <= dbMax) {
                setRange((prev) => ({ ...prev, max: rangeRef.current.min }));
                return;
            }
            rangeRef.current.max = value;
            setRange((prev) => ({ ...prev, max: value }));
        }
        handleSendEventChangeValue();
    };

    const handleSendEventChangeValue = () => {
        onChangePriceRange?.(rangeRef.current);
    };

    return (
        <div className="w-full">
            <div ref={sliderRef} className="relative w-full h-2 bg-gray-200 rounded-full">
                <div
                className="absolute h-full bg-purple-500 rounded-full"
                style={{
                    left: `${valueToPercent(range.min)}%`,
                    width: `${valueToPercent(range.max) - valueToPercent(range.min)}%`,
                }}
                />

                <div
                onPointerDown={startDrag("left")}
                className="absolute top-1/2 -translate-y-1/2 w-5 h-5 bg-white border border-gray-300 rounded-full shadow cursor-pointer"
                style={{ left: `calc(${valueToPercent(range.min)}% - 10px)` }}
                />

                <div
                onPointerDown={startDrag("right")}
                className="absolute top-1/2 -translate-y-1/2 w-5 h-5 bg-white border border-gray-300 rounded-full shadow cursor-pointer"
                style={{ left: `calc(${valueToPercent(range.max)}% - 10px)` }}
                />
            </div>

            <div className="flex items-center justify-between gap-2 mt-4 text-sm font-semibold">
                <div className="flex items-center gap-2 border border-gray-300 rounded-md p-2">
                    <span>Min:</span>
                    <input
                        className="max-w-16 focus:outline-none active:outline-none text-right w-auto"
                        type="text"
                        value={range.min}
                        onChange={onchangeValue("min")} />
                        €
                    </div>
                <div className="flex items-center gap-2 border border-gray-300 rounded-md p-2">
                    <span>Max:</span>
                    <input
                        className="max-w-16 focus:outline-none active:outline-none text-right w-auto"
                        type="text"
                        value={range.max}
                        onChange={onchangeValue("max")} />
                        €
                    </div>
            </div>
        </div>
    );
}
