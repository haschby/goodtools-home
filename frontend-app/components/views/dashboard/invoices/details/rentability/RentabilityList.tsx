"use client";

import { Rentability } from "@/actions/invoice.actions";
import RentabilityRow from "./rows/RentabilityRow";

interface RentabilityListProps {
    rentabilities: Rentability[] | null;
}

export default function RentabilityList({ rentabilities }: RentabilityListProps) {
    if (!rentabilities || rentabilities.length === 0) {
        return (
            <div className="flex h-24 items-center justify-center text-sm text-gray-400">
                Aucune rentabilité à afficher
            </div>
        );
    }

    return (
        <div className="flex flex-col gap-2">
            {rentabilities.map((rentability, index) => (
                <RentabilityRow key={`rentability-${rentability.id}-${index}`} rentability={rentability} />
            ))}
        </div>
    );
}
