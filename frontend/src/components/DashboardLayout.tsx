import Link from 'next/link'
import { usePathname } from 'next/navigation'

interface NavItem {
  icon: string
  label: string
  href: string
}

const navItems: NavItem[] = [
  { icon: '📊', label: 'Dashboard', href: '/dashboard' },
  { icon: '🔬', label: 'Analysis', href: '/dashboard/analysis' },
  { icon: '⚙️', label: 'Technical', href: '/dashboard/analysis/technical' },
  { icon: '💰', label: 'Economic', href: '/dashboard/analysis/economic' },
  { icon: '🌍', label: 'Environmental', href: '/dashboard/analysis/environmental' },
]

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const pathname = usePathname()

  return (
    <div className="min-h-screen flex">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r">
        <div className="p-4 border-b">
          <h1 className="text-xl font-bold text-blue-600">PEA Protein Analysis</h1>
        </div>
        <nav className="p-4">
          {navItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center p-2 rounded-lg mb-1 ${
                pathname === item.href
                  ? 'bg-blue-50 text-blue-600'
                  : 'text-gray-700 hover:bg-gray-50'
              }`}
            >
              <span className="mr-3">{item.icon}</span>
              {item.label}
            </Link>
          ))}
        </nav>
      </aside>

      {/* Main content */}
      <div className="flex-1">
        {/* Top navigation */}
        <header className="bg-white border-b">
          <div className="flex justify-between items-center px-6 py-3">
            <h2 className="text-xl font-semibold">Dashboard</h2>
            <div className="flex items-center space-x-4">
              <span>Welcome, Admin</span>
              <Link
                href="/signin"
                className="text-sm text-gray-700 hover:text-gray-900"
              >
                Sign out
              </Link>
            </div>
          </div>
        </header>

        {/* Page content */}
        <main className="p-6 bg-gray-50 min-h-[calc(100vh-64px)]">
          {children}
        </main>
      </div>
    </div>
  )
} 