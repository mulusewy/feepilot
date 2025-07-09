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
==> Checking out commit 17cb50483d2ce6c32ef30c853d6834af57d0da16 in branch main
==> Using Node.js version 22.16.0 (default)
==> Docs on specifying a Node.js version: https://render.com/docs/node-version
==> Using Bun version 1.1.0 (default)
==> Docs on specifying a Bun version: https://render.com/docs/bun-version
==> Running build command 'npm install; npm run build'...
added 434 packages, and audited 435 packages in 5s
105 packages are looking for funding
  run `npm fund` for details
3 low severity vulnerabilities
To address all issues, run:
  npm audit fix
Run `npm audit` for details.
> cmsassstarter@0.0.1 build
> vite build
▲ [WARNING] Cannot find base config file "./.svelte-kit/tsconfig.json" [tsconfig.json]
    tsconfig.json:2:13:
      2 │   "extends": "./.svelte-kit/tsconfig.json",
        ╵              ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
vite v6.3.5 building SSR bundle for production...
transforming...
/*! 🌼 daisyUI 5.0.0 */
✓ 261 modules transformed.
✗ Build failed in 1.84s
error during build:
src/routes/(admin)/account/subscription_helpers.server.ts (4:9): "PRIVATE_STRIPE_API_KEY" is not exported by "virtual:env/static/private", imported by "src/routes/(admin)/account/subscription_helpers.server.ts".
file: /opt/render/project/src/src/routes/(admin)/account/subscription_helpers.server.ts:4:9
2: import type { Database } from "../../../DatabaseDefinitions"
3: 
4: import { PRIVATE_STRIPE_API_KEY } from "$env/static/private"
            ^
5: import Stripe from "stripe"
6: import { pricingPlans } from "../../(marketing)/pricing/pricing_plans"
    at getRollupError (file:///opt/render/project/src/node_modules/rollup/dist/es/shared/parseAst.js:397:41)
    at error (file:///opt/render/project/src/node_modules/rollup/dist/es/shared/parseAst.js:393:42)
    at Module.error (file:///opt/render/project/src/node_modules/rollup/dist/es/shared/node-entry.js:16603:16)
    at Module.traceVariable (file:///opt/render/project/src/node_modules/rollup/dist/es/shared/node-entry.js:17052:29)
    at ModuleScope.findVariable (file:///opt/render/project/src/node_modules/rollup/dist/es/shared/node-entry.js:14709:39)
    at Identifier.bind (file:///opt/render/project/src/node_modules/rollup/dist/es/shared/node-entry.js:5356:40)
    at NewExpression.bind (file:///opt/render/project/src/node_modules/rollup/dist/es/shared/node-entry.js:2779:28)
    at VariableDeclarator.bind (file:///opt/render/project/src/node_modules/rollup/dist/es/shared/node-entry.js:2783:23)
    at VariableDeclaration.bind (file:///opt/render/project/src/node_modules/rollup/dist/es/shared/node-entry.js:2779:28)
    at Program.bind (file:///opt/render/project/src/node_modules/rollup/dist/es/shared/node-entry.js:2779:28)
    at Module.bindReferences (file:///opt/render/project/src/node_modules/rollup/dist/es/shared/node-entry.js:16582:18)
    at Graph.sortModules (file:///opt/render/project/src/node_modules/rollup/dist/es/shared/node-entry.js:22130:20)
    at Graph.build (file:///opt/render/project/src/node_modules/rollup/dist/es/shared/node-entry.js:22028:14)
    at async file:///opt/render/project/src/node_modules/rollup/dist/es/shared/node-entry.js:22721:13
    at async catchUnfinishedHookActions (file:///opt/render/project/src/node_modules/rollup/dist/es/shared/node-entry.js:22187:16)
    at async rollupInternal (file:///opt/render/project/src/node_modules/rollup/dist/es/shared/node-entry.js:22716:5)
    at async buildEnvironment (file:///opt/render/project/src/node_modules/vite/dist/node/chunks/dep-DBxKXgDP.js:46206:14)
    at async Object.defaultBuildApp [as buildApp] (file:///opt/render/project/src/node_modules/vite/dist/node/chunks/dep-DBxKXgDP.js:46684:5)
    at async CAC.<anonymous> (file:///opt/render/project/src/node_modules/vite/dist/node/cli.js:863:7)
==> Build failed 😞
==> Common ways to troubleshoot your deploy: https://render.com/docs/troubleshooting-deploys