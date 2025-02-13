"use client";

import React from 'react';
import Link from 'next/link';
import { ArrowRight } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface CTAButtonsProps {
  variant?: 'default' | 'secondary';
}

export function CTAButtons({ variant = 'default' }: CTAButtonsProps) {
  return (
    <div className="flex flex-wrap justify-center gap-4">
      <Link href="/dashboard/analysis">
        <Button size="lg" variant={variant} className="gap-2">
          Start Analysis <ArrowRight className="h-4 w-4" />
        </Button>
      </Link>
      <Link href="/dashboard">
        <Button variant={variant === 'default' ? 'outline' : 'default'} size="lg">
          View Dashboard
        </Button>
      </Link>
    </div>
  );
} 