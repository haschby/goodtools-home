"use client";

import { useState, useRef, useLayoutEffect } from "react";
import Icon from "@/components/atoms/Icon";
import { CalendarDaysSolid, Gear1Solid, Spinner3Solid, Telephone3Solid } from "@lineiconshq/free-icons";
import InvoiceRentability from "../../InvoiceRentability";
import RentabilityList from "../RentabilityList";
import { RentabilitiesResponse } from "@/actions/invoice.actions";
import { Invoice } from "@/lib/types/invoice";

interface RentabilitesTabProps {
    pickedRecord: Invoice | null;
    rentabilities: RentabilitiesResponse | null;
}

export default function RentabilitesTab({
    pickedRecord,
    rentabilities,
}: RentabilitesTabProps) {

    const initialComment = pickedRecord?.gc_booking ?? '';
    const [comment, setComment] = useState<string>(initialComment);

    const listWrapperRef = useRef<HTMLElement>(null);
    const [listMaxHeight, setListMaxHeight] = useState<number>(0);

    useLayoutEffect(() => {
        const element = listWrapperRef.current;
        if (!element) return;

        const computeHeight = () => {
            const top = element.getBoundingClientRect().top;
            const availableHeight = window.innerHeight - top - 16;
            setListMaxHeight(Math.max(availableHeight, 0));
        };

        computeHeight();

        const resizeObserver = new ResizeObserver(() => computeHeight());
        resizeObserver.observe(document.body);

        return () => resizeObserver.disconnect();
    }, []);

    const isSaveEnabled = comment.trim().length > 0 && comment !== initialComment;

    return (
        <aside className="h-full flex flex-col">
            {
                !pickedRecord?.gc_booking && (
                    <div className="p-5 bg-gray-50 border border-gray-100 rounded-md">
                        <span className="text-sm font-semibold text-gray-900">
                            {`Il n'y a pas de booking rattaché à cette facture.`}
                        </span>
                        <br />
                        <span className="text-sm text-gray-500">
                            {`Veuillez récupérer le booking ID et l'ajouter à la facture.`}
                        </span>
                    </div>
                ) || (
                    <div className="flex flex-col gap-2">
                        <div className="flex flex-col gap-2">
                            <div className="flex flex-col items-start justify-between gap-4">
                                {/* <h3 className="text-xl font-bold text-gray-900">
                                    Rentabilités Détails
                                </h3> */}
                                <div className="flex flex-row leading-tight gap-2">
                                    <span className="text-sm text-gray-400">
                                        Booking
                                    </span>
                                    <span className="text-md font-bold text-gray-900">
                                        #GC-{rentabilities?.bookingId}
                                    </span>
                                </div>
                            </div>

                            <div className="flex flex-row flex-wrap items-center gap-1 text-sm">
                                <span className="text-xs inline-flex items-center gap-2 font-semibold bg-purple-100 text-purple-500 px-3 py-1.5 rounded-full">
                                    <Icon Icon={CalendarDaysSolid} size={16} strokeWidth={2} />
                                    {
                                        rentabilities?.isMonthly === undefined
                                        ? <Icon
                                            Icon={Spinner3Solid}
                                            size={16}
                                            strokeWidth={2}
                                            className="animate-spin duration-300 text-gray-600" />
                                        : 
                                        rentabilities?.isMonthly ? 'Récurrent' : 'Non récurrent'
                                    }
                                </span>
                                <span className="text-xs inline-flex items-center gap-2 font-semibold bg-blue-100 text-blue-500 px-3 py-1.5 rounded-full">
                                    <Icon Icon={Gear1Solid} size={16} strokeWidth={2} />
                                    {
                                        rentabilities?.isExternal === undefined
                                        ? <Icon
                                            Icon={Spinner3Solid}
                                            size={16}
                                            strokeWidth={2}
                                            className="animate-spin duration-300 text-gray-600" />
                                        : 
                                        rentabilities?.isExternal ? 'Externe' : 'Interne'
                                    }
                                </span>
                                <span className="text-xs inline-flex items-center gap-2 font-semibold bg-green-100 text-green-500 px-3 py-1.5 rounded-full">
                                    <Icon Icon={Telephone3Solid} size={16} strokeWidth={2} />
                                    {
                                        rentabilities?.isManualInvoice === undefined
                                        ? <Icon
                                            Icon={Spinner3Solid}
                                            size={16}
                                            strokeWidth={2}
                                            className="animate-spin duration-300 text-gray-600" />
                                        : 
                                        rentabilities?.isManualInvoice ? 'Manuelle'
                                        : rentabilities?.isMonthly ? 'Mensuelle'
                                        : 'Auto'
                                    }
                                </span>
                            </div>

                            <div className="flex flex-col rounded-xl bg-gray-50 border border-gray-200 mt-2">
                                <div className="flex flex-col gap-3 p-4">
                                    <label htmlFor="booking_comments" className="text-sm font-semibold text-gray-900">
                                        Commentaires
                                    </label>
                                    <textarea 
                                        id="booking_comments"
                                        name="booking_comments"
                                        rows={2}
                                        placeholder="Ajouter une note sur cette rentabilité..."
                                        className="w-full resize-none rounded-lg p-3 text-sm text-gray-900 bg-white placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-100 transition-all"
                                        value={comment}
                                        onChange={(e) => setComment(e.target.value)}
                                    />
                                </div>
                                <div className="flex flex-row justify-end border-t border-gray-200 p-2">
                                    <button
                                        disabled={!isSaveEnabled}
                                        className={`text-sm font-semibold px-6 py-2 rounded-lg transition-colors ${isSaveEnabled ? 'cursor-pointer bg-slate-900 hover:bg-slate-800 text-white' : 'cursor-not-allowed bg-gray-200 text-gray-400'}`}>
                                        Commenter
                                    </button>
                                </div>
                            </div>
                        </div>

                        <div className="flex flex-col w-full mt-4">
                            <InvoiceRentability
                                profit={rentabilities?.profit}
                                ca={rentabilities?.ca}
                                charges={rentabilities?.charges}
                                margin={rentabilities?.margin}
                            />
                        </div>
                        <div className="flex flex-col gap-2 h-full p-3 bg-gray-50 mt-4">
                            {
                                rentabilities?.items
                                && rentabilities?.items.length > 0
                                ? (
                                    <h3 className="text-lg font-semibold">
                                        Rentabilités&nbsp;
                                        <span className="text-green-500 text-xs">
                                            {rentabilities?.items.length}&nbsp;lignes
                                        </span>                                               
                                    </h3>
                                ) : (
                                    <>
                                        <span className="text-sm text-gray-400"> 
                                            Aucune ligne de rentabilité à afficher
                                        </span>
                                    </>
                                )
                            }
                            <aside
                                ref={listWrapperRef}
                                style={{ maxHeight: `${listMaxHeight-30}px` }}
                                className="overflow-y-auto h-full">
                                <RentabilityList rentabilities={rentabilities?.items || []} />
                            </aside>
                        </div>
                    </div>
                )
            }
        </aside>
    );
}
