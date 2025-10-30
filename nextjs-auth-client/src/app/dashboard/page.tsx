"use client";

import { signOut } from "next-auth/react";

export default function Dashboard() {
  const handleLogout = () => {
    signOut();
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      <div className="w-full max-w-md p-8 bg-white dark:bg-zinc-900 rounded-lg shadow-md">
        <h1 className="text-2xl font-semibold text-center text-black dark:text-zinc-50 mb-6">
          Dashboard
        </h1>
        <p className="text-center text-zinc-700 dark:text-zinc-300 mb-6">
          Welcome to your dashboard! You are authenticated.
        </p>
        <button
          onClick={handleLogout}
          className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
        >
          Logout
        </button>
      </div>
    </div>
  );
}
