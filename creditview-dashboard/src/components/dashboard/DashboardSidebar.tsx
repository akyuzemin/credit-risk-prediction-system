import { LayoutDashboard, UserCheck, BarChart3, Shield } from "lucide-react";

const navItems = [
  { icon: LayoutDashboard, label: "Dashboard", href: "#dashboard" },
  { icon: UserCheck, label: "Overview", href: "#overview" },
  { icon: BarChart3, label: "Scoring", href: "#scoring" },
  { icon: Shield, label: "Metrics", href: "#metrics" },
];

export function DashboardSidebar() {
  return (
    <aside className="min-h-screen w-64 border-r border-sidebar-border bg-sidebar flex flex-col">
      <div className="border-b border-sidebar-border p-6">
        <h1 className="gradient-text font-display text-xl font-bold">CreditLens</h1>
        <p className="mt-1 text-xs text-sidebar-foreground">
          Risk Intelligence Platform
        </p>
      </div>

      <nav className="flex-1 space-y-1 p-4">
        {navItems.map((item) => (
          <a
            key={item.label}
            href={item.href}
            className="flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium text-sidebar-foreground transition-colors hover:bg-sidebar-accent hover:text-sidebar-accent-foreground"
          >
            <item.icon className="h-4 w-4" />
            <span>{item.label}</span>
          </a>
        ))}
      </nav>

      <div className="border-t border-sidebar-border p-4">
        <div className="glass-card rounded-lg p-3">
          <p className="text-xs text-muted-foreground">Model Version</p>
          <p className="text-sm font-mono text-foreground">v2.4.1</p>
        </div>
      </div>
    </aside>
  );
}