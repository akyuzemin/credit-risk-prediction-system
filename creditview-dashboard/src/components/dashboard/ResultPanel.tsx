import { AlertTriangle, BadgeCheck, ShieldX } from "lucide-react";
import type { PredictResponse } from "@/lib/api";

interface ResultPanelProps {
  result: PredictResponse | null;
}

function getUiState(result: PredictResponse) {
  if (result.risk_level === "high") {
    return {
      title: "Uygun Değil",
      subtitle: "Mevcut bilgilere göre başvurunuz yüksek risk grubunda görünüyor.",
      badgeClass: "border-red-500/30 bg-red-500/15 text-red-300",
      icon: ShieldX,
    };
  }

  if (result.risk_level === "medium") {
    return {
      title: "Ek İnceleme Gerekli",
      subtitle: "Başvurunuz ek belge veya detaylı değerlendirme gerektirebilir.",
      badgeClass: "border-amber-500/30 bg-amber-500/15 text-amber-300",
      icon: AlertTriangle,
    };
  }

  return {
    title: "Uygun",
    subtitle: "Bilgilerinize göre başvurunuz ön değerlendirmede olumlu görünüyor.",
    badgeClass: "border-emerald-500/30 bg-emerald-500/15 text-emerald-300",
    icon: BadgeCheck,
  };
}

function getFriendlyRiskLabel(level: string) {
  if (level === "high") return "Yüksek";
  if (level === "medium") return "Orta";
  return "Düşük";
}

function getFriendlyFeatureName(feature: string) {
  const labels: Record<string, string> = {
    checking_status: "Hesap durumu",
    duration_months: "Vade",
    credit_history: "Kredi geçmişi",
    purpose: "Kredi amacı",
    credit_amount: "Kredi tutarı",
    savings_status: "Birikim durumu",
    employment_since: "Çalışma süresi",
    installment_rate: "Taksit oranı",
    personal_status_sex: "Medeni durum / cinsiyet",
    other_debtors: "Kefil / ortak başvuru",
    present_residence_since: "İkamet süresi",
    property: "Varlık durumu",
    age: "Yaş",
    other_installment_plans: "Diğer taksit planları",
    housing: "Konut durumu",
    existing_credits: "Mevcut kredi sayısı",
    job: "Çalışma durumu",
    num_dependents: "Bakmakla yükümlü kişi sayısı",
    own_telephone: "Telefon durumu",
    foreign_worker: "Yabancı uyruklu çalışan",
  };

  return labels[feature] || feature;
}

export function ResultPanel({ result }: ResultPanelProps) {
  if (!result) {
    return (
      <div className="glass-card rounded-2xl border border-border/60 bg-card/80 p-6 shadow-[0_20px_60px_rgba(0,0,0,0.25)]">
        <h2 className="mb-3 text-xl font-semibold">Sonuç</h2>
        <p className="text-sm text-muted-foreground">
          Formu doldurup ön değerlendirmeyi başlattığınızda sonuç burada görünecek.
        </p>
      </div>
    );
  }

  const ui = getUiState(result);
  const Icon = ui.icon;

  return (
    <div className="glass-card rounded-2xl border border-border/60 bg-card/80 p-6 shadow-[0_20px_60px_rgba(0,0,0,0.25)] space-y-5">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h2 className="text-xl font-semibold">Ön Değerlendirme Sonucu</h2>
          <p className="mt-1 text-sm text-muted-foreground">{ui.subtitle}</p>
        </div>

        <div
          className={`inline-flex items-center gap-2 rounded-full border px-3 py-1.5 text-xs font-medium ${ui.badgeClass}`}
        >
          <Icon className="h-4 w-4" />
          {ui.title}
        </div>
      </div>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
        <div className="rounded-2xl border border-border/60 bg-secondary/40 p-4">
          <p className="text-xs uppercase tracking-[0.18em] text-muted-foreground">
            Başvuru Durumu
          </p>
          <div className="mt-2 text-2xl font-semibold">{ui.title}</div>
        </div>

        <div className="rounded-2xl border border-border/60 bg-secondary/40 p-4">
          <p className="text-xs uppercase tracking-[0.18em] text-muted-foreground">
            Risk Seviyesi
          </p>
          <div className="mt-2 text-2xl font-semibold">
            {getFriendlyRiskLabel(result.risk_level)}
          </div>
        </div>

        <div className="rounded-2xl border border-border/60 bg-secondary/40 p-4">
          <p className="text-xs uppercase tracking-[0.18em] text-muted-foreground">
            Risk Oranı
          </p>
          <div className="mt-2 text-2xl font-semibold">
            %{(result.default_probability * 100).toFixed(1)}
          </div>
        </div>
      </div>

      <div className="rounded-2xl border border-border/60 bg-secondary/30 p-4">
        <p className="text-xs uppercase tracking-[0.18em] text-muted-foreground">
          Değerlendirme Özeti
        </p>
        <p className="mt-2 text-sm leading-6 text-foreground">
          {result.underwriting_action.note}
        </p>
      </div>

      <div className="rounded-2xl border border-border/60 bg-secondary/30 p-4">
        <p className="text-xs uppercase tracking-[0.18em] text-muted-foreground">
          Başvurunuzu Güçlendirmek İçin Öneri
        </p>
        <p className="mt-2 text-sm leading-6 text-foreground">
          {result.recommended_action}
        </p>
      </div>

      <div className="rounded-2xl border border-border/60 bg-secondary/30 p-4">
        <p className="mb-3 text-xs uppercase tracking-[0.18em] text-muted-foreground">
          Sonucu Etkileyen Başlıca Unsurlar
        </p>

        <div className="space-y-3">
          {(result.top_drivers ?? []).length > 0 ? (
            result.top_drivers.map((driver, index) => (
              <div
                key={`${driver.feature}-${index}`}
                className="flex items-center justify-between rounded-xl border border-border/50 bg-background/30 px-3 py-3"
              >
                <div>
                  <div className="font-medium">
                    {getFriendlyFeatureName(driver.feature)}
                  </div>
                  <div className="text-xs text-muted-foreground">
                    {driver.direction === "risk_up"
                      ? "Riski artırıyor"
                      : "Riski azaltıyor"}
                  </div>
                </div>

                <div className="text-sm text-muted-foreground">
                  {driver.impact}
                </div>
              </div>
            ))
          ) : (
            <p className="text-sm text-muted-foreground">
              Bu başvuru için ek açıklama bulunamadı.
            </p>
          )}
        </div>
      </div>
    </div>
  );
}