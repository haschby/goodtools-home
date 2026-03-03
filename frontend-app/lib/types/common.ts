import { ReactNode } from "react";

export interface PriceRange {
    min: number;
    max: number;
}

export interface SelectedFilters {
    price?: PriceRange;
}

export type ColumnProps<T> = {
    keyfield: string;
    align: 'left' | 'right';
    maxWidth?: string;
    isFirst?: boolean;
    isLast?: boolean;
    isNumber?: boolean;
    renderItem: (item: T) => ReactNode;
}

