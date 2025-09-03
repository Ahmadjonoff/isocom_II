# TZ Isocom V2

Status: In Progress
Priority: High
Responsible Person: Encar, Abdurauf Ahmadjonov, Elshod Nazarov
Due Date: August 30, 2025

ISOCOM Zavodi: Ishlab chiqarishni avtomatlashtirish
TEXNIK TOPSIRIQ (TZ)

Ushbu TZ ISOCOM zavodida ishlab chiqarish, ombor va sifat nazorati jarayonlarini RS-first (tarozi birlamchi) tamoyiliga tayangan holda to‘liq raqamlashtirish va Bitrix24 bilan integratsiyalash vazifalarini belgilaydi. Hujjat dasturchilar, tizim me’morlari, QA va operatsion jamoa uchun mo‘ljallangan.

1. Loyiha maqsadi va konteksti
1.1. Maqsad

Asosiy maqsad: Ombor → Sex (ichki ombor) → Ishlab chiqarish (sessiya) → Qadoqlash → OTK → Tayyor mahsulot ombori (FG) → Rework (drabilka) oqimini real vaqtda, aniq o‘lchov (RS) va mass-balans asosida avtomatlashtirish.

Ikkinchi darajali maqsad: KPI va oylik (Payroll)ni fakt ma’lumotlar asosida avtomatik hisoblash, Bitrix24 bilan ikki yo‘nalishli integratsiya.

Natija: Xatolarning keskin kamayishi, “qog‘oz+Excel”dan to‘liq voz kechish, hisobotlar va auditning ishonchliligi.

1.2. Kontekst va cheklovlar

Kontekst: 3 ta ekstruder (E1–E3), laminator/dublikatyor/resska oqimlari, drabilka (qattiq + yumshoq), FG ombori.

Cheklovlar:

RS485 tarozilar (YP12BSN) konvertor orqali Wi-Fi/Ethernet → Cloud Ingest API.

Laboratoriya yo‘q, OTK faqat tayyor qadoqlarda ishlaydi.

Operator bir vaqtda ≤ 2 ekstruderda ishlashi mumkin (grade: katta/starshiy).

Xomashyo tashqi logistikasi (zavodga kirish) scope tashqarisida; biz Main ombordan boshlab ishlaymiz.

Birlamchi tamoyillar:

RS-first: vazn o‘lchovi server tomonda tarozidan olinadi; qo‘lda kiritish – faqat boshliq approvali bilan, KPI’dan chiqariladi.

Mass-balans: Brak sababi kiritilmaydi; Brak = Input − Good − WIP.

FIFO yopish: Drabilka OUT (VT) faktlari sessiya braklariga FIFO bilan bog‘lanadi.

Gate/Approval: VT-limit, degazatsiya, kalibrovka va malaka kabi qat’iy to‘xtatuvchilar; manual/review/live-recipe/reopen — approvable.

1.3. Muvaffaqiyat mezonlari (KPI)

Δ-balans (|scrap_expected − (rework+disposed+outstanding)|) ≤ min(1%*input, 5 kg).

Qo‘lda kiritmalar ulushi < 5% (RS-trusted ratio > 95%).

QC OK bo‘lmagan qadoqlar FGga o‘tmasin (0 bypass).

Integratsiya PULL/PUSH muvaffaqiyati ≥ 97%.

KPI/Payroll snapshotlari oy yakunida 100% tasdiqlanadi.

1. Foydalanuvchi ehtiyojlari (User Stories)

Har bir story uchun “Done Criteria” berilgan; UI va API’da tekshiriladigan shartlar qat’iy.

2.1. Rollar

Direktor, Texnolog, Sex boshlig‘i, Operator, Shop operatori (sex ombor), Main omborchi, OTK, Drabilka operatori, FG omborchi, Moliya, Integrator (IT).

2.2. Ombor oqimi

Main omborchi sifatida, sexdan kelgan so‘rov bo‘yicha materialni RS’da tortib jo‘natmoqchiman, shunda hisob aniq bo‘ladi.
Done: MAIN_TO_SHOP (RS bilan), audit yozuvi, kalibrovka gate tekshirildi.

Shop operatori sifatida, jo‘natmani RS bilan qabul qilib, smena oxirida snapshot qilib qo‘ymoqchiman.
Done: SHOP+ (RS), SHOP_SNAPSHOT (RS), mantiqsiz/ manfiy qiymatlar bloklandi.

2.3. Sessiya va qadoqlash

Sex boshlig‘i sifatida, sessiyani boshlashdan oldin operatorlar ≤2 liniya va malaka mos bo‘lishini xohlayman.
Done: Gate >2_extruder va e3_qualification o‘tdi.

Operator sifatida, qadoq yaratganda vazn RS’dan tushsin, uzunlik avtomatik; tolеранс buzilganda “Review”ga yuboray.
Done: Package.weight_kg RS bilan lock, tolerance_status hisoblandi.

2.4. OTK va FG

OTK sifatida, faqat awaiting_qc paketlarni ko‘rib, protokol bilan ok/partial/reject qilaman va e-pechat qo‘yaman.
Done: QCRecord + e_pechat_hash, UI’da qayta tahrirga yopiq.

FG omborchi sifatida, QR skan bilan faqat QC OK paketlarni qabul qilaman, dublikat bo‘lsa OnHoldga tushsin.
Done: Gate qc_not_ok_to_fg/qr_duplicate tekshirildi, FG_RECEIVE yozildi.

2.5. Rework (drabilka)

Drabilka operatori sifatida, brakni konteynerlardan IN (RS) bilan qabul qilib, qayta ishlagach OUT (RS) bilan VT hosil qilaman.
Done: ReworkIO IN/OUT, VTBatch Main omborga kirim, Loss% hisoblandi.

2.6. KPI/Payroll va Integratsiya

Moliya sifatida, KPI/Payroll snapshotlarini tasdiqlab, Bitrixga idempotent eksport qilaman.
Done: KPISnapshot/PayrollSnapshot approved, IntegrationQueue(sent).

2.7. Direktor/Texnolog

Direktor sifatida, sessiyani re-open qilish so‘rovlarini ko‘rib tasdiqlayman; balans aniq bo‘lsin.
Done: Multi-approve (Sex boshlig‘i + Texnolog + Direktor), audit trail.

Texnolog sifatida, VT-limit buzilganda jarayon pause bo‘lsin; tahlildan so‘ng release qilaman.
Done: GateLog(vt_limit) → release, sessiya resume.

1. Biznes logikasi va qoidalar
3.1. Oqim modullari (M1–M15)

M1: Main → Shop (jo‘natish/qabul, RS–RS).

M2: Shop snapshot va Shop → Main qaytarish (RS–RS).

M3: Sessiya boshqaruvi (start/pause/resume/close/reopen), retsept snapshot, operator cheklovi.

M4: Ishlab chiqarish jarayoni va brakning hisobiy chiqishi (mass-balans).

M5: Qadoqlash & QR (RS vazn, auto/manual uzunlik, tolerans/Review).

M6: OTK (QC ok/partial/reject, e-pechat).

M7: Sessiya balansini yopish (Δ ≤ min(1%*input, 5 kg), Investigate).

M8: Rework/VT (IN/OUT RS, VT Main omborga, FIFO yopish).

M9: FG qabul (QR, dublikatga blok, degaz gate).

M10: Bitrix integratsiya (Users/Orders/Attendance PULL; KPI/Payroll PUSH).

M11: KPI/Payroll (reja-fakt, manual exclusion, approve/export).

M12: RBAC/Approval/Audit (manual/review/live-recipe/reopen/kpi/payroll).

M13: Gate/Alert siyosati (kalibrovka, degaz, VT-limit, malaka, QR dublikat).

M14: Panellar/Hisobotlar (operativ 5 s, batch export).

M15: IoT/RS pipeline (debounce, idempotency, binding oynasi).

3.2. Asosiy qoida va formullar

Brak (hisobiy):
scrap_expected_kg = input_kg − good_kg − wip_kg
delta = |scrap_expected − (rework_in_linked + disposed + outstanding)|
Yopish sharti: delta ≤ min(1%*input, 5 kg).

KPI (smena):
plan_unit = plan_24h × (shift_hours/24) × (actual_crew/norm_crew)
ach% = min(100, fact_unit/plan_unit × 100)
bonus = bonus_100 × ach%/100 (cap = 100%).
Eslatma: trusted=false (manual) yozuvlar KPI’dan chiqariladi, boshliq “override” bermasa.

UOM konversiya: SKU bo‘yicha (kg_per_m2, kg_per_m), polotno/setka/profil uchun qat’iy. Konversiya bo‘lmasa — OnHold.

3.3. Gate (bloklovchi) va Approval oqimlari

Gate’lar: vt_limit, degaz_gate, calibration_expired, >2_extruder, e3_qualification, qc_not_ok_to_fg, non_recyclable_to_rework, qr_duplicate.

Approval’lar: manual_weight/length (Sex boshlig‘i), review_tolerance (Sex boshlig‘i), live_recipe_change (Texnolog), reopen_session (3-approve), kpi/payroll (Moliya/Direktor siyosatiga muvofiq).

Audit: Har approvable amal uchun Approval + AuditLog(sig_hash).

3.4. Degazatsiya

SKU flagiga ko‘ra pending/done.

pending bo‘lsa QC/FG bosqichlarida gate ishga tushadi.

done – Sex boshlig‘i yoki Texnolog tomonidan qo‘yiladi (retseptga bog‘liq).

3.5. Drabilka

IN/OUT har ikki yo‘nalishda RS majburiy; Loss% avtomatik hisoblanadi.

VT Main omborga kirim bo‘ladi va sessiya braklariga FIFO bilan yopiladi.

Non-recyclable (masalan, laminatdagi zarrali qog‘oz) — Dispose yo‘liga o‘tadi (gate).

3.6. Integratsiya (Bitrix)

PULL: Xodimlar, buyurtmalar, attendance (ish vaqti).

PUSH: KPI/Payroll snapshotlari.

Idempotent: payload hash; mapping editor UI; xato bo‘lsa queue’da retry (eksponentsial backoff).

1. Tizim arxitekturasi tushuntirishi
4.1. Komponentlar

Frontend (PWA/React): Rolga asoslangan UI (Operator/OTK/Ombor/FG/Drabilka/Shop boss/Tech/Finance/Director).

Core API (Python/DRF): M1–M15 biznes modullari, RBAC, Gate/Approval/Audit, KPI/Payroll, Integratsiya API.

Ingest API: RS485 gatewaylardan kelgan ScaleEvent larni qabul qiladi (HMAC imzo, device token).

Worker/Queue: Hisobotlar, KPI/Payroll snapshot, Integratsiya queue, reconciliation.

DB (PostgreSQL): Tranzaksion jadvallar, “scale_events” va “audit_log” partitionlari.

Cache/RT: Redis (panel keshlari), WebSocket/SSE (operativ ko‘rsatkichlar).

Integratsiya konektor: Bitrix24 PULL/PUSH, mapping, idempotency.

Monitoring: Metriklar, loglar, alertlar (P1/P2/P3).

4.2. Muhitlar

DEV: RS simulator, Bitrix dry-run, demo ma’lumotlar.

STAGE: RS yaqin real qurilmalar, sandbox integratsiya.

PROD: Real qurilmalar va integratsiya; audit/gate/alert yoqilgan.

4.3. Yadro oqimlari (sekvens tavsifi)

IoT → Qadoq: ScaleEvent(stable) → Ingest → Qadoqlash UI kontekstida oxirgi N soniyada kelgan o‘qish package.weight_kg ga server-side bog‘lanadi.

M1 Main→Shop: Main RS − → Shop RS + (ikkala tomonda ham gate: calibration_expired).

QC → FG: awaiting_qc → OTK ok → FG QR skan (gate: degaz_gate, qr_duplicate).

4.4. Xavfsizlik va audit

JWT + refresh; RBAC minimal ruxsat; endpoint guard/dekoratorlar; har amalga AuditLog(sig_hash).

OTK qarorida e-pechat (HMAC) talab qilinadi.

Qurilmalar: device token, IP allowlist, NTP sinxron.

## 5. Ma’lumotlar oqimi (Data Flow)

### 5.1. Kontekst (DFD Level-0)

**Tashqi aktorlar:**

- **Foydalanuvchilar (rolga ko‘ra):** Direktor, Texnolog, Sex boshlig‘i, Operator, Shop/Main/FG omborchi, OTK, Drabilka operatori, Moliya.
- **Qurilmalar:** RS485 tarozilar (YP12BSN) → Gateway/MCU → Ingest API.
- **Tizimlar:** Bitrix24 (Users/Orders/Attendance PULL; KPI/Payroll PUSH).

**Ichki bloklar:**

- **Ingest API** (ScaleEvent qabul qiladi) → **Core API** (M1–M15 biznes xizmati) → **DB (PostgreSQL)** + **Redis (kesh/panel)** → **Worker/Queue** (hisobot/integratsiya/snapshot).

**Yadro oqimlar:**

1. **RS oqimi:** ScaleEvent → (binding oynasi ichida) → `StockTxn` (M1/M2) yoki `Package.weight_kg` (M5) yoki `ReworkIO` (M8).
2. **Tranzaksiyalar oqimi:** M1/M2/M5/M8 yozuvlari → audit → panellar.
3. **Kvalifikatsiya/gate/approval oqimi:** amallar → gate tekshiruvi → (kerak bo‘lsa) approval → holat o‘zgarishi.
4. **Integratsiya oqimi:** Bitrix PULL (cron/pull), KPI/Payroll PUSH (snapshot approved).

---

### 5.2. M1 — Main → Shop transfer (DFD L1)

**Input:** Sex boshlig‘i so‘rovi (SKU/retsept asosida materiallar), Main ombordagi batch’lar, RS (Main & Shop).

**Jarayon:**

1. Main: tanlangan batch’lar **RS** bilan tortiladi → `StockTxn{type=MAIN_TO_SHOP, from=MAIN, to=SHOP, material_id/batch_no, qty_kg}`.
2. Jo‘natma “in transit”; Shop qabul oynasi ochiq bo‘lganda **RS** o‘qish bilan `SHOP+` reyestrga kiradi (`SHOP` lokatsiya qoldig‘i oshadi).
3. Audit, Gate (`calibration_expired`) tekshiruv.
    
    **Output:** Main qoldig‘i kamayadi, Shop qoldig‘i oshadi; audit to‘liq; panel yangilanadi.
    

---

### 5.3. M2 — Shop snapshot & qaytarish

**Input:** Smena oxiri, qolgan materiallar; RS (Shop) snapshot.

**Jarayon:**

- Snapshot: `StockTxn{type=SHOP_SNAPSHOT, location=SHOP, material_id/batch_no, qty_kg}` (WIP sifatida M7 balansida ishlatiladi).
- Qaytarish: `StockTxn{type=SHOP_TO_MAIN, from=SHOP, to=MAIN}` — **RS** ikki tomonda.
    
    **Output:** Shop qoldiqlari tekislanadi; balansga `wip_kg` kiradi.
    

---

### 5.4. M3 — Sessiya boshqaruvi

**Input:** Workcenter (E1/E2/E3), partiya_no, SKU, retsept snapshot; operator assign (≤2; malaka gate).

**Jarayon:**

- `Session{opened}` → pause/resume (gate: VT-limit) → `close` (M7 qoidasi) yoki `reopen` (multi-approve).
    
    **Output:** `SessionBalance` (M7) uchun tayanch; panellar.
    

---

### 5.5. M5 — Qadoqlash & QR

**Input:** `Session`, RS (device: pack-scale), uzunlik (auto from counter yoki manual).

**Jarayon:**

1. Ingest: `ScaleEvent(stable)` → UI kontekstida **N soniya** ichidagi **oxirgi stable** o‘qish serverda bog‘lanadi.
2. `Package{weight_kg=RS, weight_trusted=true, length_mode, tolerance_status}` yaratiladi; `review` bo‘lsa boshliqga ketadi.
3. QR generatsiya; `awaiting_qc`.
    
    **Output:** Qadoqlar navbati OTKga; audit; tolerans statistikasi.
    

---

### 5.6. M6 — OTK (QC)

**Input:** `awaiting_qc` paketlar.

**Jarayon:** OTK protokolni to‘ldiradi → **e-pechat** → `qc_ok | qc_partial | qc_reject`.

**Output:** OK → M9 (FG), partial → split (qisman OK + rework), reject → M8 (rework IN).

---

### 5.7. M7 — Sessiya balansini yopish

**Input:** `SHOP_TO_SESSION` kirimlari, `Package(qc_ok)` summasi, `SHOP_SNAPSHOT (wip)`; M8 linklari (rework/disp).

**Jarayon:**

- `scrap_expected = input − good − wip`, `delta` tekshirish.
- Δ ≤ limit → **Close**; aks holda Investigate (snapshot/RS/QR/VT linklarni qayta ko‘rish) yoki Re-open (multi-approve).
    
    **Output:** `SessionBalance` yozuvi; KPI uchun asos.
    

---

### 5.8. M8 — Rework (drabilka) → VT

**Input:** Brak konteynerlari (ixtiyoriy SEAL/TARE bilan), RS (IN/OUT).

**Jarayon:**

- `ReworkIO(IN=RS)` → qayta ishlash → `ReworkIO(OUT=RS)`, `VTBatch` (Main’ga kirim).
- FIFO bilan sessiya scrap’lariga yopish (link).
    
    **Output:** `Loss%` metrik; `REWORK_VT_IN` tranzaksiya; balans yopilishi.
    

---

### 5.9. M9 — FG qabul

**Input:** QC OK paket QR; degaz holati.

**Jarayon:** FG QR skan → Gate: `qr_duplicate`, `qc_not_ok_to_fg`, `degaz_gate`.

**Output:** `FG_RECEIVE` tranzaksiya yoki `OnHold` yozuvi.

---

### 5.10. M10 — Integratsiya (Bitrix)

**PULL:** Users/Orders/Attendance → `IntegrationMapping` (idempotent).

**PUSH:** `KPISnapshot/PayrollSnapshot` → Bitrix (hash-idempotent).

**Queue:** Retry/backoff; xatolar “mapping editor” orqali tuzatiladi.

---

### 5.11. M11 — KPI/Payroll

**Input:** `SessionBalance`, `Package(qc_ok)`, Attendance.

**Jarayon:** Formula bo‘yicha hisob → `KPISnapshot` → approve → `PayrollSnapshot` → approve → PUSH.

**Output:** Moliya uchun to‘lov ro‘yxati; Bitrixda aks etadi.

---

### 5.12. Xatolik va retry oqimlari

- **Ingest**: late-arrival → `late_bool`; duplicate `(device_id,seq)` → no-op.
- **Integratsiya**: `error` → backoff → eskalatsiya.
- **Gate**: blok → UI banner + yechimga yo‘naltirish.

---

### 5.13. Holat mashinalari (konspekt)

- `Session`: `opened ↔ paused → closed → reopen(approved)`
- `Package`: `draft_manual? → awaiting_qc → qc_ok|qc_partial|qc_reject`
- `Approval`: `pending → approved|rejected`
- `GateLog`: `open → released`

---

## 6. API dokumentatsiyasi

### 6.0. Konvensiyalar

- **Base URL:** `/api/v1`
- **Auth:** `Authorization: Bearer <JWT>`
- **Format:** `application/json; charset=utf-8`
- **Datetime:** ISO-8601 (UTC)
- **Paging:** `?page=<int>&page_size=<1..200>`; default: 50
- **Filter:** `?from=...&to=...&sku_id=...&session_id=...`
- **Idempotensiya:** Ingest `(device_id,seq)` unique; Export `payload_hash` unique.
- **Xato formati:**

```json
{
  "success": false,
  "error": {
    "code": "validation_error|forbidden|gate_blocked|business_conflict|not_found",
    "message": "Inson o‘qiy oladigan izoh",
    "details": { "field": "xabar" }
  },
  "trace_id": "uuid"
}

```

---

### 6.1. Autentifikatsiya

**POST** `/auth/login`

**Body**: `{ "username": "user", "password": "..." }`

**200**:

```json
{ "access": "<jwt>", "refresh": "<jwt>", "user": {"id":"...", "role":"sex_boshligi"} }

```

**POST** `/auth/refresh` → yangi `access`.

> Eslatma: Ishlab chiqarish muhitida SSO ham bo‘lishi mumkin; JWT bu yerda minimal talablarga mos.
> 

---

### 6.2. Qurilma/kalibrovka/ingest

**GET** `/devices` → ro‘yxat (filter: `workcenter_id`, `type=scale`)

**PATCH** `/devices/{id}/calibration`

**Body**:

```json
{
  "performed_at": "2025-08-28T06:00:00Z",
  "valid_until": "2025-11-28T06:00:00Z",
  "certificate_no": "CAL-IS-2025-081"
}

```

**POST** `/ingest/scale-events`

**Headers:** `X-Device-Id`, `X-Signature` (HMAC)

**Body (single yoki batch):**

```json
{
  "events": [
    {
      "seq": 104238,
      "ts_device": "2025-08-28T10:14:37Z",
      "gross_kg": 20.520,
      "stable": true}
  ]
}

```

**201**:

```json
{ "accepted": 1, "duplicates": 0, "late": 0 }

```

---

### 6.3. M1/M2 — Ombor endpointlari

### 6.3.1. Main → Shop (jo‘natish)

**POST** `/stock/transfers/main-to-shop`

**Body:**

```json
{
  "lines": [
    { "material_id": "uuid", "batch_no": "PVD-2508-01", "device_id":"scale-MAIN-01" },
    { "material_id": "uuid", "batch_no": "VT-0825-05", "device_id":"scale-MAIN-02" }
  ],
  "comment": "E1 smena uchun"
}

```

> Har line uchun server oxirgi stable ScaleEventni device_id bo‘yicha topib, qty_kgni bog‘laydi. Manual kiritish taqiqlanadi (strict_rs_only).
> 

**201**:

```json
{
  "transfer_id": "uuid",
  "lines": [
    { "material_id":"...", "batch_no":"...", "qty_kg": 151.200, "scale_event_id": "..." }
  ],
  "status": "in_transit"
}

```

### 6.3.2. Shop qabul (M1 qabul)

**POST** `/stock/transfers/{transfer_id}/receive`

**Body:**

```json
{
  "lines": [
    { "material_id":"...", "batch_no":"...", "device_id":"scale-SHOP-01" }
  ]
}

```

**200**: `status="completed"`, Shop qoldig‘i yangilandi.

### 6.3.3. Shop snapshot (M2)

**POST** `/stock/shop/snapshot`

**Body:**

```json
{
  "items": [
    { "material_id":"...", "batch_no":"...", "device_id":"scale-SHOP-01" }
  ],
  "shift": "day"
}

```

**201**: snapshot yozuvlari, `wip_kg` M7 da ishlatiladi.

### 6.3.4. Shop → Main qaytarish (M2)

**POST** `/stock/transfers/shop-to-main`

**Body**: xuddi M1 kabi, lekin `from=SHOP, to=MAIN` (RS har ikki tomonda).

---

### 6.4. M3 — Sessiya endpointlari

**POST** `/sessions`

**Body:**

```json
{
  "workcenter_id": "uuid",  "sku_id": "uuid",
  "partiya_no": "ORD-2025-08-001",
  "shift": "day",
  "operators": ["user-1","user-2"]
}

```

**201**:

```json
{
  "id":"sess-uuid",
  "status":"opened",
  "recipe_snapshot": { "sku":"...", "lines":[ { "material":"PVD", "ratio_pct": 60 }, ... ] }
}

```

**PATCH** `/sessions/{id}/pause` → `{"reason":"tech"}`

**PATCH** `/sessions/{id}/resume`

**PATCH** `/sessions/{id}/close` → balans preview tekshiriladi, Δ ≤ limit bo‘lsa `closed`, aks holda 409 `business_conflict` (`delta_exceeded`).

**POST** `/sessions/{id}/reopen` → multi-approve oqimi boshlanadi.

---

### 6.5. M5 — Qadoqlash & Review

**POST** `/packages`

**Body:**

```json
{
  "session_id": "sess-uuid",
  "sku_id": "uuid",
  "length_mode": "auto",        // yoki "manual"
  "length_m": 120.5,            // manual bo'lsa talab qilinadi
  "device_id": "scale-E1-pack-01"
}

```

**201**:

```json
{
  "id":"pkg-uuid",
  "qr_code":"FG-2025-08-28-000123",
  "weight_kg": 20.520,
  "weight_trusted": true,
  "tolerance_status":"ok",
  "status":"awaiting_qc"
}

```

> Agar device_id bo‘yicha oxirgi stable RS topilmasa: draft_manual yaratiladi; 202 pending_approval.
> 

**POST** `/packages/{id}/review/submit` (tolerans breach)

**Body:** `{ "reason":"edge case thickness", "images":[] }`

**POST** `/packages/{id}/review/approve` yoki `/reject` — Sex boshlig‘i.

---

### 6.6. M6 — OTK (QC)

**POST** `/qc/decide`

**Body:**

```json
{
  "package_id":"pkg-uuid",
  "decision":"ok",              // "partial"|"reject"
  "protocol": { "note":"vizual ko'rik OK" },
  "e_pechat": "HMAC-SHA256(...)"
}

```

**200**: `status="qc_ok"` (yoki `qc_partial` → split jarayoni, `qc_reject` → rework IN navbati).

---

### 6.7. Gate/Approval va Audit API (umumiy)

**GET** `/gates?session_id=...` → ochiq gate’lar (vt_limit, degaz, calibration...).

**POST** `/approvals/{type}/{object_id}/approve` (yoki `/reject`)

**GET** `/audit?object_type=package&object_id=pkg-uuid` → difflar.

---

## 6. API dokumentatsiyasi (davomi)

> Konvensiya eslatmasi: Base URL: /api/v1, JWT auth, JSON, ISO-8601 UTC, paging & filterlar Qism 2 §6.0 da.
> 

### 6.8. M7 — Sessiya balansini yopish / Investigate / Re-open

**GET** `/sessions/{id}/balance/preview`

- **Ma’no:** Yopishdan oldingi hisoblash.
- **200**:

```json
{
  "session_id":"sess-uuid",
  "input_kg": 1500.000,
  "good_kg": 1180.000,
  "wip_kg": 50.000,
  "scrap_expected_kg": 270.000,
  "rework_in_linked_kg": 260.000,
  "disposed_linked_kg": 5.000,
  "outstanding_kg": 5.000,
  "delta_session_kg": 0.000,
  "gate_ok": true,
  "limit_kg": 5.000
}

```

**PATCH** `/sessions/{id}/close`

- **Natija:** Δ ≤ limit bo‘lsa `closed`; aks holda 409.
- **409** (`business_conflict`):

```json
{ "error": { "code":"delta_exceeded", "details": { "delta_kg": 8.4, "limit_kg": 5.0 } } }

```

**GET** `/sessions/{id}/investigate`

- **Ma’no:** Δ’ni tahlil qilish uchun linklar.
- **200**: `snapshotlar, qadoqlar, rework linklari, RS eventlar` ro‘yxati.

**POST** `/sessions/{id}/reopen`

- **Ma’no:** Multi-approve (Sex boshlig‘i → Texnolog → Direktor).
- **202**: `approval_id` qaytaradi.
- **POST** `/approvals/{approval_id}/approve` → oqim yakunlanadi.

---

### 6.9. M8 — Rework/Drabilka → VT

**POST** `/rework/orders`

- **Body**:

```json
{ "type":"rework_soft", "opened_by":"user-uuid", "note":"Smena-2 brak konteyner #RD-04" }

```

- **201**: `{ "id":"rw-uuid", "status":"opened" }`

**POST** `/rework/orders/{id}/in`

- **Ma’no:** Brak konteyner(lar)ini **RS** bilan qabul qilish.
- **Body**:

```json
{
  "containers": [
    { "seal_no":"BRK-2025-0828-01", "device_id":"scale-RW-IN-01" }
  ]
}

```

- **201**: `in_kg` RS’dan bog‘lanadi.

**POST** `/rework/orders/{id}/out`

- **Ma’no:** Qayta ishlangan VT’ni **RS** bilan chiqarish.
- **Body**:

```json
{ "device_id":"scale-RW-OUT-01", "vt_sku_id":"sku-vt" }

```

- **201**:

```json
{
  "out_kg": 298.500,
  "loss_pct": 0.5,
  "vt_batch_id": "vtb-uuid",
  "stock_txn_id":"txn-uuid"     // REWORK_VT_IN → Main
}

```

**POST** `/rework/fifo-link`

- **Ma’no:** VT batch(lar)ni sessiya scrap’lariga FIFO bilan yopish (agar avtomatikda outstanding qolsa — qo‘lda linklash).
- **Body**:

```json
{ "vt_batch_id":"vtb-uuid", "session_id":"sess-uuid", "qty_kg": 20.000 }

```

**POST** `/rework/dispose`

- **Ma’no:** Qayta ishlanmaydigan chiqit. Gate `non_recyclable_to_rework` ishlasa — shu yo‘l.
- **Body**: `{ "qty_kg": 3.000, "reason":"laminat zar qog'oz" }`

---

### 6.10. M9 — FG qabul (QR skan)

**POST** `/fg/receive`

- **Body**:

```json
{ "qr_code": "FG-2025-08-28-000123", "location_id":"FG-ZONE-A" }

```

- **200**:

```json
{ "status":"received", "package_id":"pkg-uuid", "received_at":"..." }

```

- **Gate xatolari:**
    - `qc_not_ok_to_fg`: paket `qc_ok` emas.
    - `qr_duplicate`: QR oldin qabul qilingan.
    - `degaz_gate`: degazatsiya `pending`.

**POST** `/fg/onhold/release`

- **Role:** Sex boshlig‘i (+ ixtiyoriy OTK).
- **Body**: `{ "qr_code":"...", "reason":"duplicate false-positive" }`

---

### 6.11. M10 — Bitrix integratsiya

**GET** `/integration/mapping?entity=user|order|attendance`

- **Ma’no:** Tashqi ↔ ichki ID mapping.
- **PATCH** `/integration/mapping/{id}` → qo‘lda tuzatish.

**POST** `/integration/pull`

- **Body**: `{ "entity": "user|order|attendance", "since":"2025-08-01T00:00:00Z" }`
- **Natija:** `IntegrationQueue`ga pull vazifalari qo‘shiladi (worker bajaradi).

**POST** `/integration/push`

- **Body**: `{ "entity": "kpi|payroll", "period":"2025-08" }`

**GET** `/integration/queue?status=pending|error|sent`

- **Ma’no:** Navbat statuslari; `retry` amali errorlar uchun.

**POST** `/integration/queue/{id}/retry`

- **Natija:** backoffni chetlab o‘tib, zudlik bilan sinaydi.

---

### 6.12. M11 — KPI/Payroll

**POST** `/kpi/snapshot/generate`

- **Body**:

```json
{
  "period_start":"2025-08-01T00:00:00Z",
  "period_end":"2025-08-31T23:59:59Z",
  "scope": { "workcenter_id": "E1" }   // ixtiyoriy
}

```

- **201**: `KPISnapshot` yozuvlari yaratildi.

**POST** `/kpi/snapshot/{id}/approve`

- **Role:** Sex boshlig‘i (yoki siyosat bo‘yicha Moliya).
- **Effect:** KPI “freeze”; manual/trusted=false yozuvlar defaultda **istisno**.

**POST** `/payroll/snapshot/generate?month=2025-08`

- **Body**: `{ "include_avans": true }`
- **201**: payroll draft’lar.

**POST** `/payroll/snapshot/{id}/approve`

- **Role:** Moliya.
- **Effect:** Bitrixga PUSH’ga tayyor.

**POST** `/payroll/export/bitrix?month=2025-08`

- **Effect:** `IntegrationQueue`ga PUSH vazifalari (hash-idempotent).

---

### 6.13. M12 — RBAC / Approval / Audit

**GET** `/rbac/roles` | **GET** `/rbac/permissions`

**POST** `/approvals/{type}/{object_id}/approve` | `/reject`

**GET** `/audit?object_type=sessions&object_id=...&from=...&to=...`

- **Natija:** imzolangan diff yozuvlari.

---

### 6.14. M13 — Gate / Alert

**GET** `/gates?session_id=...` → ochiq gate’lar.

**POST** `/gates/{gate_id}/release` → role bo‘yicha (Texnolog/Servis/va h.k.).

**GET** `/alerts?severity=P1|P2|P3&status=open|ack|closed`

**POST** `/alerts/{id}/ack` | `/close`

---

### 6.15. M14 — Panellar / Hisobotlar

**GET** `/dash/session-live?workcenter_id=E1`

- **Natija:** `input/good/wip/scrap_expected/delta/gates`.

**POST** `/reports`

- **Body**:

```json
{
  "type": "kpi_rollup|qc_defect|fg_aging|rs_trusted|rework_loss|session_delta_watch",
  "filters": { "from":"...", "to":"...", "workcenter_id":"..." },
  "format": "xlsx|csv|pdf"
}

```

- **201**: `report_job_id`.

**GET** `/reports/{id}` → `status=running|done` + `file_ref` (yuklab olish).

---

### 6.16. M15 — IoT / RS pipeline (qurilma hayoti)

**GET** `/devices/health` → heartbeat, kalibrovka muddati.

**POST** `/devices/{id}/heartbeat` (gateway)

**GET** `/ingest/scale-events?device_id=...&from=...&to=...` → diagnostika.

---

## 7. Xavfsizlik talablari

### 7.1. Autentifikatsiya va avtorizatsiya

- JWT + refresh; server rotation; token muddati siyosati (8 soat access, 30 kun refresh).
- RBAC minimal ruxsat: ro‘yxat Qism 1 §4.4, Qism 11 §92.3.
- Endpoint guard/dekoratorlari: `@enforce_gate`, `@requires_approval`, `@role_required`.

### 7.2. Qurilmalar va tarmoq

- Device token (alohida sir), **HMAC-SHA256** imzo.
- IP allowlist; NTP sinx; TLS 1.2+.
- `(device_id, seq)` unique — **idempotent** qabul.

### 7.3. Audit va e-pechat

- Har amal `AuditLog(sig_hash)` bilan.
- OTK qarorida `e_pechat_hash`; server tarafda `verify`.

### 7.4. Ma’lumot himoyasi

- PII (KPI/Payroll) — ko‘rish cheklovi; eksportlar **watermark** + audit.
- Backup shifrlangan; DR o‘yinlari chorakda 1 marta.

### 7.5. Rate-limit va DoS

- API: 120 rpm (user), Ingest: 600 rpm (device).
- Queue backpressure; retries with backoff.
- Log/metric monitoring (gate hit’lari, Δ, rs_trusted ratio).

---

## 8. Performance kriteriylari

### 8.1. SLO (oylik)

- API p95 **≤ 300 ms**; Ingest p95 **≤ 150 ms**; Panel refresh **≤ 5 s**.
- Idempotent qayta jo‘natish **no-op** (≤ 20 ms).
- Hisobotlar (≤ 1 mln qator) **≤ 90 s** (async job).

### 8.2. Oqim sig‘imi

- 3 ekstruder, pikda **30 RS event/min** har biri; jami ingest **≤ 100 event/min**.
- Qadoq yaratish **20 parallel** foydalanuvchi (p95 ≤ 300 ms).
- Sessiya balans preview **≤ 1.5 s** (1000 qadoq/sessiya).

### 8.3. Ma’lumotlar bazasi

- Partitionlar: `scale_events` (kun), `audit_log` (oy), `stock_txn` (oy).
- Muhim indekslar: QR unique, `(device_id, seq)`, `gate_log(gate_type, released_at is null)`, `integration_queue(status,last_try_at)`.

### 8.4. Kesh va real-time

- Redis kesh (operativ panellar); SSE/WebSocket — 5 s poll/push.
- Materializatsiyalangan view’lar (sessiya live, QC, FG).

---

## 9. Test ssenariylari

> Har test: ID, Precondition, Steps, Expected. Quyida yadro toifalar ro‘yxati va namunalar.
> 

### 9.1. Birlik (Unit) testlar

- **Rule**: `delta_calc()` — chekka holatlar (0 kg, katta qiymat, xatolik).
- **Gate**: `vt_limit_gate()` — limitga yaqin (thr ± ε).
- **Approval**: `manual_weight_flow()` — approve/reject branch’lari.
- **Idempotency**: `scale_event_upsert()` — duplicate `(device_id,seq)`.

### 9.2. Integratsion testlar

- **M1**: Main→Shop RS–RS (kalibrovka expired’da blok).
- **M5**: Qadoq + tolerans breach → review approve → OTK `ok`.
- **M8**: Rework IN/OUT RS → VTBatch → FIFO link → M7 Δ=0.
- **M9**: FG qabul (QR dublikat) → OnHold → Release.
- **M10**: PULL Users/Orders/Attendance; PUSH KPI/Payroll (idempotent).

### 9.3. End-to-End (E2E)

- **E2E-01**: `Main→Shop → Session → Qadoq(RS) → QC OK → FG` (Δ ≤ limit).
- **E2E-02**: `Brak ko‘p` → Rework → VT OUT → FIFO link → Close OK.
- **E2E-03**: `Degaz pending` → FG blok → degaz done → FG receive.

### 9.4. Salbiy (Negative) testlar

- Manual vazn kiritib KPIga kirishga urinish → **exclude + approval talab**.
- Operator 3-liniyaga assign → **gate blok**.
- OTK RS/uzunlikni tahrirlashga urinish → **403**.
- Device kalibrovkasi muddati o‘tgan → **gate blok**.

### 9.5. Security testlar

- JWT yo‘q / muddati o‘tgan → **401**.
- RBAC: roli mos emas → **403**.
- HMAC noto‘g‘ri → `/ingest` **401**.
- PII eksporti (Payroll) → audit yozuvi va watermark borligini tekshirish.

### 9.6. Performance/Load testlar

- Qadoq yaratish 20 par. foydalanuvchi p95 ≤ 300 ms.
- Ingest 100 event/min — yo‘qotishlarsiz; duplicate event’lar **no-op**.
- Report (1 mln qator) ≤ 90 s; API bloklanmaydi.

### 9.7. DR/Backup testlar

- STAGE’da to‘liq **restore drill**; `packages/stock_txn/audit_log` CRC/son mosligi.
- Failover (DB primary→standby) — xizmat uzilishsiz (≤ 2 min).

### 9.8. UAT (qabul) testlar

- Modullar bo‘yicha 150+ test (Qism 11 §92 katalogi): 100% o‘tish.
- Go-Live chek-list (Qism 8 §70) to‘liq.

## 10) Texnik stacklar ro‘yxati

### 10.1. Backend

- **Til/Framework:** Python 3.11+, **Django REST Framework (DRF)**.
- **ORM/Migratsiya:** Django ORM, **Alembic yo‘q**, Django migrations (standart).
- **Autentifikatsiya:** JWT (djangorestframework-simplejwt yoki ekvivalenti).
- **Gate/Approval Engine:** DRF view-dekoratorlari + xizmat qatlami (service layer).
- **Celery/RQ Worker:** Asinxron ishlar: hisobot, integratsiya navbati, KPI/Payroll snapshot, reconciliation.
- **Serializatsiya/Validatsiya:** DRF Serializer, qo‘shimcha biznes validatorlar (Zod FE tomonida).
- **Testing:** pytest + pytest-django + factory_boy.

### 10.2. Frontend (PWA)

- **React 18 + TypeScript**, **Vite** (bundler).
- **UI:** TailwindCSS + **shadcn/ui**, ikonalar: lucide-react.
- **State/RT:** React Query (server state), SSE/WebSocket (panel), Zustand (minimal UI state).
- **I18n/UOM:** Uzbek default, UOM formatterlar.
- **PWA:** Service Worker (statik kesh), “kiosk mode”.

### 10.3. IoT (Ingest)

- **Gateway/MCU:** ESP32/Arduino, RS485→Wi-Fi/Eth.
- **Protokol:** HTTPS + **HMAC-SHA256** imzo (device secret).
- **Debounce/Stable:** MCU tomonida (minimal), serverda yakuniy tekshiruv.

### 10.4. Ma’lumotlar bazasi va kesh

- **DB:** PostgreSQL 14+ (partitioning: `scale_events` kun, `audit_log` oy, `stock_txn` oy).
- **Kesh/RT:** Redis (panellar materializatsiyasi, navbat indikatorlari).

### 10.5. Monitoring/Observability

- **APM/Logs:** OpenTelemetry (OTLP), Prometheus metriklari, Grafana dashboard.
- **Alerting:** P1/P2/P3 siyosat (Slack/Email/SMS).

### 10.6. DevOps

- **Container:** Docker, docker-compose (DEV), Kubernetes (STAGE/PROD).
- **CI/CD:** GitHub Actions/GitLab CI — test → build → migrate → deploy.
- **Secrets:** Vault/yoki K8s Secrets, .env **yo‘q** (local devdan tashqari).

---

## 11) Endpoint’lar yakuniy ro‘yxati (modul bo‘yicha)

> Base: /api/v1, Auth: JWT. Quyida metod + yo‘l (payload tafsili Qism 2–3 da).
> 

### 11.1. Auth & Users

- `POST /auth/login`, `POST /auth/refresh`
- `GET /me`, `GET /users?role=...`, `GET /roles`, `GET /permissions`

### 11.2. Qurilma/kalibrovka/ingest

- `GET /devices`, `PATCH /devices/{id}/calibration`
- `GET /devices/health`, `POST /devices/{id}/heartbeat`
- `POST /ingest/scale-events` (batch/single)
- `GET /ingest/scale-events?device_id=&from=&to=`

### 11.3. M1–M2: Ombor oqimi

- `POST /stock/transfers/main-to-shop`
- `POST /stock/transfers/{transfer_id}/receive`
- `POST /stock/shop/snapshot`
- `POST /stock/transfers/shop-to-main`
- `GET /stock/locations` (MAIN/SHOP/FG)
- `GET /stock/items?location=SHOP|MAIN|FG`

### 11.4. M3: Sessiya

- `POST /sessions`
- `PATCH /sessions/{id}/pause`
- `PATCH /sessions/{id}/resume`
- `GET /sessions/{id}/balance/preview`
- `PATCH /sessions/{id}/close`
- `POST /sessions/{id}/reopen`
- `GET /sessions?status=open|closed&workcenter_id=...`

### 11.5. M5–M6: Qadoqlash & QC

- `POST /packages`
- `POST /packages/{id}/review/submit`
- `POST /packages/{id}/review/approve`
- `POST /packages/{id}/review/reject`
- `POST /qc/decide`
- `GET /qc/queue?workcenter_id=...`

### 11.6. M8: Rework/VT

- `POST /rework/orders`
- `POST /rework/orders/{id}/in`
- `POST /rework/orders/{id}/out`
- `POST /rework/fifo-link`
- `POST /rework/dispose`
- `GET /rework/orders?status=open|closed`

### 11.7. M9: FG qabul

- `POST /fg/receive`
- `POST /fg/onhold/release`
- `GET /fg/items`
- `GET /fg/onhold`

### 11.8. M10: Integratsiya (Bitrix)

- `GET /integration/mapping?entity=user|order|attendance`
- `PATCH /integration/mapping/{id}`
- `POST /integration/pull`
- `POST /integration/push`
- `GET /integration/queue?status=pending|error|sent`
- `POST /integration/queue/{id}/retry`

### 11.9. M11: KPI/Payroll

- `POST /kpi/snapshot/generate`
- `POST /kpi/snapshot/{id}/approve`
- `GET /kpi/snapshot?period=...`
- `POST /payroll/snapshot/generate?month=...`
- `POST /payroll/snapshot/{id}/approve`
- `POST /payroll/export/bitrix?month=...`
- `GET /payroll/snapshot?month=...`

### 11.10. M12–M13–M14–M15: RBAC/Gate/Audit/Panel

- `GET /gates?session_id=...`, `POST /gates/{gate_id}/release`
- `POST /approvals/{type}/{object_id}/approve|reject`
- `GET /audit?object_type=&object_id=&from=&to=`
- `GET /dash/session-live?workcenter_id=...`
- `POST /reports`, `GET /reports/{id}`

---

## 12) Ma’lumotlar bazasi sxemasi

### 12.1. ER-yadro (matnli ko‘rinish)

- **User (1..n)**—`Approval/Audit`—(n..1)**Object** (session/package/…)
- **Workcenter (1..n)**—**Device (1..n)**—**ScaleEvent**
- **SKU (1..n)**—**Recipe (1..n)**—**RecipeLine**
- **StockLocation (MAIN/SHOP/FG)**—**StockItem**—**StockTxn**
- **Session (1..n)**—**Package (1..n)**—**QCRecord (0..1)**—**FG Receive**
- **Session**—**SessionBalance (1..1)**
- **ReworkOrder (1..n)**—**ReworkIO (0..n)**—**VTBatch (0..n)**—**StockTxn(REWORK_VT_IN)**
- **IntegrationMapping/Queue**, **KPI/Payroll Snapshot**, **GateLog**, **Alert**, **ReportJob**

### 12.2. Asosiy jadvallar (kalit maydonlar)

**users**(id, full_name, position, grade, status, created_at, updated_at)

**roles**, **user_roles**, **permissions**, **role_permissions** *(agar granular RBAC kerak bo‘lsa)*

**workcenters**(id, code, type, name, location, active_bool)

**devices**(id, workcenter_id*, device_type, serial_no, calibration_due_at, last_heartbeat_at, active_bool)

**calibration**(id, device_id*, performed_at, valid_until, certificate_no, by_whom)

**scale_events**(id, device_id*, seq, ts_device, ts_ingested, gross_kg, stable_bool, trusted_bool, late_bool, bind_ref) — **partition (by day)**, **unique(device_id,seq)**

**materials**(id, code, name, category, polymer_family, recyclable_bool, attributes_json)

**material_batches**(id, material_id*, batch_no, received_at, supplier, quality_cert_no)

**skus**(id, code, name, category, uom_default, width_mm, thickness_mm, kg_per_m2, mesh_type, is_recyclable_for_rework_bool, tolerance_weight_pct, tolerance_length_pct, degaz_required_bool)

**recipes**(id, sku_id*, version, vt_limit_pct, status, published_at, published_by)

**recipe_lines**(id, recipe_id*, material_id*, comp_type, ratio_pct, ratio_per_kg, is_optional_bool)

**stock_locations**(id, code: MAIN/SHOP/FG, name, zone)

**stock_items**(id, location_id*, item_type(material|sku|vt), material_id?, sku_id?, batch_no?, qty, uom, degaz_status)

**stock_txn**(id, type, from_location_id?, to_location_id?, item_type, material_id?, sku_id?, batch_no?, qty, uom, ts, by_user, ref_doc) — **partition (by month)**

**sessions**(id, workcenter_id*, sku_id*, partiya_no, shift, operators[], status, started_at, ended_at, recipe_snapshot_json)

**session_input_link**(id, session_id*, stock_txn_id*, qty_kg)

**packages**(id, session_id*, sku_id*, qr_code unique, weight_kg, weight_trusted_bool, length_m, length_mode, length_trusted_bool, tolerance_status, status, created_by, created_at) — **index (status)**

**qc_records**(id, package_id* unique, inspector_id*, decision, protocol_json, e_pechat_hash, ts)

**session_balance**(id, session_id* unique, input_kg, good_kg, wip_kg, scrap_expected_kg, rework_in_linked_kg, disposed_linked_kg, outstanding_kg, delta_session_kg) — **index(filter: delta_session_kg>0)**

**rework_orders**(id, type, opened_by, opened_at, notes, status)

**rework_io**(id, rework_order_id*, in_kg, in_at, in_by, out_kg, out_at, out_by, loss_pct)

**vt_batches**(id, rework_order_id*, sku_id*(VT), qty_kg, location_id=MAIN, created_at)

**disposed_log**(id, reason, qty_kg, ts, by_user)

**integration_mapping**(id, external_system, entity, external_id, internal_id, meta_json)

**integration_queue**(id, direction, entity, operation, payload_json, payload_hash, status, error_msg, retry_count, last_try_at) — **index(status,last_try_at)**

**kpi_config**(id, bonus_100, cap_pct, penalties_json, allow_manual_bool)

**kpi_snapshot**(id, period_start, period_end, workcenter_id, shift, crew_json, plan_unit, fact_unit, ach_pct, bonus_amount, status, approved_by, approved_at)

**payroll_snapshot**(id, month, user_id, base_salary, kpi_bonus, avans, penalties, net_pay, status, approved_by, approved_at, exported_to_bitrix_bool)

**approvals**(id, object_type, object_id, requested_by, requested_at, state, approver_id, approved_at, comment)

**audit_log**(id, actor_id, role, ts, action, object_type, object_id, old_new_diff_json, sig_hash) — **partition (by month)**

**gate_log**(id, gate_type, object_ref, ts, released_at, released_by, note) — **index(gate_type, released_at is null)**

**alerts**(id, severity, metric_code, value, threshold, ts, routed_to, status, closed_at)

**report_jobs**(id, type, filters_json, format, status, file_ref, created_by, created_at, finished_at)

### 12.3. Muhim CHECK/UNIQUE/FK qoidalari

- `scale_events`: **unique(device_id, seq)**.
- `stock_items`: **CHECK** `(material_id IS NULL) XOR (sku_id IS NULL)`.
- `packages.qr_code`: **UNIQUE**.
- `qc_records.package_id`: **UNIQUE** (har paketga bitta QC).
- `session_balance.session_id`: **UNIQUE**.
- `session_delta_check`: **CHECK** `delta_session_kg <= LEAST(0.01*input_kg, 5)` yopishda enforced (service qatlamida ham).

### 12.4. Indekslar

- `packages(status, created_at DESC)`
- `gate_log(gate_type, released_at)` **partial** (`released_at IS NULL`)
- `integration_queue(status, last_try_at)`
- `stock_txn(type, ts)`
- `audit_log(ts)` (partition)
- `scale_events(ts_ingested)` (partition)

---

## 13) Konfiguratsiya parametrlari (ENV)

| Kalit | Turi | Default | Izoh |
| --- | --- | --- | --- |
| `DB_DSN` | string | — | PostgreSQL DSN |
| `REDIS_URL` | string | — | Redis |
| `JWT_SECRET` | string | — | JWT imzo |
| `SERVER_SECRET` | string | — | Audit sig_hash |
| `QC_SECRET` | string | — | OTK e-pechat HMAC |
| `IOT_ACCEPT_WINDOW_SEC` | int | 10 | RS binding oynasi |
| `STRICT_RS_ONLY` | bool | true | Manual vaznni bloklash (prod) |
| `VT_GATE_HARD` | bool | true | VT-limit buzilsa pause |
| `DEGAZ_GATE_FG` | bool | true | Degaz pending → FG blok |
| `BITRIX_BASE_URL` | string | — | Integratsiya |
| `BITRIX_TOKEN` | secret | — | Integratsiya |
| `BITRIX_TIMEOUT_MS` | int | 8000 | HTTP timeout |
| `BITRIX_RETRY_MAX` | int | 8 | Retry count |
| `REPORT_MAX_ROWS` | int | 1_000_000 | Eksport limiti |
| `EXPORT_RETENTION_DAYS` | int | 30 | Fayl saqlash |
| `BACKUP_KEEP_DAYS` | int | 30 | Zaxira saqlash |
| `API_RATE_LIMIT_RPM` | int | 120 | Foydalanuvchi rate-limit |
| `INGEST_RATE_LIMIT_RPM` | int | 600 | Qurilma rate-limit |

---

## 14) Deadlinelar va releas-reja (Hybrid Agile)

> Boshlanish sanasi: 2025-09-01 (Dushanba), vaqt zonasi: Asia/Tashkent.
> 
> 
> Sprint davomiyligi: **2 hafta**. Hardening: **1 hafta**.
> 

### 14.1. Sprintlar

- **Sprint 0 (2025-09-01 → 2025-09-12):**
    
    Master-data import (SKU/Material/Recipe/PlanNorm), Device registry+Calibration, RBAC skeleti, Ingest skeleton.
    
    **Qabul:** CSV importlari ishlaydi; 1 ta tarozi’dan event qabul qilinadi; RBAC minimal.
    
- **Sprint 1 (2025-09-15 → 2025-09-26):**
    
    M1–M2: Main↔Shop RS oqimlari, snapshot/qaytarish; stok panel.
    
    **Qabul:** RS–RS tranzaksiyalar; kalibrovka gate test; audit yoziladi.
    
- **Sprint 2 (2025-09-29 → 2025-10-10):**
    
    M3–M5: Sessiya, Qadoqlash/QR, tolerans/review; Δ live preview.
    
    **Qabul:** Qadoq RS lock, review approve oqimi, session preview <1.5 s.
    
- **Sprint 3 (2025-10-13 → 2025-10-24):**
    
    M6–M7–M9: OTK (e-pechat), Sessiya yopish (Investigate), FG qabul (QR anti-repeat, degaz gate).
    
    **Qabul:** QC navbati, e-pechat verifikatsiya, FG dublikat blok.
    
- **Sprint 4 (2025-10-27 → 2025-11-07):**
    
    M8 rework/VT (IN/OUT, FIFO), M10 Bitrix (PULL/PUSH dry→real), M11 KPI/Payroll.
    
    **Qabul:** Rework Loss% trend; Bitrix PULL/PUSH idempotent; KPI/payroll snapshot/approve.
    
- **Hardening (2025-11-10 → 2025-11-14):**
    
    Security chek-list (Ilova G), DR sinovi, Performance tuning, UAT.
    
    **Qabul:** UAT 100% o‘tish; DR RPO≤15m, RTO≤2h; p95 ko‘rsatkichlar.
    
- **Go-Live (2025-11-17):**
    
    Cutover, Excel/qog‘oz to‘xtatiladi, Hypercare T+7.
    

### 14.2. Milestone qabul mezonlari (har sprint)

- **Demo & UAT**: sprintning asosiy oqimlari “happy path” E2E o‘tilgan bo‘lishi.
- **Testlar**: Unit/Integration minimal 80% qamrov (kritik modul).
- **Security**: JWT/RBAC/gate/approval/audit ishlashi.
- **Docs**: API schema va SOP yangilangan.

---

## 15) Yakuniy qabul mezonlari (Go-Live)

1. **Δ-balans** yopilishi: barcha ishlab chiqarish sessiyalari uchun `delta ≤ min(1%*input, 5 kg)`.
2. **RS-trusted ratio** ≥ 95%; manual yozuvlar approve bilan cheklangan.
3. **FG qabul**: QC OK bo‘lmagan paketlar 0; QR dublikatlar OnHold va jurnalga tushadi.
4. **Rework**: VT FIFO bilan sessiya braklariga yopiladi; Loss% monitoring ishlaydi.
5. **KPI/Payroll**: oy yakunida snapshot/approve; Bitrixga eksport muvaffaqiyati ≥ 97%.
6. **NFR**: p95 API ≤ 300 ms; Ingest p95 ≤ 150 ms; panel ≤ 5 s.
7. **DR**: RPO ≤ 15 min, RTO ≤ 2 soat — STAGE’da isbotlangan.
8. **UAT**: 150+ testdan 100% o‘tish.

## 16) ER / DDL snippetlari (PostgreSQL)

> Izoh: Quyidagi DDL’lar ishlaydigan andoza sifatida berilgan. Real loyihada Django migrations orqali generatsiya qilinadi. Kommentariyalar orqali biznes qoida mustahkamlangan.
> 

### 16.1. Yadro obyektlari

```sql
-- USERS
create table users (
  id uuid primary key,
  full_name text not null,
  position text not null check (position in (
    'direktor','texnolog','sex_boshligi','operator',
    'shop_op','main_ombor','fg_ombor','otk','moliya','integrator'
  )),
  grade text check (grade in ('stajor','kichik','katta','starshiy')),
  status text not null check (status in ('active','disabled')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

-- WORKCENTER
create table workcenters (
  id uuid primary key,
  code text unique not null,                -- E1/E2/E3/...
  type text not null check (type in ('extruder','coater','laminator','duplicator','cutter','rework_hard','rework_soft')),
  name text not null,
  location text,
  active_bool boolean not null default true
);

-- DEVICE (scale/length_counter)
create table devices (
  id uuid primary key,
  workcenter_id uuid references workcenters(id),
  device_type text not null check (device_type in ('scale','length_counter')),
  serial_no text,
  active_bool boolean not null default true,
  calibration_due_at timestamptz,
  last_heartbeat_at timestamptz
);

-- SCALE EVENTS (partitioned by day)
create table scale_events (
  id uuid primary key,
  device_id uuid not null references devices(id),
  seq bigint not null,
  ts_device timestamptz not null,
  ts_ingested timestamptz not null default now(),
  gross_kg numeric(14,3) not null check (gross_kg >= 0),
  stable_bool boolean not null,
  trusted_bool boolean not null default true,
  late_bool boolean not null default false,
  bind_ref jsonb,                              -- ex: {"package_id":"..."} yoki {"stock_txn_id":"..."}
  unique (device_id, seq)
) partition by range (date(ts_ingested));

```

> Eslatma: scale_events uchun kunlik partitionlar CREATE TABLE scale_events_2025_08_28 PARTITION OF ... FOR VALUES FROM ('2025-08-28') TO ('2025-08-29') ko‘rinishida yaratiladi (migratsiya/cron).
> 

### 16.2. Material/SKU/Recipe

```sql
create table materials (
  id uuid primary key,
  code text unique not null,
  name text not null,
  category text not null check (category in ('perv','vt','additiv')),
  polymer_family text check (polymer_family in ('PE','PP','PVC','OTHER')),
  recyclable_bool boolean not null default true,
  attributes_json jsonb
);

create table material_batches (
  id uuid primary key,
  material_id uuid not null references materials(id),
  batch_no text not null,
  received_at timestamptz,
  supplier text,
  quality_cert_no text,
  unique (material_id, batch_no)
);

create table skus (
  id uuid primary key,
  code text unique not null,
  name text not null,
  category text not null check (category in ('polotno','setka','ot','js','profil','lam_out','dubl','kesilgan','izdeliya','vt')),
  uom_default text not null check (uom_default in ('kg','m','m2')),
  width_mm numeric(10,2),
  thickness_mm numeric(10,3),
  kg_per_m2 numeric(12,5),
  mesh_type text,
  is_recyclable_for_rework_bool boolean not null default true,
  tolerance_weight_pct numeric(6,3),
  tolerance_length_pct numeric(6,3),
  degaz_required_bool boolean not null default false
);

create table recipes (
  id uuid primary key,
  sku_id uuid not null references skus(id),
  version integer not null default 1,
  vt_limit_pct numeric(6,3) default 0,   -- VT limit (gate)
  status text not null check (status in ('draft','published')) default 'draft',
  published_at timestamptz,
  published_by uuid references users(id)
);

create table recipe_lines (
  id uuid primary key,
  recipe_id uuid not null references recipes(id) on delete cascade,
  material_id uuid not null references materials(id),
  comp_type text not null check (comp_type in ('perv','vt','additiv')),
  ratio_pct numeric(8,4),         -- umumiy foiz (100% ga mos)
  ratio_per_kg numeric(12,6),     -- yoki kg/kg koeffitsiyent
  is_optional_bool boolean not null default false
);

```

### 16.3. Stok va tranzaksiyalar

```sql
create table stock_locations (
  id uuid primary key,
  code text unique not null check (code in ('MAIN','SHOP','FG')),
  name text not null,
  zone text
);

create table stock_items (
  id uuid primary key,
  location_id uuid not null references stock_locations(id),
  item_type text not null check (item_type in ('material','sku','vt')),
  material_id uuid,
  sku_id uuid,
  batch_no text,
  qty numeric(14,3) not null default 0,
  uom text not null check (uom in ('kg','m','m2')),
  degaz_status text check (degaz_status in ('pending','done')),
  check ( (material_id is null) <> (sku_id is null) )   -- XOR
);

create table stock_txn (
  id uuid primary key,
  type text not null check (type in ('MAIN_TO_SHOP','SHOP_TO_MAIN','SHOP_SNAPSHOT','SHOP_TO_SESSION','FG_RECEIVE','REWORK_VT_IN','DISPOSE_WASTE')),
  from_location_id uuid references stock_locations(id),
  to_location_id uuid references stock_locations(id),
  item_type text not null check (item_type in ('material','sku','vt')),
  material_id uuid,
  sku_id uuid,
  batch_no text,
  qty numeric(14,3) not null check (qty > 0),
  uom text not null check (uom in ('kg','m','m2')),
  ts timestamptz not null default now(),
  by_user uuid references users(id),
  ref_doc jsonb
) partition by range (date(ts));

```

### 16.4. Sessiya, qadoq, QC, balans

```sql
create type session_status as enum ('opened','paused','closed');

create table sessions (
  id uuid primary key,
  workcenter_id uuid not null references workcenters(id),
  sku_id uuid not null references skus(id),
  partiya_no text not null,
  shift text not null check (shift in ('day','night')),
  operators uuid[] not null,                          -- ≤2, service layer tekshiradi
  status session_status not null default 'opened',
  started_at timestamptz not null default now(),
  ended_at timestamptz,
  recipe_snapshot_json jsonb not null
);

create table packages (
  id uuid primary key,
  session_id uuid not null references sessions(id),
  sku_id uuid not null references skus(id),
  qr_code text not null unique,
  weight_kg numeric(14,3) not null check (weight_kg >= 0),
  weight_trusted_bool boolean not null default true,
  length_m numeric(14,2),
  length_mode text check (length_mode in ('auto','manual')),
  length_trusted_bool boolean,
  tolerance_status text not null check (tolerance_status in ('ok','review')),
  status text not null check (status in ('awaiting_qc','qc_ok','qc_reject','qc_partial')) default 'awaiting_qc',
  created_by uuid references users(id),
  created_at timestamptz not null default now()
);

create table qc_records (
  id uuid primary key,
  package_id uuid not null unique references packages(id) on delete cascade,
  inspector_id uuid not null references users(id),
  decision text not null check (decision in ('ok','partial','reject')),
  protocol_json jsonb,
  e_pechat_hash text not null,
  ts timestamptz not null default now()
);

create table session_balance (
  id uuid primary key,
  session_id uuid not null unique references sessions(id) on delete cascade,
  input_kg numeric(14,3) not null,
  good_kg numeric(14,3) not null,
  wip_kg numeric(14,3) not null,
  scrap_expected_kg numeric(14,3) not null,
  rework_in_linked_kg numeric(14,3) not null default 0,
  disposed_linked_kg numeric(14,3) not null default 0,
  outstanding_kg numeric(14,3) not null default 0,
  delta_session_kg numeric(14,3) not null default 0
);
create index idx_session_balance_delta on session_balance (delta_session_kg) where delta_session_kg > 0;

```

### 16.5. Rework/VT, Dispose

```sql
create table rework_orders (
  id uuid primary key,
  type text not null check (type in ('rework_hard','rework_soft')),
  opened_by uuid references users(id),
  opened_at timestamptz not null default now(),
  notes text,
  status text not null check (status in ('opened','closed')) default 'opened'
);

create table rework_io (
  id uuid primary key,
  rework_order_id uuid not null references rework_orders(id) on delete cascade,
  in_kg numeric(14,3),
  in_at timestamptz,
  in_by uuid references users(id),
  out_kg numeric(14,3),
  out_at timestamptz,
  out_by uuid references users(id),
  loss_pct numeric(6,3)      -- service layerda calc: (in - out)/in * 100
);

create table vt_batches (
  id uuid primary key,
  rework_order_id uuid not null references rework_orders(id),
  sku_id uuid not null references skus(id),          -- VT tipidagi SKU
  qty_kg numeric(14,3) not null,
  location_id uuid not null references stock_locations(id),
  created_at timestamptz not null default now()
);

create table disposed_log (
  id uuid primary key,
  reason text,
  qty_kg numeric(14,3) not null check (qty_kg > 0),
  ts timestamptz not null default now(),
  by_user uuid references users(id)
);

```

### 16.6. Integratsiya, KPI/Payroll, approval/audit/gate/alert

```sql
create table integration_mapping (
  id uuid primary key,
  external_system text not null check (external_system='bitrix'),
  entity text not null check (entity in ('user','order','attendance')),
  external_id text not null,
  internal_id uuid not null,
  meta_json jsonb,
  unique (external_system, entity, external_id)
);

create table integration_queue (
  id uuid primary key,
  direction text not null check (direction in ('pull','push')),
  entity text not null check (entity in ('user','order','attendance','kpi','payroll')),
  operation text not null check (operation in ('upsert','export')),
  payload_json jsonb not null,
  payload_hash text not null,
  status text not null check (status in ('pending','sent','error')) default 'pending',
  error_msg text,
  retry_count int not null default 0,
  last_try_at timestamptz
);
create index idx_intq_status_try on integration_queue(status,last_try_at);

create table kpi_config (
  id uuid primary key,
  bonus_100 numeric(14,2) not null,
  cap_pct numeric(6,2) not null default 100,
  penalties_json jsonb,
  allow_manual_bool boolean not null default false
);

create table kpi_snapshot (
  id uuid primary key,
  period_start timestamptz not null,
  period_end timestamptz not null,
  workcenter_id uuid,
  shift text,
  crew_json jsonb,
  plan_unit numeric(14,3),
  fact_unit numeric(14,3),
  ach_pct numeric(6,2),
  bonus_amount numeric(14,2),
  status text not null check (status in ('draft','approved')) default 'draft',
  approved_by uuid references users(id),
  approved_at timestamptz
);

create table payroll_snapshot (
  id uuid primary key,
  month text not null,   -- '2025-08'
  user_id uuid not null references users(id),
  base_salary numeric(14,2) not null default 0,
  kpi_bonus numeric(14,2) not null default 0,
  avans numeric(14,2) not null default 0,
  penalties numeric(14,2) not null default 0,
  net_pay numeric(14,2) not null default 0,
  status text not null check (status in ('draft','approved')) default 'draft',
  approved_by uuid references users(id),
  approved_at timestamptz,
  exported_to_bitrix_bool boolean not null default false
);

create table approvals (
  id uuid primary key,
  object_type text not null,
  object_id uuid not null,
  requested_by uuid not null references users(id),
  requested_at timestamptz not null default now(),
  state text not null check (state in ('pending','approved','rejected')) default 'pending',
  approver_id uuid references users(id),
  approved_at timestamptz,
  comment text
);

create table audit_log (
  id uuid primary key,
  actor_id uuid references users(id),
  role text,
  ts timestamptz not null default now(),
  action text not null,
  object_type text not null,
  object_id uuid,
  old_new_diff_json jsonb,
  sig_hash text not null
) partition by range (date(ts));

create table gate_log (
  id uuid primary key,
  gate_type text not null,        -- vt_limit, degaz_gate, calibration_expired, etc.
  object_ref jsonb,
  ts timestamptz not null default now(),
  released_at timestamptz,
  released_by uuid references users(id),
  note text
);
create index idx_gates_open on gate_log(gate_type, released_at) where released_at is null;

create table alerts (
  id uuid primary key,
  severity text not null check (severity in ('P1','P2','P3')),
  metric_code text not null,       -- rs_trusted_ratio, loss_pct, delta_session
  value numeric(14,3),
  threshold numeric(14,3),
  ts timestamptz not null default now(),
  routed_to uuid[] not null,
  status text not null check (status in ('open','ack','closed')) default 'open',
  closed_at timestamptz
);

```

---

## 17) Wireframe/Wizard oqimlari (matnli tavsif)

> Maqsad — ishlab chiquvchi uchun UI oqimlarini aniq ko‘rsatish. Har ekranda asosiy vidjetlar, validatsiya va xatolik holatlari tasvirlanadi.
> 

### 17.1. M1: Main → Shop transfer wizard

1. **So‘rov tanlash** (sex boshlig‘i yaratgan): SKU/retsept asosida material ro‘yxati.
2. **Batch tanlash**: FIFO bo‘yicha avtomatik taklif; operator o‘zgartira oladi.
3. **RS tortish**: har line uchun `device_id` tanlanadi, “Oxirgi stable o‘qish” labeli. **Manual kiritish yo‘q** (strict).
4. **Yakun**: ko‘rinish — `MAIN−` jurnal, status `in_transit`, printerga jo‘natish (ixtiyoriy).

**Xato holatlari:** `calibration_expired` banner; RS yo‘q — “Gateway offline” modal.

### 17.2. M2: Shop snapshot & qaytarish

- **Snapshot**: stok grid (material/batch/qty), har satrda **RS tortish** tugmasi; “Smena yakunlandi” checkbox.
- **Qaytarish**: “Shop → Main” wizard M1 bilan bir xil (RS–RS).

### 17.3. M3: Sessiya yaratish

- Form: Workcenter (E1/E2/E3), SKU, partiya_no, shift, operator(≤2), **retsept snapshot preview**.
- Gate indikator: `>2_extruder`, `e3_qualification`.
- `Start` → sessiya panel (input/good/wip/scrap live).

### 17.4. M5: Qadoqlash ekrani

- Kiosk layout: katta **RS vazn** display (read-only), uzunlik (Auto/Manual switch).
- **Tolеранs**: normadan og‘ish bo‘lsa sariq “Review required” banner, “Submit for review”.
- `Create` → QR preview/print.
- Tarix paneli: so‘nggi N paket (status, QC, QR).

### 17.5. M6: OTK navbat

- Chap: `awaiting_qc` ro‘yxat (filtr: E1/E2/E3/SKU/partiya).
- O‘ng: paket detali, protokol formasi, `ok/partial/reject`, e-pechat sign maydoni.
- `partial` → “Split package” wizard (OK qism va Reject qism RS bilan qayta tortish talab qilinmaydi — massalashuvni suratga olish bilan cheklanadi, ammo istasak RS qayta o‘qish tugmasi).

### 17.6. M7: Sessiya yopish/Investigate

- “Preview balans” karta: input/good/wip/scrap_expected + linked rework/dispose/outstanding.
- **Delta vizual**: progress bar, limit chizig‘i.
- Drill-down: snapshot log, paketlar, rework linklari, RS eventlar.
- Tugmalar: `Close`, `Investigate`, `Re-open` (approve oqimi).

### 17.7. M8: Rework IN/OUT

- IN: konteyner skan (seal), **RS IN** tortish, “Konteyner qo‘shish” tugmasi.
- OUT: **RS OUT** tortish, VT SKU tanlash (default VT), “Loss%” avtomatik ko‘rsatkich.

### 17.8. M9: FG qabul

- Skanner maydoni (QR fokus), natija karta: paket, QC OK, degaz status.
- Xatolar: `qc_not_ok_to_fg`, `qr_duplicate`, `degaz_gate` — qizil banner, “OnHold” tugmasi.
- FG ro‘yxat: partiya / sana bo‘yicha filtrlar.

### 17.9. M10/M11: Integratsiya & Payroll panel

- Integratsiya: Queue jadvali (pending/error/sent), retry tugmasi, mapping editor.
- KPI/Payroll: ‘Generate’ → ‘Approve’ → ‘Export to Bitrix’ tugmalari; ko‘rsatkichlar kartalari.

---

## 18) SOP “bir sahifalik” (rol bo‘yicha)

> Har SOP: 60–90 soniyalik tekshiruv chek-listi.
> 

**Main omborchi (M1)**

- [ ]  Batch FIFO tanlandi
- [ ]  Har line RS tortildi (kalibrovka OK)
- [ ]  Jo‘natma “in transit” ga o‘tdi

**Shop operatori (M1/M2)**

- [ ]  Qabul RS bilan
- [ ]  Smena oxiri snapshot RS
- [ ]  Ortiqcha material qaytarildi (RS–RS)

**Sex boshlig‘i (M3/M5/M7)**

- [ ]  Sessiya: operator(≤2), malaka OK
- [ ]  Review/Manual kiritmalarni ko‘rib tasdiqladi
- [ ]  Δ ≤ limit — `Close` yoki `Investigate`

**Operator (M5)**

- [ ]  Vazn RS (qo‘lda emas)
- [ ]  Uzunlik Auto (manual bo‘lsa sabab yozildi)
- [ ]  Tolerans breach — review yuborildi

**OTK (M6)**

- [ ]  Navbat → Protokol
- [ ]  e-pechat qo‘yildi
- [ ]  `ok/partial/reject` qaror aniq qayd

**Drabilka (M8)**

- [ ]  IN RS, OUT RS
- [ ]  Loss% ko‘rildi, yuqori bo‘lsa xabar

**FG omborchi (M9)**

- [ ]  QR skan → OK
- [ ]  Gate xatolar bo‘lsa OnHold

**Moliya (M11)**

- [ ]  KPI/Payroll snapshot → approve
- [ ]  Bitrix eksport → sent

---

## 19) Muhim algoritmlar (pseudokod)

### 19.1. RS binding (M5/M1/M2/M8)

```
function bind_latest_stable(device_id, bind_to, window_sec=IOT_ACCEPT_WINDOW_SEC):
    now = utcnow()
    ev = ScaleEvent.where(device_id=device_id, stable=True)
                   .order_by(ts_ingested DESC)
                   .first()
    if not ev or (now - ev.ts_ingested) > window_sec:
        return error("rs_not_found_in_window")
    ev.bind_ref = bind_to   # {"package_id":..., ...}
    save(ev)
    return ev.gross_kg, ev.id

```

### 19.2. Tolerans tekshiruvi (M5)

```
function tolerance_check(sku, weight_kg, length_m?):
    norm_w = expected_weight_per_package(sku, length_m)  # kg_per_m yoki kg_per_m2'dan
    diff_pct = abs(weight_kg - norm_w) / norm_w * 100
    if diff_pct <= sku.tolerance_weight_pct:
        return "ok"
    return "review"

```

### 19.3. Mass-balans va yopish (M7)

```
scrap_expected = input_kg - good_kg - wip_kg
linked_total  = rework_in_linked_kg + disposed_linked_kg + outstanding_kg
delta = abs(scrap_expected - linked_total)
limit = min(0.01 * input_kg, 5.0)
if delta <= limit:
    close_session()
else:
    raise Conflict("delta_exceeded", delta, limit)

```

### 19.4. VT FIFO linklash (M8 → M7)

```
function fifo_link(vt_batch_id, session_id, qty_kg):
    rem = qty_kg
    for scrap in session.scrap_outstanding_ordered_by_time():
        take = min(scrap.remaining_kg, rem)
        create_link(vt_batch_id, scrap.id, take)
        scrap.remaining_kg -= take
        rem -= take
        if rem == 0: break
    if rem > 0:
        return warning("vt_excess", rem)
    return ok

```

### 19.5. Gate baholash (umumiy)

```
function enforce_gate(context):
    if device.calibration_due_at < now: block("calibration_expired")
    if session.vt_ratio > recipe.vt_limit_pct: pause("vt_limit")  # Texnolog release qiladi
    if sku.degaz_required and sku.degaz_status == "pending": block("degaz_gate")
    if operator.assigned_lines > 2: block(">2_extruder")

```

### 19.6. Integratsiya retry (queue)

```
function retry_policy(q):
    delay = [60s, 300s, 900s, 3600s, 14400s]  # 1m,5m,15m,1h,4h
    if q.retry_count >= len(delay): escalate("integration_backlog")
    else schedule(now + delay[q.retry_count])

```

---

## 20) Kuzatuv va telemetriya

### 20.1. Metrik nomlari

- `api_http_request_duration_seconds{route,method,status}` (histogram)
- `ingest_events_total{device_id,status}` — accepted/duplicate/late
- `gate_hits_total{gate_type}` — vt_limit, degaz, calibration_expired…
- `rs_trusted_ratio` — trusted/(trusted+manual)
- `rework_loss_pct{type}` — soft/hard
- `session_delta_kg{workcenter}`
- `integration_queue_backlog{status}`

### 20.2. Loglar

- Har biznes amal: `trace_id`, foydalanuvchi, obyekt ID, natija.
- Xatolar: `error_code`, `gate_blocked`, `business_conflict`.
- Audit: `sig_hash` bilan alohida saqlanadi.

### 20.3. Alertlar

- `P1`: Ingest to‘xtadi (no events > 2 min), DB down.
- `P2`: rs_trusted_ratio < 95%, integration backlog > 100.
- `P3`: rework_loss > 15%, Δ trend ko‘tarilmoqda.

---

## 21) Ma’lumot sifati qoidalari

- **Unikal**: `packages.qr_code`, `(device_id,seq)`.
- **Xatolik**: manfiy qty/vazn, mantiqsiz UOM kombinatsiyasi → 422.
- **Konsistensiya**: `material_id XOR sku_id` (StockItem/Txn).
- **Qo‘lda kiritma**: KPI’dan default **chiqariladi** (Sex boshlig‘i override qilmaguncha).
- **OnHold**: FG’da dublikat/gate bo‘lsa; release protokoli auditlanadi.
- **Degazatsiya**: `pending` bo‘lsa QC/FG blok — SKU flag majburiy.

---

## 22) Migratsiya/Seed konvensiyalari

- **Migratsiya nomlari:** `YYYYMMDDHHMM_<short_desc>.py`
- **Seed CSV ustunlari (namuna):**
    - `skus.csv`: `code,name,category,uom_default,width_mm,thickness_mm,kg_per_m2,mesh_type,tolerance_weight_pct,tolerance_length_pct,degaz_required_bool`
    - `materials.csv`: `code,name,category,polymer_family,recyclable_bool`
    - `recipes.csv` / `recipe_lines.csv`
    - `workcenters.csv`, `devices.csv` (device_id, workcenter_code, type, serial, calibration_due_at)
- **Import validatsiyasi:** ustunlar to‘liq, enum qiymatlar yaroqli, `code` lar unique.

---

## 23) Enum va lug‘atlar (to‘plam)

- **positions**: direktor, texnolog, sex_boshligi, operator, shop_op, main_ombor, fg_ombor, otk, moliya, integrator
- **workcenter.type**: extruder, coater, laminator, duplicator, cutter, rework_hard, rework_soft
- **device.type**: scale, length_counter
- **sku.category**: polotno, setka, ot, js, profil, lam_out, dubl, kesilgan, izdeliya, vt
- **stock_txn.type**: MAIN_TO_SHOP, SHOP_TO_MAIN, SHOP_SNAPSHOT, SHOP_TO_SESSION, FG_RECEIVE, REWORK_VT_IN, DISPOSE_WASTE
- **session.status**: opened, paused, closed
- **package.status**: awaiting_qc, qc_ok, qc_reject, qc_partial
- **qc.decision**: ok, partial, reject
- **degaz_status**: pending, done
- **approval.state**: pending, approved, rejected
- **gate.type**: vt_limit, degaz_gate, calibration_expired, gt_2_extruder, e3_qualification, qc_not_ok_to_fg, non_recyclable_to_rework, qr_duplicate

---

## 24) UAT test ma’lumot to‘plami (minimal)

- **SKUs**:
    - `POL-10` (polotno, kg_per_m2=0.120, tol_w=2%)
    - `SET-05` (setka, tol_w=3%)
- **Materials**: `PVD-PE`, `VT-PE`, `MB-RED` (additiv), `TALK` (additiv)
- **Recipes**: `POL-10 v1` (PVD 60%, VT 30%, MB 5%, TALK 5%, vt_limit=35%)
- **Workcenters/Devices**: E1,E2,E3 + `scale-E1-pack-01`, `scale-MAIN-01`, `scale-SHOP-01`, `scale-RW-IN-01`, `scale-RW-OUT-01` (kalibrovka amal qiladi)
- **Users**: 2 operator (katta), 1 sex_boshligi, 1 otk, 1 main_ombor, 1 shop_op, 1 fg_ombor, 1 texnolog, 1 moliya, 1 direktor
- **Bitrix stub**: 5 ta xodim, 2 ta order, attendance haftalik