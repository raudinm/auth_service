import { NextResponse, NextRequest } from "next/server";
import { getToken } from "next-auth/jwt";

export async function middleware(req: NextRequest) {
  const { pathname } = req.nextUrl;
  const token = await getToken({
    req,
    secret: process.env.NEXTAUTH_SECRET!,
  });

  const user = token?.user as any;

  if (!user && !pathname.includes("/sign-in") && !pathname.includes("/sign-up"))
    return NextResponse.redirect(new URL("/sign-in", req.url));

  return NextResponse.next();
}

export const config = {
  matcher: ["/sign-in", "/sign-up", "/dashboard"],
};
