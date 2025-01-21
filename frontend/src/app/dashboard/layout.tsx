import React from "react";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="min-h-screen flex flex-col">
          <header className="border-b">
            <nav className="container mx-auto px-4 py-4">
              {/* Navigation will go here */}
            </nav>
          </header>
          <main className="flex-1 container mx-auto px-4 py-8">{children}</main>
          <footer className="border-t">
            <div className="container mx-auto px-4 py-4">
              {/* Footer content */}
            </div>
          </footer>
        </div>
      </body>
    </html>
  );
}
