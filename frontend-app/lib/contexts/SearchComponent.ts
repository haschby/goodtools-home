import { createContext, useContext } from "react";
import { SelectedFilters } from "@/lib/types/common";

interface SearchComponentContextType {
    isOpenFilters: boolean;
    setIsOpenFilters: (isOpen: boolean) => void;
    selectedFilters: SelectedFilters;
    setSelectedFilter: (filter: SelectedFilters) => void;
    queryText: string;
    setQueryText: (query: string) => void;
    debouncedValue: string;
}

const SearchComponentCTX = createContext<SearchComponentContextType | null>(null);

function useSearchComponent() {
    const context = useContext(SearchComponentCTX);
    if (!context) {
        throw new Error('useSearchComponent must be used within a SearchComponentProvider');
    }
    return context;
}

export { useSearchComponent, SearchComponentCTX, type SearchComponentContextType };