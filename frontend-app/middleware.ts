import { NextRequest, NextResponse } from "next/server";

export default function middleware(request: NextRequest) {
    const { pathname } = request.nextUrl;
    // if (pathname.startsWith('/signin')) {
    //     return NextResponse.next();
    // }

    if (pathname.startsWith('/signin')) {
        return NextResponse.next();
    }

    // return NextResponse.redirect(new URL('/signin', request.url));
    return NextResponse.next();
}

// export const config = {
//     matcher: [
//         '/((?!api|_next/static|_next/image|favicon.ico).*)',
//     ],
// }