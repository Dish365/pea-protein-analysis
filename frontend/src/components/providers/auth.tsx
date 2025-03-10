"use client";

import { createContext, useContext, useState } from "react";
import { User } from "@/types/user";
import { useAuth, UseAuth } from "@/hooks/useAuth";

const AuthContext = createContext<UseAuth | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const auth = useAuth();
  return <AuthContext.Provider value={auth}>{children}</AuthContext.Provider>;
}

export const useAuthContext = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuthContext must be used within AuthProvider");
  return context;
}; 