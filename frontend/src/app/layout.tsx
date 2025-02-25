"use client";

import "@/app/globals.css"
import { Inter as FontSans } from "next/font/google"
import { cn } from "@/lib/utils"
import { Providers } from "@/components/providers/index"
import { MotionDiv } from "@/components/motion"

const fontSans = FontSans({
  subsets: ["latin"],
  variable: "--font-sans",
})

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <link rel="icon" href="/favicon.ico" />
      </head>
      <body 
        className={cn(
          "min-h-screen bg-background font-sans antialiased overflow-x-hidden",
          fontSans.variable
        )}
      >
        <Providers>
          {/* Background Effects */}
          <div className="fixed inset-0 bg-grid-black/[0.02] -z-10" />
          <div className="fixed inset-0 bg-gradient-to-br from-blue-50/50 via-background to-emerald-50/50 dark:from-blue-950/20 dark:via-background dark:to-emerald-950/20 -z-10" />
          
          {/* Animated Background Orbs */}
          <MotionDiv
            className="fixed top-1/4 right-1/4 w-[500px] h-[500px] bg-blue-500/10 rounded-full blur-3xl"
            animate={{
              scale: [1, 1.2, 1],
              opacity: [0.2, 0.3, 0.2],
              x: [0, 50, 0],
              y: [0, 30, 0],
            }}
            transition={{
              duration: 15,
              repeat: Infinity,
              ease: "easeInOut"
            }}
          />
          <MotionDiv
            className="fixed bottom-1/4 left-1/4 w-[500px] h-[500px] bg-emerald-500/10 rounded-full blur-3xl"
            animate={{
              scale: [1.2, 1, 1.2],
              opacity: [0.2, 0.3, 0.2],
              x: [0, -50, 0],
              y: [0, -30, 0],
            }}
            transition={{
              duration: 15,
              repeat: Infinity,
              ease: "easeInOut",
              delay: 2
            }}
          />
          <MotionDiv
            className="fixed top-1/2 left-1/2 w-[500px] h-[500px] bg-purple-500/10 rounded-full blur-3xl"
            animate={{
              scale: [1.1, 0.9, 1.1],
              opacity: [0.2, 0.3, 0.2],
              x: [-50, 50, -50],
              y: [-30, 30, -30],
            }}
            transition={{
              duration: 20,
              repeat: Infinity,
              ease: "easeInOut",
              delay: 4
            }}
          />

          <main className="relative flex min-h-screen flex-col">
            {children}
          </main>
        </Providers>
      </body>
    </html>
  )
}
