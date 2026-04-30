import { NextRequest, NextResponse } from "next/server";

export default function middleware(request: NextRequest) {
    const token = request.cookies.get('token');

    if (token) {
        return NextResponse.redirect(new URL('/signin', request.url));
    }

    // return NextResponse.redirect(new URL('/signin', request.url));
    return NextResponse.next();
}

export const config = {
    matcher: [
      '/invoices/:path*',
      '/purchases/:path*',
      '/users/:path*',
      '/workflows/:path*',
    ],
}

// export const config = {
//     matcher: [
//         '/((?!api|_next/static|_next/image|favicon.ico).*)',
//     ],
// }