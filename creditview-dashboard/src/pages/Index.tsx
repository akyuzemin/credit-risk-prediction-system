import { useEffect, useState } from "react";
import { ScoringForm } from "@/components/dashboard/ScoringForm";
import { ResultPanel } from "@/components/dashboard/ResultPanel";
import { fetchMeta } from "@/lib/api";
import type { MetaResponse, PredictResponse } from "@/lib/api";

const Index = () => {
  const [meta, setMeta] = useState<MetaResponse | null>(null);
  const [result, setResult] = useState<PredictResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const metaData = await fetchMeta();
        setMeta(metaData);
      } catch (err) {
        console.error("Failed to load form metadata:", err);
      } finally {
        setLoading(false);
      }
    }

    load();
  }, []);

  return (
    <div className="min-h-screen bg-background px-4 py-8 lg:px-8">
      <main className="mx-auto max-w-6xl space-y-8">
        <section className="space-y-3 text-center">
          <div className="mx-auto inline-flex rounded-full border border-primary/20 bg-primary/10 px-4 py-1 text-xs font-medium text-primary">
            Güvenli Ön Değerlendirme
          </div>

          <h1 className="font-display text-3xl font-bold tracking-tight lg:text-4xl">
            Kredi Ön Değerlendirme
          </h1>

          <p className="mx-auto max-w-2xl text-sm text-muted-foreground lg:text-base">
            Başvuru bilgilerinizi girerek kredi uygunluk durumunuzu hızlı ve anlaşılır şekilde öğrenin.
          </p>

          <p className="mx-auto max-w-2xl text-xs text-muted-foreground">
            Bu ekran yalnızca ön bilgilendirme sağlar. Nihai değerlendirme banka politikalarına göre yapılır.
          </p>
        </section>

        <section className="grid grid-cols-1 gap-6 lg:grid-cols-2">
          <ScoringForm meta={meta} onResult={setResult} />

          {loading ? (
            <div className="glass-card rounded-xl p-6">
              <h2 className="mb-3 text-lg font-semibold">Sonuç</h2>
              <p className="text-sm text-muted-foreground">
                Başvuru alanları hazırlanıyor...
              </p>
            </div>
          ) : (
            <ResultPanel result={result} />
          )}
        </section>

        <section className="glass-card rounded-xl p-5">
          <h2 className="mb-2 text-lg font-semibold">Nasıl değerlendirilir?</h2>
          <div className="space-y-2 text-sm text-muted-foreground">
            <p>
              Sistem; kredi tutarı, vade, birikim durumu, çalışma süresi ve
              benzeri başvuru bilgilerini birlikte değerlendirir.
            </p>
            <p>
              Sonuç ekranında göreceğiniz uygunluk durumu, risk seviyesi ve kısa
              öneriler sadece ön değerlendirme amaçlıdır.
            </p>
          </div>
        </section>
      </main>
    </div>
  );
};

export default Index;