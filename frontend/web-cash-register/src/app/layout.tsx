import type { Metadata } from "next";
import QueryProvider from "@/lib/queryClient";
import "./globals.css";
import Link from "next/link";


export const metadata: Metadata = {
  title: "Cash register",
  description: "Generated by create next app"
};

export default function RootLayout({
                                     children
                                   }: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
    <QueryProvider>
      <body className={"mt-24"}>
      <nav className="navbar fixed top-0 left-0 w-full navbar-expand-lg navbar-dark bg-gray-100 p-4 z-10">
        <div className="flex flex-wrap items-center text-l text-gray-600">
          <div className={"flex flex-wrap items-center space-x-8"}>
            <span className={"text-xl text-black px-10"}>Admin</span>
            <Link className={"hover:text-black"} href="/">Produkty</Link>
            <Link className={"hover:text-black"} href="/add-product">Dodaj produkt</Link>
            <Link className={"hover:text-black"} href="/storage">Magazyn</Link>
            <Link className={"hover:text-black"} href="/purchase-history">Historia zakupów</Link>
          </div>
        </div>
      </nav>
      {children}
      </body>
    </QueryProvider>
    </html>
  );
}
