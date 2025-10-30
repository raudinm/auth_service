import NextAuth from "next-auth";
import { NextAuthOptions } from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";
import GoogleProvider from "next-auth/providers/google";
import axios from "axios";

const BACKEND_URL =
  process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

export const authOptions: NextAuthOptions = {
  providers: [
    CredentialsProvider({
      name: "credentials",
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" },
        name: { label: "Name", type: "text" },
        device_name: { label: "Device Name", type: "text" },
        action: { label: "Action", type: "text" },
      },
      async authorize(credentials: any) {
        try {
          let response;
          if (credentials.action === "register") {
            response = await axios.post(`${BACKEND_URL}/api/auth/register`, {
              email: credentials.email,
              password: credentials.password,
              name: credentials.name,
              device_name: credentials.device_name || "NextAuth Client",
            });
          } else {
            response = await axios.post(`${BACKEND_URL}/api/auth/login`, {
              email: credentials.email,
              password: credentials.password,
              device_name: credentials.device_name || "NextAuth Client",
            });

            console.log(response.data);
          }

          const { access, refresh, user, session_id } = response.data;

          if (user) {
            return {
              id: user.id,
              session_id: session_id,
              email: user.email,
              name: user.name,
              avatar: user.avatar,
              accessToken: access,
              refreshToken: refresh,
            };
          }

          return null;
        } catch (error) {
          console.error("Auth error:", error);
          return null;
        }
      },
    }),
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
      authorization: {
        params: {
          prompt: "consent",
          access_type: "offline",
          response_type: "code",
        },
      },
    }),
  ],
  callbacks: {
    async signIn({ user, account, profile, email, credentials }) {
      // console.log("signIn", user, account, profile, email, credentials);
      return true;
    },
    async jwt({ token, user, account }: any) {
      if (user) {
        token.accessToken = user.accessToken;
        token.refreshToken = user.refreshToken;
        token.user = {
          id: user.id,
          email: user.email,
          name: user.name,
          avatar: user.avatar,
        };
      }

      // Handle Google OAuth
      if (account?.provider === "google") {
        try {
          const response = await axios.post(`${BACKEND_URL}/api/auth/google`, {
            access_token: account.access_token,
          });

          console.log("Google OAuth response:", response.data);

          const { access, refresh, user: backendUser } = response.data;

          token.accessToken = access;
          token.refreshToken = refresh;
          token.user = {
            id: backendUser.id,
            email: backendUser.email,
            name: backendUser.name,
            avatar: backendUser.avatar,
          };
        } catch (error) {
          console.error("Google OAuth error:", error);
          return null;
        }
      }

      return token;
    },
    async session({ session, token }: any) {
      session.accessToken = token.accessToken;
      session.refreshToken = token.refreshToken;
      session.user = token.user || session.user;
      return session;
    },
  },
  pages: {
    signIn: "/sign-in",
    error: "/sign-in",
  },
  session: {
    strategy: "jwt",
  },
  secret: process.env.NEXTAUTH_SECRET,
};
