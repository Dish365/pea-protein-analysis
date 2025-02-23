import { 
  Home,
  DollarSign,
  Activity,
  Leaf,
  Book,
  MessageSquare,
  LucideIcon,
  LayoutDashboard,
  Plus
} from "lucide-react";

interface NavItem {
  title: string;
  href: string;
  icon: LucideIcon;
  color?: string;
  variant?: "default" | "ghost" | "outline";
}

interface NavSection {
  title: string;
  items: NavItem[];
}

export const navigationConfig: NavSection[] = [
  {
    title: "Home",
    items: [
      {
        title: "Home",
        href: "/",
        icon: Home
      },
    ]
  },
  {
    title: "Analysis",
    items: [
      {
        title: "Economic Analysis",
        href: "/dashboard/economic_analysis",
        icon: DollarSign,
        color: "text-green-500"
      },
      {
        title: "Technical Analysis",
        href: "/dashboard/technical_analysis",
        icon: Activity,
        color: "text-blue-500"
      },
      {
        title: "Environmental Analysis",
        href: "/dashboard/environmental_analysis",
        icon: Leaf,
        color: "text-emerald-500"
      }
    ]
  },
  {
    title: "Resources",
    items: [
      {
        title: "Documentation",
        href: "/documentation",
        icon: Book
      },
      {
        title: "Contact Support",
        href: "/contact",
        icon: MessageSquare
      }
    ]
  }
]; 