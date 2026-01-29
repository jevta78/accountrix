# Accountrix

Accountrix je **web-first SaaS aplikacija** za kreiranje i upravljanje fakturama, namenjena:
- freelancerima i individualnim korisnicima
- outsourcing agencijama
- timovima sa approval workflow-om
- kasnije enterprise korisnicima (bank reconciliation, Stripe)

Aplikacija se razvija **korak po korak**, sa fokusom na:
- čist domain model
- skalabilnu arhitekturu
- production-ready Django praksu
- minimalan tehnički dug

---

## 🎯 Vizija aplikacije

Accountrix rešava sledeće probleme:
- jednostavno kreiranje faktura
- jasno razdvajanje **identiteta korisnika** i **poslovnog konteksta**
- podršku za:
  - personal (freelancer) fakturisanje
  - interno fakturisanje unutar outsourcing kompanija
- kasnije:
  - approval tokove
  - bank statement reconciliation
  - Stripe integraciju
  - SaaS planove (free / corporate tiers)

Ključni cilj je da aplikacija:
- ne zaključava korisnika u jedan tip naloga
- omogućava rast od MVP-a do ozbiljnog proizvoda

---

## 🧠 Ključne arhitektonske odluke

### 1. User ≠ Company (Organization)

Najvažnija odluka u aplikaciji:

- **User** je uvek fizičko lice (email + password)
- **Company / Organization** (kasnije) je poslovni entitet

User:
- može postojati bez kompanije
- može biti član više kompanija
- može imati različite uloge po kompaniji

Nikada ne vezujemo `User` direktno za jednu kompaniju.

Ovo je industrijski standard (Stripe, GitHub, Notion).

---

### 2. Custom User model od prvog dana

Od samog starta koristimo **custom User model**:

- login preko **email + password**
- bez `username` polja
- spremno za:
  - invite-based signup
  - email verifikaciju
  - corporate onboarding

Ova odluka eliminiše potrebu za kasnijim refaktorom auth sistema.

---

### 3. Razdvajanje profila od User modela

`User` model je **namerno minimalan**.

Podaci su podeljeni u posebne modele:

#### UserProfile
- lični podaci korisnika
- ime, prezime, telefon
- onboarding status

#### BusinessProfile
- podaci koji se koriste na fakturama
- naziv firme / freelancera
- adresa, država
- IBAN, SWIFT

Ovo omogućava:
- čist domain model
- kasnije lako uvođenje organizacija
- fleksibilan invoice sender sistem

---

## 🏗️ Tehnološki stack (trenutno)

- Python 3.13
- Django 5+
- SQLite (dev)
- PostgreSQL (planirano)
- **uv** – virtual environment & dependency management
- VS Code
- Django Admin (backoffice)
- Django Templates (web-first UI)

---

## 📁 Struktura projekta

---

## 🧪 Development workflow

### Virtual environment & komande

Koristimo **uv** umesto klasičnog `virtualenv` + `pip`.

Kreiranje venv-a:
```bash
uv venv