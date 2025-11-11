# 4-WEEK BUILD PLAN
## Complete Customer Retention System for Kenyan Salons

**Last Updated:** 2025-11-04
**Timeline:** 4 weeks
**First Customers:** Maloy Salon + VIP Nail Spa (both committed at 1,000 KES/month)

---

## THE DAILY RHYTHM

**How we work together each day:**

### 1. Claude Prepares (5 min)
- I read the relevant documentation (django-tenants, SMS APIs, etc.)
- I identify the key concepts/methods you need to know

### 2. You Read (10 min)
- I tell you: "Read these 3 key concepts in the docs"
- You read and absorb the essentials
- Focus on WHAT and WHY, not memorizing syntax

### 3. We Discuss (10-15 min)
- I ask: "What did you understand?"
- We talk through the approach
- Decide: Do you get it well enough to proceed?
- I explain what CANNOT be automated (architectural decisions)

### 4. We Implement (2-3 hours)
- Work together to build the feature
- You understand WHAT we're building at each step
- I generate syntax/boilerplate (what CAN be automated)
- You review and ask "why this way?"

### 5. You Must Understand (15 min)
- Before committing, explain back to me what we built
- If unclear, we discuss until it clicks
- This is non-negotiable

### 6. Commit & Move On (5 min)
```bash
git add .
git commit -m "feat: [what we built] - [what you learned]"
```

---

## WHAT WE'RE BUILDING

**Two-part solution:**
1. **Public Website** (Frontend) - For salon's customers to see
2. **Admin Panel** (Backend) - For salon owner to manage retention

**Value Proposition:**
- Salons get online presence (website as hook)
- Salons get retention system (core value - keep customers coming back)

---

## PART 1: PUBLIC WEBSITE (Frontend)

**Single-page website for each salon:**

### Hero Section
- **Google Local Ratings** (social proof)
  - Display star rating + review count
  - Link to Google Business Profile

### Primary Actions
- **Book Now Button** → WhatsApp or call
- **Contact Now Button** → Direct contact links

### Products/Services Catalog
- Display services (e.g., "Haircut - 500 KES")
- With images and prices

### Social Media Links
- Instagram, Facebook, TikTok, WhatsApp Business

### Posts/Updates Section
- New items/services
- Trending styles
- Special offers

**Tech:** Next.js + Tailwind, mobile-first, PWA-enabled

---

## PART 2: ADMIN PANEL (Backend)

**Salon owner's retention management system:**

### A) Customer Management
- **Import contacts** from CSV/phone
- **Tag customers:** VIP, Regular, New, Lost
- Full customer database per salon

### B) Daily Outreach System
- **Schedule 3-10 SMS** to customers (Celcom API)
- Pre-written message templates
- **Copy to WhatsApp button** (manual sending)
- **Schedule 1-2 phone calls** to VIP/Lost customers

### C) Activity Tracking
- **Manual check-in** when customer arrives
- **Referral tracking** (who referred whom)
- Track visit frequency

### D) Follow-up System
- **Post-service SMS** (2-3 days later)
- "How was your haircut? Rate 1-5 stars"
- Track satisfaction scores

### E) M-Pesa Integration
- **Scrape M-Pesa SMS** automatically
- Parse: "Received KES 1,500 from JANE..."
- Auto-link payment to customer
- Update last visit date automatically

### F) Retention Dashboard
**Key metrics displayed:**
- Last contacted date (per customer)
- Last check-in date (per customer)
- Customers not back in 30+ days (warning)
- Customers not back in 90+ days (lost)
- Last phone call tracking
- Active vs Lost customers (visual chart)
- Win-back campaign tracking

---

## TECH STACK

**Backend:**
- Django + django-tenants (multi-tenant architecture)
- PostgreSQL (required for schemas)
- Celery (scheduled tasks)
- Celcom Africa SMS API

**Frontend (Public Website):**
- Next.js + Tailwind CSS
- PWA-enabled (installs like app)
- Server-side rendering

**Frontend (Admin Panel):**
- Next.js + Tailwind CSS
- Charts/graphs for dashboard
- Mobile-responsive

**Integrations:**
- M-Pesa: SMS parsing → Daraja API later
- Google Local: Ratings widget
- WhatsApp: Direct links (no API)

---

## 4-WEEK BUILD TIMELINE

### WEEK 1: Backend Foundation

#### Day 0: SMS Provider Test
**Before building anything:**
- Sign up for Celcom Africa (free 50 SMS)
- Send test SMS to your phone
- Send test SMS to both salon owners
- Verify: Do they receive it?
- If yes → proceed. If no → try Africa's Talking

#### Day 1: Django-Tenants Setup
**Goal:** Understand multi-tenant architecture

**What you'll learn:**
- How tenant isolation works (separate PostgreSQL schemas)
- Why this matters (salon data never mixes)
- What breaks if you mess it up

**What we'll build:**
- Django project with django-tenants installed
- Tenant model (Salon)
- First tenant created (Maloy Salon)
- Test: Can we access Maloy's isolated database?

#### Day 2: Customer Database Model
**Goal:** Build core customer tracking

**What you'll learn:**
- Django models for tenant-specific data
- What fields salons actually need

**What we'll build:**
- Customer model (name, phone, last_visit, tags, etc.)
- Admin interface to add customers
- Test: Add 5 test customers for Maloy

#### Day 3: SMS Integration
**Goal:** Send first automated SMS

**What you'll learn:**
- How SMS APIs work (Celcom Africa)
- Sending SMS from Django

**What we'll build:**
- SMS service integration
- Function to send reminder SMS
- Test: Send SMS to your own phone

#### Day 4-5: "Who to Contact" Logic
**Goal:** Salon's #1 requested feature

**What you'll learn:**
- Django queries for "not seen in 30+ days"
- Scheduling automated tasks

**What we'll build:**
- Query: Find customers who haven't visited in X days
- Automatic SMS trigger (daily check)
- Dashboard view: "Contact these customers today"
- Test: Does it identify the right customers?

#### Day 6-7: Customer Tagging & Manual Check-in
**Goal:** Basic retention tracking

**What you'll learn:**
- Django admin customization
- Updating records via forms

**What we'll build:**
- Tag customers (VIP, Regular, New, Lost)
- "Check-in customer" button
- Updates last_visit date
- Test: Check in a customer, verify date updates

---

### WEEK 2: M-Pesa & Dashboard

#### Day 8-9: M-Pesa SMS Parsing
**Goal:** Automatic visit tracking

**What you'll learn:**
- Parsing structured text (M-Pesa format)
- Matching payments to customers

**What we'll build:**
- M-Pesa SMS parser (regex/AI)
- Link payment to customer by phone/name
- Auto-update last_visit when payment received
- Test: Simulate M-Pesa SMS, verify customer updated

#### Day 10-11: Retention Dashboard (Backend)
**Goal:** Show salon owner key metrics

**What you'll learn:**
- Django aggregation queries
- Calculating date ranges (30+ days, 90+ days)

**What we'll build:**
- Dashboard endpoint (Django REST API)
- Queries:
  - Customers not seen in 30+ days
  - Customers not seen in 90+ days
  - Active vs Lost count
  - Last contacted date per customer
- Test: API returns correct data

#### Day 12-14: Referral & Follow-up System
**Goal:** Track word-of-mouth + satisfaction

**What you'll learn:**
- ForeignKey relationships (referrals)
- Scheduled SMS (post-service follow-up)

**What we'll build:**
- Referral tracking (Jane referred by Sarah)
- Post-service SMS (2-3 days after visit)
- "Rate your service 1-5" tracking
- Test: Send follow-up SMS, track response

---

### WEEK 3: Frontend (Admin Panel + Public Website)

#### Day 15-16: Admin Panel - Login & Customer List
**Goal:** Salon owner can see their customers

**What you'll learn:**
- Next.js basics (just enough)
- Connecting to Django API
- Authentication (JWT tokens)

**What we'll build:**
- Login page (salon owner)
- Customer list view (from Django API)
- Show: Name, phone, last visit, tags
- Test: Login as Maloy, see their customers

#### Day 17-18: Admin Panel - Dashboard View
**Goal:** Visual retention metrics

**What you'll learn:**
- React components (basic)
- Charts/graphs (simple library)

**What we'll build:**
- Dashboard page with metrics:
  - Customers to contact today (30+ days)
  - Lost customers (90+ days)
  - Active vs Lost chart
- "Send SMS" button (triggers Django API)
- Test: Click "Send SMS", verify SMS sent

#### Day 19-20: Admin Panel - Check-in & Tags
**Goal:** Daily salon operations

**What we'll learn:**
- Forms and PUT requests
- Updating records from frontend

**What we'll build:**
- "Check-in customer" button
- Update customer tags (VIP, Regular, New, Lost)
- "Copy to WhatsApp" button (copies pre-written message)
- Test: Check in customer, tag updates, WhatsApp link works

#### Day 21: Admin Panel - PWA Setup
**Goal:** Works like mobile app

**What you'll learn:**
- PWA basics (manifest, service worker)
- Installing web app to phone

**What we'll build:**
- PWA manifest (app name, icon)
- Service worker (offline functionality - optional)
- Test: Install admin panel on phone, use it

---

### WEEK 4: Public Website + Deploy

#### Day 22-23: Public Website Template
**Goal:** Salon's customer-facing site

**What you'll learn:**
- Next.js dynamic routing (subdomain per salon)
- Tailwind CSS basics

**What we'll build:**
- Single-page website template
- Sections: Hero, Services, Contact, Posts
- Mobile-responsive
- Test: View Maloy's public site on phone

#### Day 24: Google Ratings + Social Links
**Goal:** Social proof and discoverability

**What you'll learn:**
- Embedding widgets (Google Reviews)
- Dynamic links (WhatsApp, social media)

**What we'll build:**
- Google ratings display (manual for now)
- Book Now → WhatsApp link
- Contact Now → Call/WhatsApp
- Social media icons (Instagram, Facebook, TikTok)
- Test: Click "Book Now", opens WhatsApp

#### Day 25: Products/Services Catalog
**Goal:** Show what salon offers

**What you'll learn:**
- Django model for services
- Image uploads (if time permits)

**What we'll build:**
- Services model (name, price, description)
- Display on public website
- Admin panel: Add/edit services
- Test: Add "Haircut - 500 KES", see it on website

#### Day 26-27: Deploy to Production
**Goal:** Live on the internet

**What you'll learn:**
- Deployment (Railway, Render, or Vercel)
- Environment variables (secrets)
- SSL certificates (HTTPS)

**What we'll build:**
- Deploy Django backend (Railway/Render)
- Deploy Next.js frontend (Vercel)
- Configure subdomains (maloy.yourdomain.com)
- Test: Access from phone, everything works

#### Day 28: Add VIP Nail Spa (Second Tenant)
**Goal:** Prove multi-tenant works

**What you'll learn:**
- Creating new tenants
- Data isolation verification

**What we'll build:**
- VIP Nail Spa tenant
- Their customer database
- Their public website (vipnails.yourdomain.com)
- Test: Both salons see ONLY their data

---

## SUCCESS CRITERIA

**After 4 weeks:**
- ✅ 2 salons with live public websites
- ✅ Both salon owners using admin panel daily
- ✅ Automatic SMS reminders sending
- ✅ M-Pesa payments auto-tracking visits
- ✅ Dashboard showing 30+/90+ day customers
- ✅ Both salons paying 1,000 KES/month
- ✅ Revenue: 2,000 KES/month

**More importantly:**
- ✅ Built complete commercial product from scratch
- ✅ Understand django-tenants architecture deeply
- ✅ Can work with Claude as co-developer effectively
- ✅ Have sellable product to pitch to 10 more salons
- ✅ Path to 10,000 KES/month (10 salons)

---

## WHAT THIS IS

✅ Complete business solution (website + retention system)
✅ Sellable as-is (no rebuilding mid-sale)
✅ Learning just enough to build (not comprehensive course)
✅ Using AI for syntax (focus on architecture)
✅ Shipping real product for real customers

**You will sell what you've built. Period.**

If market doesn't buy, you'll learn by trying. But you're not rebuilding mid-sale.

---

## OPEN QUESTIONS (Decide Before Starting)

**1. Google Ratings Integration:**
- A) Embed Google reviews widget?
- B) Just show star rating + count manually?
- C) Skip for MVP, add later?

**2. M-Pesa Integration:**
- A) Start with SMS parsing (quick, Week 2)
- B) Go straight to Daraja API (proper, 5+ days setup)

**3. Posts/Updates:**
- A) Salon owner manually posts via admin panel
- B) Auto-pull from Instagram (complex)

**4. Booking System:**
- A) "Book Now" = WhatsApp message (simple)
- B) Full calendar booking (too complex for 4 weeks)

---

## COMMIT MESSAGE FORMAT

```bash
git commit -m "feat: [feature name] - [key learning]

- What was built: [specific implementation]
- Why it matters: [architectural understanding]
- What I learned: [concept that cannot be automated]
- Day X/28"
```

**Example:**
```bash
git commit -m "feat: M-Pesa SMS parsing - automatic visit tracking

- What was built: Parser extracts customer name/amount from M-Pesa SMS
- Why it matters: Salon owner doesn't manually log visits anymore
- What I learned: Regex for structured text vs AI for unstructured text
- Day 8/28"
```

---

## TOMORROW MORNING

**Day 0: Test Celcom SMS first**

1. Sign up: https://celcomafrica.com
2. Get 50 free SMS credits
3. Send test SMS to your phone + both salon owners
4. Verify: Do they receive it?

**If SMS works:**

Say to Claude CLI: **"I'm ready for Day 1 - Django-Tenants Setup"**

I'll read django-tenants docs, tell you what to read for 10 min, we discuss, then build.

**No overthinking. No perfect setup. Just build.**

---

**Ready? See you tomorrow morning. 🚀**
