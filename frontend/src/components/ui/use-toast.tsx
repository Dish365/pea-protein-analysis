import { useState } from "react";

interface Toast {
  title?: string;
  description?: string;
  variant?: "default" | "destructive";
}

export function useToast() {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const toast = (props: Toast) => {
    setToasts([...toasts, props]);
  };

  return { toast, toasts };
} 