export const displayBookingRef = (booking: string): string | null => {
    const cleaned = booking.match(/\d+/g);
    if (cleaned?.[0]) {
        return `GC-${cleaned?.[0]}`;
    }
    return null;
}
