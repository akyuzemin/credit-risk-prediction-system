import { useMemo, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Send, Loader2 } from "lucide-react";
import type { MetaResponse, PredictRequest, PredictResponse } from "@/lib/api";
import { predict } from "@/lib/api";

interface ScoringFormProps {
  meta: MetaResponse | null;
  onResult: (result: PredictResponse) => void;
}

type SelectOption =
  | string
  | {
      value: string;
      label: string;
    };

type FieldConfig = {
  name: keyof PredictRequest;
  label: string;
  type: "categorical" | "numeric";
  min?: number;
  max?: number;
};

const FIELD_CONFIGS: FieldConfig[] = [
  { name: "checking_status", label: "Hesap Durumu", type: "categorical" },
  { name: "duration_months", label: "Vade (Ay)", type: "numeric", min: 1, max: 120 },
  { name: "credit_history", label: "Kredi Geçmişi", type: "categorical" },
  { name: "purpose", label: "Kredi Amacı", type: "categorical" },
  { name: "credit_amount", label: "Kredi Tutarı", type: "numeric", min: 0, max: 100000 },
  { name: "savings_status", label: "Birikim Durumu", type: "categorical" },
  { name: "employment_since", label: "Çalışma Süresi", type: "categorical" },
  { name: "installment_rate", label: "Taksit Oranı", type: "numeric", min: 1, max: 10 },
  { name: "personal_status_sex", label: "Medeni Durum / Cinsiyet", type: "categorical" },
  { name: "other_debtors", label: "Kefil / Ortak Başvuru", type: "categorical" },
  { name: "present_residence_since", label: "İkamet Süresi", type: "numeric", min: 1, max: 10 },
  { name: "property", label: "Varlık Durumu", type: "categorical" },
  { name: "age", label: "Yaş", type: "numeric", min: 18, max: 100 },
  { name: "other_installment_plans", label: "Diğer Taksit Planları", type: "categorical" },
  { name: "housing", label: "Konut Durumu", type: "categorical" },
  { name: "existing_credits", label: "Mevcut Kredi Sayısı", type: "numeric", min: 1, max: 10 },
  { name: "job", label: "Çalışma Durumu", type: "categorical" },
  { name: "num_dependents", label: "Bakmakla Yükümlü Kişi Sayısı", type: "numeric", min: 1, max: 10 },
  { name: "own_telephone", label: "Telefon Durumu", type: "categorical" },
  { name: "foreign_worker", label: "Yabancı Uyruklu Çalışan", type: "categorical" },
];

function normalizeOptions(options: SelectOption[] | undefined) {
  if (!options) return [];

  return options.map((item) => {
    if (typeof item === "string") {
      return { value: item, label: item };
    }
    return item;
  });
}

export function ScoringForm({ meta, onResult }: ScoringFormProps) {
  const [formData, setFormData] = useState<PredictRequest>({} as PredictRequest);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const selectOptions = useMemo(() => {
    return meta?.select_options ?? {};
  }, [meta]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const result = await predict(formData);
      onResult(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Değerlendirme sırasında bir hata oluştu");
    } finally {
      setLoading(false);
    }
  };

  if (!meta) {
    return (
      <div className="glass-card rounded-2xl border border-border/60 bg-card/80 p-6 shadow-[0_20px_60px_rgba(0,0,0,0.25)]">
        <h2 className="mb-1 text-lg font-semibold">Başvuru Formu</h2>
        <p className="mb-5 text-sm text-muted-foreground">
          Bilgiler yükleniyor...
        </p>
      </div>
    );
  }

  return (
    <div className="glass-card rounded-2xl border border-border/60 bg-card/80 p-6 shadow-[0_20px_60px_rgba(0,0,0,0.25)]">
      <div className="mb-6">
        <h2 className="mb-1 text-xl font-semibold">Başvuru Formu</h2>
        <p className="text-sm text-muted-foreground">
          Bilgilerinizi girerek kredi uygunluk ön değerlendirmenizi başlatın.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-5">
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
          {FIELD_CONFIGS.map((field) => {
            const options = normalizeOptions(
              selectOptions[field.name as keyof typeof selectOptions]
            );

            return (
              <div key={String(field.name)} className="space-y-2">
                <Label className="text-xs font-medium uppercase tracking-[0.14em] text-muted-foreground">
                  {field.label}
                </Label>

                {field.type === "categorical" ? (
                  <Select
                    onValueChange={(val) =>
                      setFormData((prev) => ({
                        ...prev,
                        [field.name]: val,
                      }))
                    }
                  >
                    <SelectTrigger className="h-11 rounded-xl border-border bg-secondary/70">
                      <SelectValue placeholder="Seçiniz" />
                    </SelectTrigger>
                    <SelectContent>
                      {options.map((item) => (
                        <SelectItem key={item.value} value={item.value}>
                          {item.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                ) : (
                  <Input
                    type="number"
                    step="any"
                    min={field.min}
                    max={field.max}
                    placeholder="Giriniz"
                    className="h-11 rounded-xl border-border bg-secondary/70 font-mono"
                    onChange={(e) =>
                      setFormData((prev) => ({
                        ...prev,
                        [field.name]: Number(e.target.value),
                      }))
                    }
                  />
                )}
              </div>
            );
          })}
        </div>

        {error && (
          <div className="rounded-xl border border-red-500/20 bg-red-500/10 px-4 py-3 text-sm text-red-300">
            {error}
          </div>
        )}

        <Button
          type="submit"
          disabled={loading}
          className="h-12 w-full rounded-xl bg-primary text-primary-foreground shadow-lg hover:opacity-90"
        >
          {loading ? (
            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
          ) : (
            <Send className="mr-2 h-4 w-4" />
          )}
          Ön Değerlendirmeyi Başlat
        </Button>
      </form>
    </div>
  );
}