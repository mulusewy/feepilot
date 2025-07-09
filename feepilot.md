You are a SR deloper working on a we app. Build a full-stack MVP web application for **FeePilot**, a real-time PSP fee simulator for online merchants. Follow the instructions below exactly.

---

## 1. 🧠 Overview

**FeePilot MVP Purpose**:  
A no-login, web-based calculator to compare transaction fees, FX costs, and hidden surcharges across Stripe, PayPal, Square, and Wise. The goal is to help merchants quickly decide which PSP yields the highest net revenue.
## DO NOT COPY ANY FILES FROM ANOTHER DEVELOPMENT PROJECT!!!!
## PLEASE ask to to start the dev server for front and back end!! dont not try to run the dev server, you dont have permissions!!!!

---

## 2. 💻 Tech Stack

- **Frontend**: React + Vite + Tailwind CSS (with hardcoded utility classes)
- **Backend**: FastAPI + Uvicorn (Python)
- **FX**: Use Wise API for real-time exchange rates
- **Auth**: Admin login only (JWT)
- **Data**: In-memory or SQLite DB for MVP

---

## 3. ✨ Styling Requirements

Style the UI **exactly like** the design of https://vercel.saasstarter.work. But **DO NOT rely on any shared theme config** — use hardcoded Tailwind classes directly in components.

### 🎨 Tailwind Styling (hardcoded only):
please use the styleing from the cloed website CriticalMoments/CMSaasStarter

### UI Components:
- **Buttons**:
  - Primary: `please use the styleing from the cloed website CriticalMoments/CMSaasStarter`
  - Secondary: `please use the styleing from the cloed website CriticalMoments/CMSaasStarter`
- **Cards**: `please use the styleing from the cloed website CriticalMoments/CMSaasStarter`
- **Inputs**: `please use the styleing from the cloed website CriticalMoments/CMSaasStarter`
- **Layout**: please use the styleing from the cloed website CriticalMoments/CMSaasStarter
All components must be mobile-first and responsive.

---

## 4. 📄 Pages to Generate

### 1. **Home / Landing Page**
- Hero section with CTA: "Start Simulation"
- Features section
- PSP logos section
- Sticky nav + footer

### 2. **Simulation Page (Core Feature)**
> This is the main calculator. But first, collect user data.

#### Step 1: User Info Form (required before simulation)
- Collect: First Name, Last Name, Email, Phone Number
- Show this form in a modal or top-of-page block
- Validate fields (email format, required, phone pattern)
- Submit to backend: `POST /submit-user`
- After submission: reveal the calculator section (smooth scroll or toggle)

#### Step 2: Transaction Fee Calculator
- Inputs:
  - Transaction Amount
  - Currency (dropdown)
  - Merchant Country
  - Customer Country
  - Payment Method (card, ACH, bank, etc.)
  - Day of Week (toggle weekday/weekend)
  - Optional Markup (% or flat)
  - PSPs to Compare (multi-select: Stripe, PayPal, Square, Wise)

- Calculate button
- Shows result in dashboard/cards below

### 3. **Comparison Dashboard**
- Side-by-side cards for each PSP
- Each card shows:
  - Effective rate (%)
  - Fixed & variable fee breakdown
  - FX cost (if needed)
  - Weekend/cross-border surcharges
  - Net revenue
- Highlight best net revenue with badge
- Visual warning icons for hidden fees

### 4. **Admin Login + Dashboard**
- Email + password login (`POST /admin/login`)
- Admin panel:
  - View collected user submissions
  - Upload and manage Google & Facebook pixel scripts
  - Toggle tracking embed for frontend
  - JWT-based route protection for admin APIs

---

## 5. 🔐 Backend API (FastAPI)

### General Rules
- Use `pydantic` for input validation
- Use environment variables (`os.getenv`) for secrets (Wise API key)
- Rate-limit `POST /simulate` and `POST /submit-user` (e.g. 5 req/min per IP)
- **DO NOT expose `/docs` or `/redoc` in production**
- Use `allow_origins` in CORS to only accept requests from `http://localhost:5173` (for dev) or production domain
- Enable CORS, HTTPS redirection middleware in production

### Endpoints to Implement

```py
POST /submit-user
- Payload: first name, last name, email, phone
- Store in memory or SQLite (later use for analytics)

POST /simulate
- Payload: transaction details and PSP selections
- Logic:
  - Load static fee matrix for each PSP
  - Pull real-time FX rate from Wise API if needed
  - Add surcharges for weekend or cross-border
  - Apply any custom markup
  - Return breakdown for each PSP

POST /admin/login
- Authenticate admin, return JWTok

GET /admin/simulations
- Protected: return all collected user info

POST /admin/tracking
- Protected: accepts tracking script code (Google Ads, FB Pixel)
- Store in backend memory or DB
- Frontend reads and injects script into `<head>`


## Error from developers tools i am seeing ## 
==> Cloning from https://github.com/mulusewy/feepilot
==> Checking out commit 314627fef11847c17c6c093cb3278481b96032b0 in branch main
==> Using Node.js version 22.16.0 (default)
==> Docs on specifying a Node.js version: https://render.com/docs/node-version
==> Using Bun version 1.1.0 (default)
==> Docs on specifying a Bun version: https://render.com/docs/bun-version
==> Running build command 'npm install; npm run build'...
added 395 packages, and audited 396 packages in 5s
91 packages are looking for funding
  run `npm fund` for details
4 low severity vulnerabilities
To address issues that do not require attention, run:
  npm audit fix
To address all issues (including breaking changes), run:
  npm audit fix --force
Run `npm audit` for details.
> cmsassstarter@0.0.1 build
> vite build
▲ [WARNING] Cannot find base config file "./.svelte-kit/tsconfig.json" [tsconfig.json]
    tsconfig.json:2:13:
      2 │   "extends": "./.svelte-kit/tsconfig.json",
        ╵              ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
vite v6.3.5 building SSR bundle for production...
transforming...
✓ 30 modules transformed.
✗ Build failed in 363ms
error during build:
Could not resolve "../../../../(marketing)/pricing/pricing_plans" from "src/routes/(admin)/account/(menu)/billing/+page.svelte"
file: /opt/render/project/src/src/routes/(admin)/account/(menu)/billing/+page.svelte
    at getRollupError (file:///opt/render/project/src/node_modules/rollup/dist/es/shared/parseAst.js:397:41)
    at error (file:///opt/render/project/src/node_modules/rollup/dist/es/shared/parseAst.js:393:42)
    at ModuleLoader.handleInvalidResolvedId (file:///opt/render/project/src/node_modules/rollup/dist/es/shared/node-entry.js:21111:24)
    at file:///opt/render/project/src/node_modules/rollup/dist/es/shared/node-entry.js:21071:26
==> Build failed 😞
==> Common ways to troubleshoot your deploy: https://render.com/docs/troubleshooting-deploys