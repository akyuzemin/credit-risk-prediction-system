import { Brain, ShieldCheck, Gauge, Activity } from "lucide-react";
import type { DashboardSummary } from "@/lib/api";

interface KpiCardsProps {
  summary: DashboardSummary | null;
}

function formatMetric(value?: number, digits = 3) {
  if (value === undefined || value === null || Number.isNaN(value)) return "-";
  return Number(value).toFixed(digits);
}

export function KpiCards({ summary }: KpiCardsProps) {
  const items = [
    {
      title: "Active Model",
      value: summary?.available_model ?? "-",
      icon: Brain,
      helper: "Selected best-performing model",
    },
    {
      title: "Threshold",
      value:
        summary?.threshold !== undefined ? Number(summary.threshold).toFixed(2) : "-",
      icon: ShieldCheck,
      helper: "Decision cut-off",
    },
    {
      title: "ROC-AUC",
      value: formatMetric(summary?.latest_metrics?.roc_auc),
      icon: Gauge,
      helper: "Discrimination performance",
    },
    {
      title: "F1 Score",
      value: formatMetric(summary?.latest_metrics?.f1_score),
      icon: Activity,
      helper: "Balanced classification quality",
    },
  ];

  return (
    <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
      {items.map((item) => {
        const Icon = item.icon;

        return (
          <div
            key={item.title}
            className="glass-card rounded-xl border border-border/60 p-5"
          >
            <div className="mb-4 flex items-center justify-between">
              <p className="text-xs uppercase tracking-[0.18em] text-muted-foreground">
                {item.title}
              </p>
              <div className="rounded-lg bg-secondary p-2 text-primary">
                <Icon className="h-4 w-4" />
              </div>
            </div>

            <div className="text-2xl font-semibold tracking-tight">
              {item.value}
            </div>

            <p className="mt-2 text-xs text-muted-foreground">{item.helper}</p>
          </div>
        );
      })}
    </div>
  );
}