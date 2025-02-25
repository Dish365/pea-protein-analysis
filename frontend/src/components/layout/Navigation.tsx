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
import { MotionDiv } from "@/components/motion";

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
    <nav className={cn("py-4 relative", className)}>
      {/* Navigation Background Gradient */}
      <div className="absolute inset-0 bg-gradient-to-b from-background via-background to-muted/20" />
      
      <div className="px-3 py-2 space-y-6 relative">
        {navigationConfig.map((section, sectionIndex) => (
          <MotionDiv
            key={section.title}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.3, delay: sectionIndex * 0.1 }}
            className="space-y-2"
          >
            {section.items.length > 1 ? (
              <Collapsible
                open={openSections[section.title]}
                onOpenChange={() => toggleSection(section.title)}
              >
                <CollapsibleTrigger asChild>
                  <Button
                    variant="ghost"
                    className="w-full justify-between hover:bg-muted/80 group transition-all duration-200"
                  >
                    <span className="text-sm font-medium text-muted-foreground group-hover:text-foreground transition-colors">
                      {section.title}
                    </span>
                    <ChevronDown className={cn(
                      "h-4 w-4 text-muted-foreground transition-all duration-200 ease-in-out",
                      openSections[section.title] && "transform rotate-180"
                    )} />
                  </Button>
                </CollapsibleTrigger>
                <CollapsibleContent className="space-y-1">
                  {section.items.map((item, itemIndex) => {
                    const isActive = pathname === item.href;
                    return (
                      <MotionDiv
                        key={item.href}
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.2, delay: itemIndex * 0.1 }}
                      >
                        <Link href={item.href}>
                          <Button
                            variant={item.variant || (isActive ? "secondary" : "ghost")}
                            className={cn(
                              "w-full justify-start gap-3 relative overflow-hidden group",
                              isActive && !item.variant && "bg-primary/10 hover:bg-primary/20",
                              "transition-all duration-200"
                            )}
                          >
                            <item.icon className={cn(
                              "h-4 w-4 transition-transform duration-200 ease-out group-hover:scale-110",
                              item.color || (isActive ? "text-primary" : "text-muted-foreground")
                            )} />
                            <span className={cn(
                              "text-sm font-medium transition-colors",
                              isActive && !item.variant && "text-primary"
                            )}>
                              {item.title}
                            </span>
                            {isActive && (
                              <MotionDiv
                                layoutId="active-nav-item"
                                className="absolute inset-0 bg-primary/10 -z-10"
                                transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
                              />
                            )}
                          </Button>
                        </Link>
                      </MotionDiv>
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
                        "w-full justify-start gap-3 relative overflow-hidden group",
                        isActive && !item.variant && "bg-primary/10 hover:bg-primary/20",
                        "transition-all duration-200"
                      )}
                    >
                      <item.icon className={cn(
                        "h-4 w-4 transition-transform duration-200 ease-out group-hover:scale-110",
                        item.color || (isActive ? "text-primary" : "text-muted-foreground")
                      )} />
                      <span className={cn(
                        "text-sm font-medium transition-colors",
                        isActive && !item.variant && "text-primary"
                      )}>
                        {item.title}
                      </span>
                      {isActive && (
                        <MotionDiv
                          layoutId="active-nav-item"
                          className="absolute inset-0 bg-primary/10 -z-10"
                          transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
                        />
                      )}
                    </Button>
                  </Link>
                );
              })
            )}
          </MotionDiv>
        ))}
      </div>
    </nav>
  );
}
