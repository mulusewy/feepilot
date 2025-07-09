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
PS C:\Windows\system32> cd C:\Users\Yemane\Desktop\feepilot_2.0\backend
PS C:\Users\Yemane\Desktop\feepilot_2.0\backend>  uvicorn main:app --reload
←[32mINFO←[0m:     Will watch for changes in these directories: ['C:\\Users\\Yemane\\Desktop\\feepilot_2.0\\backend']
←[32mINFO←[0m:     Uvicorn running on ←[1mhttp://127.0.0.1:8000←[0m (Press CTRL+C to quit)
←[32mINFO←[0m:     Started reloader process [←[36m←[1m15312←[0m] using ←[36m←[1mStatReload←[0m
Process SpawnProcess-1:
Traceback (most recent call last):
  File "C:\Users\Yemane\AppData\Local\Programs\Python\Python313\Lib\multiprocessing\process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "C:\Users\Yemane\AppData\Local\Programs\Python\Python313\Lib\multiprocessing\process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Yemane\AppData\Local\Programs\Python\Python313\Lib\site-packages\uvicorn\_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "C:\Users\Yemane\AppData\Local\Programs\Python\Python313\Lib\site-packages\uvicorn\server.py", line 67, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Yemane\AppData\Local\Programs\Python\Python313\Lib\asyncio\runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "C:\Users\Yemane\AppData\Local\Programs\Python\Python313\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "C:\Users\Yemane\AppData\Local\Programs\Python\Python313\Lib\asyncio\base_events.py", line 725, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "C:\Users\Yemane\AppData\Local\Programs\Python\Python313\Lib\site-packages\uvicorn\server.py", line 71, in serve
    await self._serve(sockets)
  File "C:\Users\Yemane\AppData\Local\Programs\Python\Python313\Lib\site-packages\uvicorn\server.py", line 78, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "C:\Users\Yemane\AppData\Local\Programs\Python\Python313\Lib\site-packages\uvicorn\config.py", line 436, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "C:\Users\Yemane\AppData\Local\Programs\Python\Python313\Lib\site-packages\uvicorn\importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "C:\Users\Yemane\AppData\Local\Programs\Python\Python313\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "C:\Users\Yemane\Desktop\feepilot_2.0\backend\main.py", line 48, in <module>
    "hashed_password": pwd_context.hash("adminpass") # TODO: Change this in production
                       ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "C:\Users\Yemane\AppData\Local\Programs\Python\Python313\Lib\site-packages\passlib\context.py", line 2258, in hash
    return record.hash(secret, **kwds)
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^
  File "C:\Users\Yemane\AppData\Local\Programs\Python\Python313\Lib\site-packages\passlib\utils\handlers.py", line 779, in hash
    self.checksum = self._calc_checksum(secret)
                    ~~~~~~~~~~~~~~~~~~~^^^^^^^^
  File "C:\Users\Yemane\AppData\Local\Programs\Python\Python313\Lib\site-packages\passlib\handlers\bcrypt.py", line 591, in _calc_checksum
    self._stub_requires_backend()
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "C:\Users\Yemane\AppData\Local\Programs\Python\Python313\Lib\site-packages\passlib\utils\handlers.py", line 2254, in _stub_requires_backend
    cls.set_backend()
    ~~~~~~~~~~~~~~~^^
  File "C:\Users\Yemane\AppData\Local\Programs\Python\Python313\Lib\site-packages\passlib\utils\handlers.py", line 2156, in set_backend
    return owner.set_backend(name, dryrun=dryrun)
           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Yemane\AppData\Local\Programs\Python\Python313\Lib\site-packages\passlib\utils\handlers.py", line 2176, in set_backend
    raise default_error
passlib.exc.MissingBackendError: bcrypt: no backends available -- recommend you install one (e.g. 'pip install bcrypt')