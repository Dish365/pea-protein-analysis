"use client";

import "@/app/globals.css"
import { Inter } from "next/font/google"
import { cn } from "@/lib/utils"
import { Providers } from "@/components/providers/index"

const inter = Inter({ subsets: ["latin"] })

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={cn(inter.className, "min-h-screen bg-background antialiased")}>
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  )
}
