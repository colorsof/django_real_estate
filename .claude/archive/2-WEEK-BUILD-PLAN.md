# 2-WEEK BUILD PLAN



                                                                                                     jii## Customer Retention System for Kenyan Salons

**Last Updated:** 2025-11-04
**Status:** Building MVP
**Customers Waiting:** Maloy Salon + VIP Nail Spa (both committed at 1,000 KES/month)

---

## THE DAILY RHYTHM

**Each morning when you start:**

### 1. Claude Prepares (5 min)
- I read the relevant documentation (django-tenants, SMS APIs, etc.)
- I identify the key concepts/methods you need to know

### 2. You Read (10 min)
- I tell you: "Read these 3 key concepts in django-tenants docs"
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

**Product:** SMS-based customer retention system (PWA)

**Core Features (MVP):**
1. Multi-tenant Django backend (each salon isolated)
2. Customer database per salon
3. Automatic SMS reminders (via Celcom Africa API)
4. "Who hasn't come back" dashboard (salon's #1 request)
5. Simple visit tracking

**Tech Stack:**
- Django + django-tenants (backend)
- Next.js + Tailwind (frontend PWA)
- PostgreSQL (required for django-tenants)
- Celcom Africa SMS API

---

## WEEK 1: Backend Foundation

### Day 1 (Tomorrow): Django-Tenants Setup
**Goal:** Understand multi-tenant architecture, create first tenant (Maloy)

**What you'll learn:**
- How tenant isolation works (separate schemas)
- Why this matters (salon data never mixes)
- What breaks if you mess it up

**What we'll build:**
- Django project with django-tenants installed
- Tenant model (Salon)
- First tenant created (Maloy Salon)
- Test: Can we access Maloy's isolated database?

### Day 2: Customer Database Model
**Goal:** Build the core customer tracking system

**What you'll learn:**
- Django models for tenant-specific data
- What fields salons actually need (based on interviews)

**What we'll build:**
- Customer model (name, phone, last_visit, etc.)
- Admin interface to add customers manually
- Test: Add 5 test customers for Maloy

### Day 3: SMS Integration
**Goal:** Send your first automated SMS

**What you'll learn:**
- How SMS APIs work (Celcom Africa)
- Webhook pattern for automation

**What we'll build:**
- SMS service integration
- Function to send reminder SMS
- Test: Send SMS to your own phone

### Day 4-5: "Who to Contact" Logic
**Goal:** Build salon's #1 requested feature

**What you'll learn:**
- Django queries for "customers not seen in 30+ days"
- Scheduling automated tasks (Celery or simple cron)

**What we'll build:**
- Query: Find customers who haven't visited in X days
- Automatic SMS trigger (daily check)
- Test: Does it identify the right customers?

---

## WEEK 2: Frontend + Deployment

### Day 6-7: Simple Dashboard (Next.js PWA)
**Goal:** Salon can see their customers

**What you'll learn:**
- Next.js basics (just enough)
- PWA setup (works like mobile app)
- Connecting to Django API

**What we'll build:**
- Login page (salon owner)
- Customer list view
- "Customers to contact" highlighted view

### Day 8-9: Visit Tracking
**Goal:** Record when customer visits salon

**What you'll learn:**
- Simple form submission
- Updating customer records

**What we'll build:**
- "Customer visited" button
- Updates last_visit date
- Test: Does dashboard update correctly?

### Day 10-11: Add VIP Nail Spa (Second Tenant)
**Goal:** Prove multi-tenant works

**What we'll learn:**
- Creating new tenants
- Data isolation verification

**What we'll build:**
- VIP Nail Spa tenant
- Their customer database
- Test: Can each salon ONLY see their data?

### Day 12-13: Deploy + Polish
**Goal:** Get it on the internet, working on phones

**What you'll learn:**
- Deployment (Railway/Render)
- SSL certificates
- Mobile testing

**What we'll build:**
- Live URL for each salon
- PWA installed on salon owner's phone
- Test: Can they add customers from their phone?

### Day 14: Onboard Maloy
**Goal:** First customer using it for real

**What you'll do:**
- Visit Maloy salon
- Import their first 20 customers
- Send first batch of SMS reminders
- Get feedback

---

## SUCCESS CRITERIA

**After 2 weeks, you will have:**
- ✅ Working multi-tenant system (2 salons using it)
- ✅ Automatic SMS reminders sending
- ✅ Salons can see "who to contact" dashboard
- ✅ Proven: They'll actually use it (or you'll know why not)
- ✅ Revenue: 2,000 KES/month (2 customers paying)

**More importantly:**
- ✅ Understood django-tenants architecture (not just copied code)
- ✅ Can work with Claude as co-developer effectively
- ✅ Built your first commercial product end-to-end
- ✅ Validated product in market (real customers paying)

---

## WHAT THIS IS NOT

❌ Not a comprehensive course (you're learning just enough)
❌ Not perfect code (it's an MVP to validate)
❌ Not following best practices everywhere (speed matters more)
❌ Not trying to memorize syntax (AI handles that)

✅ Learning architecture (what matters)
✅ Shipping fast (2 weeks, not 2 months)
✅ Getting paid customers (validation)
✅ Using AI effectively (Andrej's approach)

---

## TOMORROW MORNING

When you start tomorrow:

1. Open this file
2. Say to Claude CLI: "I'm ready for Day 1 - Django-Tenants Setup"
3. I'll read the django-tenants docs
4. I'll tell you what to read for 10 minutes
5. We start building

**No overthinking. No perfect setup. Just build.**

---

## COMMIT MESSAGE FORMAT

```bash
git commit -m "feat: [feature name] - [key learning]

- What was built: [specific implementation]
- Why it matters: [architectural understanding]
- What I learned: [concept that cannot be automated]
- Day X/14"
```

**Example:**
```bash
git commit -m "feat: django-tenants setup - tenant isolation via schemas

- What was built: TenantModel, first tenant (Maloy) created
- Why it matters: Each salon's data completely isolated at DB level
- What I learned: PostgreSQL schemas provide isolation, not separate DBs
- Day 1/14"
```

---

**Ready? See you tomorrow morning.**
