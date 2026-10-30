import { NextRequest, NextResponse } from "next/server";

export function middleware(request: NextRequest) {
  const token = process.env.NEUROSIM_AUTH_TOKEN;
  if (!token) return NextResponse.next();
  const headers = new Headers(request.headers);
  headers.set("authorization", `Bearer ${token}`);
  return NextResponse.next({ request: { headers } });
}

export const config = { matcher: "/api/:path*" };
