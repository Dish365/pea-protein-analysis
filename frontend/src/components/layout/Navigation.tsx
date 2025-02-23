"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { navigationConfig } from "@/config/navigation";
import { ChevronDown } from "lucide-react";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";

interface NavigationProps {
  className?: string;
}

export function Navigation({ className }: NavigationProps) {
  const pathname = usePathname();
  const [openSections, setOpenSections] = React.useState<Record<string, boolean>>({
    Analysis: true
  });

  const toggleSection = (section: string) => {
    setOpenSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  return (
    <nav className={cn("py-4", className)}>
      <div className="px-3 py-2 space-y-6">
        {navigationConfig.map((section) => (
          <div key={section.title} className="space-y-2">
            {section.items.length > 1 ? (
              <Collapsible
                open={openSections[section.title]}
                onOpenChange={() => toggleSection(section.title)}
              >
                <CollapsibleTrigger asChild>
                  <Button
                    variant="ghost"
                    className="w-full justify-between hover:bg-muted"
                  >
                    <span className="text-sm font-medium text-muted-foreground">
                      {section.title}
                    </span>
                    <ChevronDown className={cn(
                      "h-4 w-4 text-muted-foreground transition-transform",
                      openSections[section.title] && "transform rotate-180"
                    )} />
                  </Button>
                </CollapsibleTrigger>
                <CollapsibleContent className="space-y-1">
                  {section.items.map((item) => {
                    const isActive = pathname === item.href;
                    return (
                      <Link key={item.href} href={item.href}>
                        <Button
                          variant={item.variant || (isActive ? "secondary" : "ghost")}
                          className={cn(
                            "w-full justify-start gap-3",
                            isActive && !item.variant && "bg-primary/10 hover:bg-primary/20"
                          )}
                        >
                          <item.icon className={cn(
                            "h-4 w-4",
                            item.color || (isActive ? "text-primary" : "text-muted-foreground")
                          )} />
                          <span className={cn(
                            "text-sm font-medium",
                            isActive && !item.variant && "text-primary"
                          )}>
                            {item.title}
                          </span>
                        </Button>
                      </Link>
                    );
                  })}
                </CollapsibleContent>
              </Collapsible>
            ) : (
              section.items.map((item) => {
                const isActive = pathname === item.href;
                return (
                  <Link key={item.href} href={item.href}>
                    <Button
                      variant={item.variant || (isActive ? "secondary" : "ghost")}
                      className={cn(
                        "w-full justify-start gap-3",
                        isActive && !item.variant && "bg-primary/10 hover:bg-primary/20"
                      )}
                    >
                      <item.icon className={cn(
                        "h-4 w-4",
                        item.color || (isActive ? "text-primary" : "text-muted-foreground")
                      )} />
                      <span className={cn(
                        "text-sm font-medium",
                        isActive && !item.variant && "text-primary"
                      )}>
                        {item.title}
                      </span>
                    </Button>
                  </Link>
                );
              })
            )}
          </div>
        ))}
      </div>
    </nav>
  );
}
