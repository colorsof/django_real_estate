# PRODUCT REQUIREMENTS
## Customer Retention System + Business Website for Kenyan Salons

**Last Updated:** 2025-11-04
**Timeline:** 4 weeks
**First Customers:** Maloy Salon, VIP Nail Spa
**Price:** 1,000 KES/month per salon

---

## THE PRODUCT

**Two-part solution:**
1. **Public Website** (Frontend) - For salon's customers
2. **Admin Panel** (Backend) - For salon owner to manage retention

**Value Proposition:**
- Salons get online presence (website as bonus/hook)
- Salons get retention system (core value - keep customers coming back)

---

## PART 1: PUBLIC WEBSITE (Frontend)

**What customers see when they visit the salon's website:**

### Hero Section
- **Google Local Ratings** (social proof)
  - Display star rating
  - Show review count
  - Link to Google Business Profile

### Primary Actions
- **Book Now Button**
  - Triggers WhatsApp message or call
  - Or simple booking form

- **Contact Now Button**
  - WhatsApp direct link
  - Phone number

### Products/Services Catalog
- Display services offered (e.g., "Haircut - 500 KES")
- Or products for sale
- With images if available
- Prices visible

### Social Media Links
- Instagram
- Facebook
- TikTok
- WhatsApp Business

### Posts/Updates Section
- New items/services
- Trending styles
- Special offers
- Before/after photos

**Tech:**
- Single-page website (responsive)
- Mobile-first (most customers on phones)
- Fast loading (Kenya internet speeds)
- Each salon gets branded subdomain: `maloy.yourdomain.com`

---

## PART 2: ADMIN PANEL (Backend)

**What salon owner uses to manage customer retention:**

### A) Customer Management

**Import Contacts**
- Upload CSV from phone
- Or manually add customers
- Fields: Name, Phone, Last Visit Date

**Tag Customers**
- VIP (high-value, frequent)
- Regular (normal customers)
- New (first-time visitors)
- Lost (haven't returned in 90+ days)

### B) Daily Outreach System

**Schedule SMS Reminders**
- System suggests 3-10 customers to contact daily
- Pre-written message templates
- One-click send via SMS (Celcom API)
- **Copy to WhatsApp** button (for personal touch)

**Schedule Phone Calls**
- Mark 1-2 VIP/Lost customers to call today
- Reminder notification
- Track: Did you call them? (Y/N)

### C) Customer Activity Tracking

**Manual Check-in**
- When customer arrives: "Check-in [Customer Name]"
- Updates: Last Visit Date
- Tracks: Visit frequency

**Referral Tracking**
- Mark: "Jane referred by Sarah"
- Track: Who brings most referrals
- Reward top referrers

### D) Product/Service Follow-up

**Post-Service SMS**
- 2-3 days after visit: "How was your haircut? Reply 1-5 stars"
- Or: "Did the product work well for you?"
- Track satisfaction scores

### E) M-Pesa Integration

**Automatic Payment Tracking**
- Scrape M-Pesa SMS messages
- Parse: "Received KES 1,500 from JANE WANJIKU..."
- Link payment to customer check-in
- Auto-update: Last Visit Date + Amount Spent

**Why:** Salon owner doesn't need to manually log visits - M-Pesa does it automatically

### F) Retention Dashboard

**Key Metrics Display:**

1. **Last Contacted Date** (per customer)
   - Shows: Last SMS/call/WhatsApp interaction

2. **Last Check-in Date** (per customer)
   - Shows: Last time they visited salon

3. **Customers Who Haven't Returned:**
   - 30+ days (warning - at risk)
   - 90+ days (critical - lost customer)

4. **Last Phone Call Tracking**
   - If messaged but didn't respond → call them
   - Track: When was last phone call

5. **Active vs Lost Customers**
   - Active: Visited in last 30 days
   - At Risk: 30-90 days
   - Lost: 90+ days
   - Visual graph/chart

6. **Win-Back Campaign Tracking**
   - For lost customers: "Come back! 20% off"
   - Track: How many won back
   - Track: Discount redemption

---

## TECHNICAL ARCHITECTURE

### Multi-Tenant Setup (django-tenants)
- Each salon = separate tenant
- Complete data isolation
- Each salon gets:
  - Own subdomain (`maloy.yourdomain.com`)
  - Own database schema
  - Own admin login

### Tech Stack

**Backend:**
- Django + django-tenants
- PostgreSQL (required for multi-tenant)
- Celery (for scheduled SMS sending)
- Celcom Africa SMS API

**Frontend (Public Website):**
- Next.js + Tailwind CSS
- PWA-enabled (installs like app)
- Server-side rendering (fast loading)

**Frontend (Admin Panel):**
- Next.js + Tailwind CSS
- Charts/graphs for dashboard
- Mobile-responsive (owner uses phone)

**Integrations:**
- M-Pesa: SMS parsing or Daraja API
- Google Local: Ratings widget/API
- WhatsApp: Direct links (no API needed for MVP)

---

## 4-WEEK BUILD TIMELINE

### Week 1: Foundation
- **Days 1-2:** Django multi-tenant setup, first tenant (Maloy)
- **Days 3-4:** Customer model, import contacts, tagging system
- **Days 5-7:** SMS integration (Celcom), send first test SMS

### Week 2: Retention Features
- **Days 8-9:** Daily outreach system (who to contact today)
- **Days 10-11:** Check-in tracking, M-Pesa SMS parsing
- **Days 12-14:** Dashboard (30+ days, 90+ days, active vs lost)

### Week 3: Public Website
- **Days 15-16:** Public website template (Next.js)
- **Days 17-18:** Google ratings integration, book/contact buttons
- **Days 19-21:** Products/services catalog, social media links, posts

### Week 4: Polish + Deploy
- **Days 22-23:** Win-back campaigns, referral tracking
- **Days 24-25:** Product follow-up SMS system
- **Days 26-27:** Deploy to production, test on phones
- **Day 28:** Onboard Maloy + VIP Nail Spa

---

## SUCCESS CRITERIA

**After 4 weeks:**
- ✅ Both salons have live public websites
- ✅ Both salon owners using admin panel daily
- ✅ Automatic SMS reminders sending
- ✅ M-Pesa payments auto-tracking visits
- ✅ Dashboard showing retention metrics
- ✅ Both salons paying 1,000 KES/month

**More importantly:**
- ✅ You've built a complete product from scratch
- ✅ You understand django-tenants architecture
- ✅ You have 2,000 KES/month revenue
- ✅ You can sell this to 10 more salons (path to 10K/month)

---

## WHAT THIS IS

✅ Complete business solution (website + retention)
✅ Salons get online presence + customer management
✅ You sell this package as-is until market tells you otherwise
✅ If customers don't want it, you'll learn by trying to sell it
✅ Not building piecemeal - shipping complete product

**You will sell what you've built. Period.**

If they don't buy it, you build something else. But you're not rebuilding mid-sale.

---

## OPEN QUESTIONS

1. **Google Ratings Integration:**
   - Embed widget? Or scrape ratings? Or manual entry?
   - Need to research Google Business API

2. **M-Pesa Integration:**
   - SMS parsing (faster, Week 2) OR Daraja API (proper, Week 4)?
   - Start with SMS parsing, upgrade later?

3. **Booking System:**
   - Simple form that sends WhatsApp message?
   - Or full calendar booking? (too complex for 4 weeks)

4. **Posts/Updates:**
   - Salon owner uploads via admin panel?
   - Or pulls from their Instagram/Facebook automatically?

---

**Ready to build this?**
