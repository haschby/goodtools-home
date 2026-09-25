"use client";

import { useState, useRef, useLayoutEffect, useEffect } from "react";
import Icon from "@/components/atoms/Icon";
import { CalendarDaysSolid, Gear1Solid, Locked1Solid, Spinner3Solid, Telephone3Solid } from "@lineiconshq/free-icons";
import InvoiceRentability from "../../InvoiceRentability";
import RentabilityList from "../RentabilityList";
import { getRentabilitiesByBookingId, RentabilitiesResponse, updateBookingComment } from "@/actions/invoice.actions";
import { Invoice } from "@/lib/types/invoice";
import Link from "next/link";

interface RentabilitesTabProps {
    pickedRecord: Invoice | null;
}

export default function RentabilitesTab({
    pickedRecord,
}: RentabilitesTabProps) {

    const [comment, setComment] = useState<string>('');
    const [savedComment, setSavedComment] = useState<string>('');
    const [isSaving, setIsSaving] = useState<boolean>(false);
    const [isClosing, setIsClosing] = useState<boolean>(false);
    const [rentabilities, setRentabilities] = useState<RentabilitiesResponse | null>(null);
    const [isLoading, setIsLoading] = useState<boolean>(false);

    const listWrapperRef = useRef<HTMLElement>(null);
    const [listMaxHeight, setListMaxHeight] = useState<number>(0);

    useEffect(() => {
        const bookingId = pickedRecord?.gc_booking;

        let cancelled = false;
        (async () => {
            if (!bookingId) {
                if (!cancelled) {
                    setRentabilities(null);
                    setIsLoading(false);
                }
                return;
            }
            if (!cancelled) {
                setIsLoading(true);
            }
            try {
                const response = await getRentabilitiesByBookingId(Number(bookingId));
                if (!cancelled) {
                    setRentabilities(response);
                    setComment(response.comment ?? '');
                    setSavedComment(response.comment ?? '');
                }
            } catch (error) {
                console.error(error);
                if (!cancelled) {
                    setRentabilities(null);
                }
            } finally {
                if (!cancelled) {
                    setIsLoading(false);
                }
            }
        })();

        return () => { cancelled = true; };
    }, [pickedRecord?.gc_booking, setRentabilities]);

    useLayoutEffect(() => {
        const element = listWrapperRef.current;
        if (!element) return;

        const computeHeight = () => {
            const top = element.getBoundingClientRect().top;
            const availableHeight = window.innerHeight - top - 52;
            setListMaxHeight(Math.max(availableHeight, 0));
        };

        computeHeight();

        const resizeObserver = new ResizeObserver(() => computeHeight());
        resizeObserver.observe(document.body);

        return () => resizeObserver.disconnect();
    }, []);

    const handleSaveComment = async () => {
        const bookingId = pickedRecord?.gc_booking;
        if (!bookingId || isSaving) return;

        setIsSaving(true);
        try {
            const response = await updateBookingComment(Number(bookingId), comment);
            const nextComment = response.data?.comment ?? comment;
            setSavedComment(nextComment);
            setComment(nextComment);
            setRentabilities((prev) => (prev ? { ...prev, comment: nextComment } : prev));
        } catch (error) {
            console.error('Failed to save booking comment', error);
        } finally {
            setIsSaving(false);
        }
    }

    const isSaveEnabled = !isSaving && comment !== savedComment;

    const handleCloseBooking = async () => {
        const bookingId = pickedRecord?.gc_booking;
        if (!bookingId || isClosing) return;

        setIsClosing(true);
        try {
            // TODO: brancher sur l'API de clôture de booking une fois disponible
            // await closeBooking(Number(bookingId));
            console.log('Clôture du booking', bookingId);
        } catch (error) {
            console.error('Failed to close booking', error);
        } finally {
            setIsClosing(false);
        }
    }

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
                    <div className="flex flex-col gap-2 h-full">
                        <div className="flex flex-col rounded-xl bg-gray-50">
                            <div className="flex flex-row items-start justify-between gap-2 p-4">
                                <div className="flex flex-col items-start gap-1">
                                    <div className="flex flex-row items-center justify-between leading-tight gap-2">
                                        <span className="text-lg font-semibold">
                                            Booking 
                                        </span>
                                        <Link href={`https://goodcollect.co/admin-v2/bookings/${rentabilities?.bookingId}`}
                                        className="text-xs border border-orange-500 text-orange-500 bg-orange-100 p-1 rounded-md">
                                            #{rentabilities?.bookingId}
                                        </Link>
                                    </div>
                                    <span className="text-xs text-gray-500">
                                        {new Date(rentabilities?.eventStartDate ?? '').toLocaleDateString('fr-FR')}
                                        &nbsp;-&nbsp;
                                        {new Date(rentabilities?.eventEndDate ?? '').toLocaleDateString('fr-FR')}
                                    </span>
                                </div>
                                <button
                                    type="button"
                                    disabled={isClosing || !rentabilities?.bookingId}
                                    onClick={handleCloseBooking}
                                    className={`inline-flex items-center gap-2 text-sm font-semibold px-4 py-2 rounded-lg transition-all duration-300 transform ${isClosing || !rentabilities?.bookingId ? 'cursor-not-allowed bg-gray-100 text-gray-400' : 'cursor-pointer bg-green-200/50 border border-green-200 hover:bg-green-200 text-green-600'}`}>
                                    <Icon
                                        Icon={isClosing ? Spinner3Solid : Locked1Solid}
                                        size={16}
                                        strokeWidth={2}
                                        className={isClosing ? 'animate-spin duration-300' : ''} />
                                    {isClosing ? 'Clôture...' : 'Clôturer'}
                                </button>
                            </div>
                            <div className="flex flex-col gap-2 p-4 rounded-t-[25px] rounded-b-xl border border-gray-200 bg-white">
                                <div className="flex flex-row flex-wrap items-center gap-1 text-sm">
                                    <span className="text-xs inline-flex items-center gap-2 font-semibold border border-blue-200 bg-blue-100 text-blue-600 px-3 py-1.5 rounded-xl">
                                        
                                        {
                                            isLoading
                                            ? <Icon
                                                Icon={Spinner3Solid}
                                                size={16}
                                                strokeWidth={2}
                                                className="animate-spin duration-300 text-gray-600" />
                                            : 
                                            rentabilities?.isMonthly === undefined
                                            ? 'NA'
                                            : rentabilities?.isMonthly ? 'Récurrent' : 'Non récurrent'
                                        }
                                    </span>
                                    <span className="text-xs inline-flex items-center gap-2 font-semibold border border border-blue-200 bg-blue-100 text-blue-600 px-3 py-1.5 rounded-xl">

                                        {
                                            isLoading
                                            ? <Icon
                                                Icon={Spinner3Solid}
                                                size={16}
                                                strokeWidth={2}
                                                className="animate-spin duration-300 text-gray-600" />
                                            : 
                                            rentabilities?.isExternal === undefined
                                            ? 'NA'
                                            : rentabilities?.isExternal ? 'Externe' : 'Interne'
                                        }
                                    </span>
                                    <span className="text-xs inline-flex items-center gap-2 font-semibold border border border-blue-200 bg-blue-100 text-blue-600 px-3 py-1.5 rounded-xl">
                                        
                                        {
                                            isLoading
                                            ? <Icon
                                                Icon={Spinner3Solid}
                                                size={16}
                                                strokeWidth={2}
                                                className="animate-spin duration-300 text-gray-600" />
                                            : 
                                            rentabilities?.isManualInvoice === undefined
                                            ? 'NA'
                                            : rentabilities?.isManualInvoice ? 'Manuelle'
                                            : rentabilities?.isMonthly ? 'Mensuelle'
                                            : 'Auto'
                                        }
                                    </span>
                                </div>

                                <div className="flex flex-col rounded-xl border border-gray-200 bg-gray-100 text-gray-500 mt-2">
                                    <div className="flex flex-col gap-3 p-4">
                                        <label htmlFor="booking_comments" className="text-sm font-semibold text-gray-900">
                                            Commentaires
                                        </label>
                                        <textarea 
                                            id="booking_comments"
                                            name="booking_comments"
                                            rows={2}
                                            maxLength={12000}
                                            placeholder="Ajouter une note sur cette rentabilité..."
                                            className="w-full resize-none rounded-lg p-3 text-sm text-gray-900 bg-white placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-100 transition-all"
                                            value={comment}
                                            onChange={(e) => setComment(e.target.value)}
                                        />
                                    </div>
                                    <div className="flex flex-row justify-end border-t border-gray-200 p-2">
                                        <button
                                            disabled={!isSaveEnabled}
                                            onClick={handleSaveComment}
                                            className={`text-sm font-semibold px-6 py-2 rounded-lg transition-all duration-300 transform ${isSaveEnabled ? 'hover:scale-105 cursor-pointer bg-green-400 hover:bg-green-500 text-white' : 'cursor-not-allowed bg-gray-50 text-gray-400'}`}>
                                            {isSaving ? 'Enregistrement...' : 'Commenter'}
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div className="flex flex-col w-full mt-4 border border-gray-200 rounded-xl bg-white">
                            <InvoiceRentability
                                profit={rentabilities?.profit}
                                ca={rentabilities?.ca}
                                charges={rentabilities?.charges}
                                margin={rentabilities?.margin}
                            />
                            <div className="flex flex-col h-full pt-4 rounded-b-xl">
                                <h3 className="flex flex-row justify-between text-md font-semibold border-b border-gray-200 p-3">
                                    Details des lignes&nbsp;
                                    <span className="text-green-500 text-xs bg-green-100 px-2 py-1 rounded-md">
                                        {rentabilities?.items?.length ?? 0}&nbsp;lignes
                                    </span>                                               
                                </h3>
                                <aside
                                    ref={listWrapperRef}
                                    style={{ maxHeight: `${listMaxHeight}px` }}
                                    className="overflow-y-auto h-full bg-gray-50 rounded-b-xl">
                                    <RentabilityList bookingId={rentabilities?.bookingId?.toString() || ''} rentabilities={rentabilities?.items || []} />
                                </aside>
                            </div>
                        </div>
                    </div>
                )
            }
        </aside>
    );
}
