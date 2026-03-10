def get_risk_level(prob: float) -> str:
    if prob >= 0.70:
        return "high"
    if prob >= 0.40:
        return "medium"
    return "low"


def recommend_action(prob: float, payload: dict) -> str:
    credit_amount = float(payload.get("credit_amount", 0) or 0)
    duration_months = int(payload.get("duration_months", 0) or 0)
    checking_status = payload.get("checking_status")
    savings_status = payload.get("savings_status")

    if prob >= 0.70:
        if credit_amount >= 8000 or duration_months >= 36:
            return "Başvurunuz yüksek risk grubunda görünüyor. Daha güçlü teminat veya kefil desteği olmadan onaylanması zor olabilir."
        return "Başvurunuz yüksek riskli görünüyor. Ek güvence veya detaylı uzman incelemesi gerekebilir."

    if prob >= 0.40:
        if credit_amount >= 5000:
            return "Başvurunuz sınırda değerlendiriliyor. Daha düşük tutar veya ek belge ile değerlendirme şansınız artabilir."
        if checking_status in {"A11", "A12"} or savings_status == "A65":
            return "Likidite ve birikim göstergeleri zayıf görünüyor. Ek belge ile başvuru güçlendirilebilir."
        return "Başvurunuz ek incelemeye uygun görünüyor."

    if duration_months >= 36 and credit_amount >= 7000:
        return "Genel olarak uygun görünüyorsunuz. Ancak yüksek tutar ve uzun vade nedeniyle ek kontrol yapılabilir."

    return "Başvurunuz ön değerlendirmede uygun görünüyor."

def build_underwriting_action(payload: dict, prob: float) -> dict:
    credit_amount = float(payload.get("credit_amount", 0) or 0)
    duration_months = int(payload.get("duration_months", 0) or 0)

    if prob >= 0.70:
        if credit_amount >= 8000 or duration_months >= 36:
            return {
                "decision": "Uygun Değil",
                "note": "Başvurunuz mevcut bilgilerle yüksek riskli görünmektedir."
            }
        return {
            "decision": "Uygun Değil",
            "note": "Başvurunuz standart koşullarda uygun görünmemektedir."
        }

    if prob >= 0.40:
        if credit_amount >= 5000:
            return {
                "decision": "Ek İnceleme Gerekli",
                "note": "Başvurunuz uzman değerlendirmesi ve ek belge ile tekrar incelenebilir."
            }
        return {
            "decision": "Ek İnceleme Gerekli",
            "note": "Başvurunuz için ek kontrol önerilmektedir."
        }

    if credit_amount >= 7000 and duration_months >= 36:
        return {
            "decision": "Uygun",
            "note": "Başvurunuz genel olarak uygun görünmektedir, ancak ek kontrol uygulanabilir."
        }

    return {
        "decision": "Uygun",
        "note": "Başvurunuz ön değerlendirmede uygun görünmektedir."
    }
