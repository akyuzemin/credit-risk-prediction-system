import type { DashboardSummary } from "@/lib/api";

interface ModelMetricsProps {
  summary: DashboardSummary | null;
  loading: boolean;
}

const metricConfig = [
  { key: "model_accuracy" as const, label: "Accuracy" },
  { key: "model_precision" as const, label: "Precision" },
  { key: "model_recall" as const, label: "Recall" },
  { key: "model_f1" as const, label: "F1 Score" },
  { key: "model_auc" as const, label: "AUC-ROC" },
];

export function ModelMetrics({ summary, loading }: ModelMetricsProps) {
  return (
    <div className="glass-card rounded-xl p-6">
      <h2 className="text-lg font-semibold mb-1">Model Performance</h2>
      <p className="text-xs text-muted-foreground mb-5">Current production model metrics</p>

      <div className="space-y-4">
        {metricConfig.map((m) => {
          const value = summary?.[m.key];
          return (
            <div key={m.key} className="space-y-1.5">
              <div className="flex justify-between text-sm">
                <span className="text-secondary-foreground">{m.label}</span>
                {loading ? (
                  <span className="h-4 w-12 rounded bg-muted animate-pulse inline-block" />
                ) : (
                  <span className="font-mono text-foreground">
                    {value !== undefined ? (value * 100).toFixed(1) + "%" : "—"}
                  </span>
                )}
              </div>
              <div className="h-2 rounded-full bg-secondary overflow-hidden">
                {loading ? (
                  <div className="h-full w-0 rounded-full bg-primary" />
                ) : (
                  <div
                    className="h-full rounded-full bg-primary transition-all duration-700"
                    style={{ width: `${(value ?? 0) * 100}%` }}
                  />
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
