# DAILY VIBE CODING SYSTEM
## Learning Django/Next.js with AI + Documenting for YouTube

**Version:** 3.0 (Revised Oct 27, 2025)  
**Commitment:** Monday-Friday, 6am-12pm (This is your JOB)  
**Target:** 5 videos/week until multi-tenant website complete (Dec 2025)  
**Format:** Document real learning process with Claude as AI tutor  
**Current Position:** Lecture 79/183 - Backend Complete, Starting Next.js Frontend (Lecture 80)

---

## 📅 WEEKLY SCHEDULE OVERVIEW

**Work Days:** Monday - Friday (6am - 12pm)
- 6am-9:30am: Learn + Code + Record (primary session)
- 9:30am-12pm: Continue coding OR edit yesterday's video OR Anki/learning
- This is your JOB. Treat it seriously.

**Weekend:** Saturday - Sunday (Rest, Recharge, Review)
- Saturday morning: Weekly review with Claude
- Sunday evening: Plan next week's lectures
- NO coding obligation - this is recovery time
- Use for exercise, Python Crash Course, reflection, planning

**Result:** 5 videos/week + steady progress toward December deadline

---

## 🎯 THE CORE INSIGHT

**Old thinking:** "I need separate time for coding AND YouTube"  
**New reality:** "My daily coding work IS my YouTube content"

**This is your job:** Monday-Friday, 6am-12pm
- First 3.5 hours (6-9:30am): Primary coding session (recorded)
- Next 2.5 hours (9:30am-12pm): Flexible (continue coding, edit yesterday's video, or learn)

When you code with OBS recording, you're simultaneously:
✅ Learning Django/Next.js (primary goal)
✅ Building multi-tenant website (business goal)
✅ Creating YouTube content (documentation goal)
✅ Staying accountable (job mindset)

**One work session, four outcomes.**

**5 videos per week = 20+ videos per month = Website done by December + Portfolio built**

---

## 📋 MONDAY - FRIDAY ROUTINE (Your Work Day)

**This is your job. Clock in at 6am. Clock out at 12pm.**

### ⏰ 5:45am - 6:00am | WAKE UP & PREP (15 min)

**Every weekday. This is your job.**

- [ ] Bathroom, water, coffee
- [ ] Boot up computer (Ubuntu)
- [ ] Open my-context.md (remind yourself why you're doing this)
- [ ] Quick mental check: "I'm documenting my learning, not performing expertise"
- [ ] **Today I'm clocking in. This is work.**

---

### ⏰ 6:00am - 6:20am | SESSION PLANNING (20 min)

**Step 1: Identify Today's Learning Goal (5 min)**

Open file: `~/Documents/YouTube/YYYY-MM-DD-goal.txt`

```
TODAY'S LEARNING SESSION
Date: ___________
Course Lecture: #___ (Title: _____________)
Lecture Length: ___ minutes

Feature I'm Building: 
[e.g., "Redux auth slice with login/logout"]

New Concept(s) I'll Encounter:
[e.g., "Redux, reducers, extraReducers, async actions"]

What I DON'T Know Yet:
[e.g., "What is Redux? Why use it? How does it connect to Django?"]

Success Looks Like:
[e.g., "User can login via Next.js frontend, token stored in Redux, persists on refresh"]
```

**Step 2: Pre-Session Questions List (5 min)**

In same file, add:

```
QUESTIONS TO ASK CLAUDE:
Before coding:
1. What is [new concept]? ELI5 then ELI10 then developer explanation
2. Why does this concept exist? What problem does it solve?
3. What would break if I didn't use it?

During coding:
[Leave blank - you'll discover these while coding]
```

**Step 3: OBS Technical Check (10 min)**

- [ ] Open OBS Studio
- [ ] Verify Source 1: Screen Capture (VSCode visible)
- [ ] Verify Source 2: Browser source (phone camera in corner)
- [ ] Audio test: Clap hands, check levels in OBS
- [ ] Recording destination: `~/Videos/Raw/YYYY-MM-DD-session.mp4`
- [ ] **Test record 10 seconds** → Stop → Verify file exists
- [ ] Delete test file
- [ ] Leave OBS ready (but not recording yet)

---

### ⏰ 6:20am - 6:30am | B-ROLL SETUP (10 min)

**These are brief clips you'll narrate over later**

**Clip 1: Context Setup (3 min recording)**
- [ ] Start OBS recording
- [ ] Open VSCode showing your Django project (backend that works)
- [ ] Open browser to course website, show today's lecture
- [ ] Open goal.txt file you just wrote (full screen, 5 seconds)
- [ ] Stop recording
- [ ] Save as: `YYYY-MM-DD-broll-context.mp4`

**Clip 2: Pre-Learning State (3 min recording)**
- [ ] Start OBS recording
- [ ] Open VSCode to blank Next.js file where you'll code
- [ ] Open Claude (web or VSCode extension)
- [ ] Show empty chat (ready to learn)
- [ ] Stop recording  
- [ ] Save as: `YYYY-MM-DD-broll-ready.mp4`

**Quick check:**
- [ ] 2 B-roll clips saved (total ~6 min footage)
- [ ] Goal.txt file written and saved
- [ ] OBS configured and tested
- [ ] You're mentally ready to learn (not perform)

---

## 🧠 LEARNING + CODING SESSION (6:30am - 9:30am)

### ⏰ 6:30am | START MAIN RECORDING

**Hit record in OBS - This runs for entire session**

Recording saves to: `~/Videos/Raw/YYYY-MM-DD-session.mp4`

**Important mindset:**
- You are LEARNING, not teaching
- You are ASKING questions, not answering them
- Mistakes are expected and valuable
- Confusion is content
- Just work naturally

---

### 📚 PHASE 1: LEARN THE CONCEPT (30-45 min)

**Before touching any code, understand what you're building**

#### **Step 1: Watch Course Lecture (8-20 min)**
- Play the lecture
- Take notes on paper (what's the feature, what tech is used)
- Pause when confused (this is content)
- Don't code yet - just absorb

#### **Step 2: Ask Claude for Conceptual Understanding (15-25 min)**

**Use the prompting framework:**

**Prompt Level 1: ELI5 → ELI10 → Developer**
```
I'm on lecture [X] of my Django + Next.js course.
They just introduced [NEW CONCEPT] for [PURPOSE].

I've never used this before. I need to understand it before I code.

Please explain [CONCEPT] to me:
1. Like I'm 5 years old
2. Like I'm 10 years old  
3. Like I'm a developer

Then answer:
- Why does [CONCEPT] exist? What problem does it solve?
- What would happen if I DIDN'T use it?
- How does it connect to Django (my backend)?
```

**Example (Redux):**
```
I'm on lecture 181 of my Django + Next.js course.
They just introduced Redux for state management in Next.js.

I've never used Redux. I barely understand what "state" means in React.

Please explain Redux to me:
1. Like I'm 5 years old
2. Like I'm 10 years old
3. Like I'm a developer

Then answer:
- Why does Redux exist? What problem does it solve?
- What would happen if I DIDN'T use Redux?
- How does Redux connect to my Django JWT authentication backend?
```

**Read Claude's response out loud (or mumble it) - this is content**

**Follow-up questions as needed:**
- "Wait, you said [X]. Can you elaborate on that?"
- "How is this different from [thing I do know]?"
- "Give me a real-world analogy"

**Stop when you feel: "Okay, I get the CONCEPT, even if I can't code it yet"**

---

### 💻 PHASE 2: UNDERSTAND THE APPROACH (15-20 min)

**Now you know WHAT. Ask Claude HOW before watching the course implementation.**

**Prompt Level 2: Planning & Approach**
```
Okay, I understand [CONCEPT] conceptually now.

My task: [Describe the feature you need to build]

Before I watch the course show their implementation:
1. How would YOU approach building this?
2. What are the key decisions I need to make?
3. What's the simplest way to structure this for a learner?
4. What could I mess up if I don't understand the fundamentals?

Be specific about file structure, key functions, data flow.
```

**Example (Redux auth):**
```
Okay, I understand Redux conceptually now.

My task: Build a Redux slice that handles user login/logout, 
stores the JWT token, and persists authentication state across page refreshes.

Before I watch the course show their implementation:
1. How would YOU approach building this?
2. What are the key decisions I need to make?
3. What's the simplest way to structure this for a learner?
4. What could I mess up if I don't understand Redux fundamentals?

Be specific about:
- File structure (where does the authSlice go?)
- Key functions (what reducers do I need?)
- Data flow (how does login action → reducer → state work?)
```

**Claude will give you an approach. Take notes.**

---

### 🎓 PHASE 3: WATCH COURSE IMPLEMENTATION (10-15 min)

**Now watch how the course does it**

- Play the coding portion of the lecture
- Pause frequently
- Compare to Claude's suggested approach
- Notice similarities and differences
- Don't judge yet - just observe

**You'll likely notice:** "Hmm, Claude suggested X but the course does Y"

**This is good. This is the learning moment.**

---

### 🤔 PHASE 4: COMPARE APPROACHES (10-15 min)

**Ask Claude to explain the differences educationally**

**Prompt Level 3: Learning from Differences**
```
I asked you how to implement [FEATURE].
You suggested: [Summarize Claude's approach]

But my course does it like this: [Describe course approach OR paste key code snippet]

I'm not experienced enough to judge which is "better."

Can you help me learn by explaining:
1. Why might the course have chosen their approach?
2. Why did you suggest something different?
3. What are the trade-offs between the two approaches?
4. For a LEARNER like me (not production), which approach helps me understand fundamentals better?
5. Are there any red flags in either approach I should know about?

Be educational, not prescriptive. I want to understand WHY, not just WHICH.
```

**Read Claude's explanation carefully**

**Make your learning decision:**
```
Based on this, I'm going to [follow course / use Claude's way / hybrid approach]
because [your reasoning - usually: simpler for learning / teaches fundamentals better / etc.]
```

**Say this out loud or type it in notes - this is content**

---

### ⌨️ PHASE 5: CODE WITH UNDERSTANDING (60-90 min)

**Now you code, using Claude as your AI tutor**

**Prompt Level 4: Implementation with Explanation**
```
Let's build [FEATURE] following [the course structure / your suggested approach].

As we code, please:
- Explain what each piece does and WHY
- Point out where I need to understand deeply vs what's boilerplate
- Help me connect this to concepts we discussed earlier

I'll type the code. You guide and explain.
Ready? Let's start with [first file/function].
```

**Coding process:**

1. **Start typing** (following course or Claude's structure)

2. **When you get stuck or confused:**
```
"I'm confused about [specific thing].
Before I continue, can you explain why we're doing [X]?"
```

3. **When you hit an error:**
```
"I'm getting this error: [paste full error]

Here's my code: [paste relevant code]

What did I misunderstand? 
Don't just fix it - help me understand what went wrong."
```

4. **When code works but you're not sure why:**
```
"This works, but I want to make sure I understand.
Walk me through the flow:
When [user action happens], what exactly happens step by step?"
```

5. **When you see a pattern you don't recognize:**
```
"The course uses this pattern: [paste code]
Before I copy it, explain:
- What is this pattern called?
- Why is it used here?
- What would happen if I did it differently?"
```

**Key principle: Always ask "why" before moving on**

---

### ✅ PHASE 6: TEST & DEBUG (20-30 min)

**Make it work**

- Run the code
- Test the feature
- Hit errors (expected)
- Debug with Claude's help

**Debugging prompts:**
```
"Feature isn't working. Here's what I expect: [X]
Here's what's happening: [Y]
Here's my code: [paste]
Here are console errors: [paste]

Walk me through debugging this step by step.
What should I check first?"
```

**When it finally works:**
- Test it thoroughly
- Understand WHY it works now
- Take a breath (you built something!)

---

### 📝 PHASE 7: COMMIT & REFLECT (10 min)

**Git commit with meaningful message**

```bash
git add .
git commit -m "feat: [Feature name] - [What I learned]

- Built [specific feature]
- Key learning: [main concept mastered]
- Used Claude to understand [challenging part]
- Course lecture: #[X]"
```

**Immediate reflection notes**

Open file: `~/Documents/YouTube/YYYY-MM-DD-session-notes.txt`

```
SESSION COMPLETE
Time spent: ___ hours

What I Built:
[Feature name and status]

Biggest Struggle:
[The moment you were most confused - note timestamp if you remember]

Biggest "Aha!" Moment:
[When it clicked - note timestamp if you remember]

Most Helpful Claude Prompts:
1. [The question that unlocked understanding]
2. [The follow-up that clarified confusion]
3. [The debugging prompt that found the issue]

What I Actually Learned (not just built):
[The deep understanding, not just "I made X work"]

Concept Mastery (1-5):
[New concept]: ___/5 (1=confused, 5=can explain to others)

Status: [ ] Feature Complete [ ] Partial [ ] Blocked

If blocked, what's the issue:
[What you'll tackle next session]

---

VOICEOVER NOTES (for later):
Key moments to include in video:
- Timestamp ~___: [Description of moment]
- Timestamp ~___: [Description of moment]
- Timestamp ~___: [Description of moment]
```

---

### ⏰ 9:30am | STOP RECORDING

- [ ] Stop OBS recording
- [ ] Save as: `~/Videos/Raw/YYYY-MM-DD-session.mp4`
- [ ] **Don't watch it yet** - your brain is tired
- [ ] Save all Claude chat history (it's auto-saved, but bookmark important convos)
- [ ] Close laptop
- [ ] **Take a break** - you earned it

**You now have:**
- 2 B-roll clips (context, ready state)
- 1 full session recording (3 hours of learning/coding)
- Written notes about key moments
- A completed feature (or clear progress)

**Your video exists. You just need to edit it.**

---

## 🔄 REST OF WORK DAY (9:30am - 12pm)

**You have 2.5 hours remaining in your work block. Choose based on what's needed:**

### Option A: Continue Coding (if feature incomplete)
- Keep working on today's feature
- Don't record this part (or keep recording if you want)
- Focus on completion

### Option B: Edit Yesterday's Video (if feature complete)
- Follow the editing workflow (5pm-6:30pm section)
- Get ahead on video editing
- Frees up evening time

### Option C: Deep Learning (Anki + Consolidation)
- Review today's concepts in Anki
- Add new cards for what you learned
- Read documentation for deeper understanding
- Prepare questions for next session

### Option D: Admin & Planning
- Update course progress tracker
- Plan tomorrow's lecture(s)
- Respond to YouTube comments
- Research concepts for upcoming lectures

**12:00pm - CLOCK OUT**
- [ ] Save all work
- [ ] Commit code if not done
- [ ] Write quick notes on progress
- [ ] Close laptop
- [ ] **You're done for the day. Good job.**

---

## 🌆 AFTERNOON/EVENING (12pm onwards)

**Follow your normal schedule from my-context.md:**

- 1pm-3pm: Anki review (if not done in morning)
- 3pm-5pm: Exercise
- 5pm-6:30pm: Video editing (if needed) OR free time
- 6:30pm-9pm: Python Crash Course
- 9pm onwards: Prayer, journal, learning, meditation, sleep

**Key principle:** Your 6-hour morning block (6am-12pm) is SACRED. Everything else is flexible.

---

## 🎬 VIDEO EDITING SESSION (5:00pm - 6:30pm)

**If needed - or do during 9:30am-12pm work block**

**90 minutes to turn footage into publishable video**

### ⏰ 5:00pm - 5:25pm | FOOTAGE REVIEW (25 min)

**Goal: Find the 8-10 best minutes from 3 hours**

- [ ] Open `YYYY-MM-DD-session.mp4` in editor (DaVinci Resolve or CapCut)
- [ ] Open your session-notes.txt (your guide)
- [ ] Watch at 2x speed
- [ ] Drop markers for these moment types:

**🎯 MARKER TYPES:**

| Marker | What to Look For | Why It's Valuable |
|--------|------------------|-------------------|
| 🧠 LEARN | You asking Claude conceptual questions | Shows prompting for understanding |
| 🤔 CONFUSE | Visible confusion or "wait, what?" | Authentic struggle = relatable |
| 💡 AHA | "Ohhh, I get it now!" moment | Breakthrough = satisfying |
| ❌ ERROR | Code breaks, error appears | Debugging process = educational |
| 🔧 DEBUG | Working through error with Claude | Problem-solving = practical |
| ✅ WORKS | Feature working for first time | Success = motivating |
| 🎓 EXPLAIN | You explaining back to Claude (testing understanding) | Shows learning, not just copying |

**Selection strategy:**
- Need: At least 1 LEARN moment (prompting example)
- Need: At least 1 ERROR → DEBUG sequence (real problem-solving)
- Need: At least 1 AHA moment (payoff)
- Want: 1 CONFUSE moment (humanizes you)
- Want: 1 WORKS moment (if feature completed)

**Target: 5-8 marked moments**

---

### ⏰ 5:25pm - 5:45pm | ROUGH CUT (20 min)

**Build the timeline**

**Video Structure (10-12 min final):**

```
[0:00-0:30] INTRO - Context
  - B-roll: Context clip
  - B-roll: Today's goal text on screen

[0:30-1:00] SETUP - What I'm learning
  - B-roll: Ready state
  - Show course lecture title/topic

[1:00-4:00] LEARN - Understanding the concept
  - Clip: You asking Claude to explain
  - Clip: Reading Claude's ELI5 explanation
  - Your "okay I think I get it" moment

[4:00-7:00] CODE - Implementation journey  
  - Clip: Starting to code
  - Clip: Hit error (confusion visible)
  - Clip: Debugging with Claude
  - Clip: "Aha!" moment

[7:00-10:00] REFLECT - What I learned
  - Clip: Feature working (if complete) OR progress state
  - Clip: You explaining what you learned

[10:00-10:30] OUTRO - Takeaways
  - B-roll: Your notes or completed code
  - Text on screen: Next session preview
```

**Quick editing:**
- [ ] Drag marked clips to timeline in story order
- [ ] Speed up typing/waiting (2x-3x speed)
- [ ] Keep confusion/debugging at normal speed (1x)
- [ ] Cut dead air >5 seconds
- [ ] Trim unnecessary mouse fumbling
- [ ] Don't worry about perfection - just arrange the story

---

### ⏰ 5:45pm - 6:20pm | ADD VOICEOVER (35 min)

**This is where you explain what happened**

**Voiceover Script Template:**

```
INTRO (over B-roll):
"Today I'm learning [NEW CONCEPT] - specifically [FEATURE].
I'm on lecture [X] of my Django + Next.js course.
I've never used [CONCEPT] before, so I need to understand it before coding.
I'm using Claude as my AI tutor.
You're watching my actual learning session - confusion, mistakes, everything."

LEARNING PHASE (over Claude conversation clips):
"First, I asked Claude to explain [CONCEPT] like I'm 5, then 10, then a developer.
[Summarize key insight from Claude's explanation]
This helped me understand [what clicked].
Before touching code, I wanted to know: Why does this exist? What problem does it solve?"

CODING PHASE (over implementation clips):
"Then I asked Claude: How would YOU build this?
[Summarize Claude's suggested approach]

The course did it [slightly/very] differently.
[Show the difference]

I asked Claude to explain both approaches educationally.
[Key insight about trade-offs]

For learning, I decided to [choice] because [reasoning].

As I coded, I asked Claude to explain each piece, not just generate code.
Notice how I'm constantly asking 'why' - this is key."

ERROR/DEBUG PHASE (over debugging clips):
"Then I hit this error [point to screen].
This took [X] minutes of back-and-forth with Claude.
The breakthrough came when I [specific insight or prompt that worked].
This taught me [technical lesson AND prompting lesson]."

REFLECTION (over working feature or progress state):
"Here's what I actually learned today - not just built, but learned:

1. [Technical understanding - the concept mastered]
2. [Prompting strategy - how to ask for learning, not just code]
3. [Meta lesson - when to struggle vs ask, or how to evaluate approaches, etc.]

Tomorrow I'm tackling [next feature].
This is day [X] of learning to code in the AI era with Claude as my tutor."
```

**Recording voiceover:**
- Use your phone's voice memo app (good enough quality)
- Speak conversationally - like explaining to a friend
- It's okay to stumble and re-record sections
- Keep your Kenyan accent (authenticity!)
- Don't over-script - bullet points are fine

**Import and sync:**
- [ ] Import voiceover files to editor
- [ ] Place audio under corresponding video clips
- [ ] Adjust audio levels (voiceover louder than ambient)
- [ ] Fade in/out between segments

---

### ⏰ 6:20pm - 6:30pm | FINAL POLISH (10 min)

**Add minimal finishing touches**

- [ ] Title card (2 sec): "Learning [Concept] with Claude: [Outcome]"
- [ ] Background music (low volume, non-distracting) - optional
- [ ] Text overlays for 1-2 key prompts or concepts - optional
- [ ] Outro text (3 sec): "Next: [Tomorrow's topic] | Day [X]/100"
- [ ] Export settings: 1080p, H.264, MP4
- [ ] Export as: `~/Videos/Final/YYYY-MM-DD-FINAL.mp4`

**While exporting (5-10 min):**
- [ ] Write video metadata (see template below)
- [ ] Create simple thumbnail (optional, can do later)

---

## 📤 VIDEO METADATA & UPLOAD

### Title Formula:
```
"Learning [Concept] with Claude: [Main Outcome/Lesson]"

Examples:
✅ "Learning Redux with Claude: From Confused to Auth Working"
✅ "Understanding Django Serializers: AI-Assisted Learning Process"
✅ "Next.js Forms with Claude: Debugging Real Errors"
✅ "First Time Using [Tech]: How I Learn with AI as Tutor"

Avoid:
❌ "Redux Tutorial" (you're not teaching, you're learning)
❌ "How to Build [X]" (sounds like guru content)
❌ "AI Codes Everything" (misleading)
```

### Description Template:
```
I'm learning Django + Next.js by building a multi-tenant website, using Claude as my AI tutor (vibe coding).

Today's learning: [Concept/feature name]
Course lecture: [X]
Time spent: [Hours]
Understanding level: [X/5]

What I learned:
• [Main technical concept]
• [Prompting strategy that worked]
• [Meta-learning insight]

This is day [X] of learning to code in 2025 - documenting the real process, mistakes included.

I'm NOT a tutorial channel. I'm documenting how to LEARN when AI is your tutor.

⏰ Timestamps:
0:00 - Today's learning goal
1:00 - Understanding the concept (Claude conversation)
4:00 - Coding & hitting errors
7:00 - Debugging & breakthrough
10:00 - What I actually learned

🔗 Resources:
• Course I'm following: [Link if allowed/relevant]
• My learning journey playlist: [Your playlist]

💬 Questions? Comment below. I'm learning too, so let's figure this out together.

#VibeCoding #LearnWithAI #Django #NextJS #CodeIn2025 #AITutor
```

### Thumbnail Checklist (Optional - 5 min):
```
Quick thumbnail in Canva or GIMP:
- [ ] Screenshot: Your confused face OR Claude conversation OR error message
- [ ] Text overlay: "Learning [CONCEPT]" or "Day [X]"
- [ ] Keep it simple - readable on phone
- [ ] Authentic > polished

Save as: YYYY-MM-DD-thumbnail.png

OR skip thumbnail initially - YouTube auto-generates one
Focus on consistency over perfection for first 10 videos
```

### Upload Schedule:
- **Monday session** → Edit Monday evening → Upload Monday night or Tuesday morning
- **Wednesday session** → Edit Wednesday evening → Upload Wednesday night or Thursday morning  
- **Friday session** → Edit Friday evening → Upload Friday night or Saturday morning

**Consistent schedule matters more than same-day upload**

---

## 🧩 THE PROMPTING FRAMEWORK REFERENCE

**Keep this handy during your coding session**

### LEVEL 1: Understanding Prompts
**Use when:** You encounter a new concept/technology

```
Template:
"I'm learning [CONCEPT] from my [course/tutorial].
I've never used this before.

Explain [CONCEPT]:
1. Like I'm 5 years old
2. Like I'm 10 years old
3. Like I'm a developer

Then answer:
- Why does [CONCEPT] exist? What problem does it solve?
- What would happen if I DIDN'T use it?
- How does it relate to [other tech in my stack]?"

Examples:
• "Explain Redux..." (for state management)
• "Explain JWT tokens..." (for authentication)
• "Explain REST APIs..." (for backend communication)
• "Explain React hooks..." (for frontend logic)
```

### LEVEL 2: Planning Prompts
**Use when:** You understand the concept, need implementation guidance

```
Template:
"I understand [CONCEPT] conceptually.

My task: [Describe the feature]

Before I code:
1. How would YOU approach building this?
2. What are the key decisions I need to make?
3. What's the simplest structure for a learner?
4. What could I mess up if I don't understand fundamentals?

Be specific about: [file structure / data flow / key functions / etc.]"

Examples:
• "I need to build user login with JWT..."
• "I need to create a form that posts to Django API..."
• "I need to store authentication state in Redux..."
```

### LEVEL 3: Learning from Differences Prompts
**Use when:** Course/tutorial suggests one approach, Claude suggests another

```
Template:
"I asked you how to implement [FEATURE].
You suggested: [Claude's approach]

But my course does it like this: [Course approach]

I'm not experienced enough to judge which is 'better.'

Explain educationally:
1. Why might the course have chosen their approach?
2. Why did you suggest something different?
3. What are the trade-offs?
4. For a LEARNER, which helps me understand fundamentals better?
5. Any red flags I should know about?

Be educational, not prescriptive."

Examples:
• "Course uses class components, you suggested functional..."
• "Course uses fetch(), you suggested axios..."
• "Course stores token in localStorage, you suggested httpOnly cookies..."
```

### LEVEL 4: Implementation with Explanation Prompts
**Use when:** Ready to code, want Claude to explain as you go

```
Template:
"Let's build [FEATURE] following [chosen approach].

As we code:
- Explain what each piece does and WHY
- Point out what I need to deeply understand vs what's boilerplate
- Connect this to concepts we discussed earlier

I'll type. You guide and explain.
Start with: [first file/function]"

Examples:
• "Let's build the authSlice.js Redux file..."
• "Let's create the login form component..."
• "Let's set up the API endpoint for user registration..."
```

### LEVEL 5: Debugging & Understanding Prompts
**Use when:** Code doesn't work, or works but you don't know why

```
Template for errors:
"I'm getting this error: [full error message]

My code: [paste relevant code]

My understanding: I think [what you think is happening]

What did I misunderstand?
Don't just fix it - help me understand what went wrong."

Template for "it works but...":
"This code works, but I want to make sure I understand.

Walk me through the flow:
When [user action], what exactly happens step by step?
Why does [specific line] work the way it does?"

Examples:
• "Getting 'undefined is not a function' error..."
• "The login works but token doesn't persist..."
• "Code works but I don't understand the async/await part..."
```

### LEVEL 6: Testing Understanding Prompts
**Use when:** You think you understand, want to verify

```
Template:
"I've built [FEATURE] and I think I understand it.

Let me explain [CONCEPT] back to you in my own words:
[Your explanation]

Is my understanding correct?
What am I missing or misunderstanding?"

Examples:
• "Let me explain how Redux works..."
• "Let me explain the JWT authentication flow..."
• "Let me explain why we use serializers in Django..."
```

---

## 📊 TRACKING & ACCOUNTABILITY

### Weekly Checklist (Monday-Friday work week):

```
WEEK OF: [Date]

Monday Session:
[ ] 6am: Planning complete
[ ] 6:30am-9:30am: Coded + recorded
[ ] 9:30am: Session notes written
[ ] 9:30am-12pm: [Continued coding / Edited / Learned / Admin]
Feature built: ___________
Lecture(s): ___
Video status: [Edited / Scheduled / Published]

Tuesday Session:
[ ] 6am: Planning complete
[ ] 6:30am-9:30am: Coded + recorded
[ ] 9:30am: Session notes written
[ ] 9:30am-12pm: [Continued coding / Edited / Learned / Admin]
Feature built: ___________
Lecture(s): ___
Video status: [Edited / Scheduled / Published]

Wednesday Session:
[ ] 6am: Planning complete
[ ] 6:30am-9:30am: Coded + recorded
[ ] 9:30am: Session notes written
[ ] 9:30am-12pm: [Continued coding / Edited / Learned / Admin]
Feature built: ___________
Lecture(s): ___
Video status: [Edited / Scheduled / Published]

Thursday Session:
[ ] 6am: Planning complete
[ ] 6:30am-9:30am: Coded + recorded
[ ] 9:30am: Session notes written
[ ] 9:30am-12pm: [Continued coding / Edited / Learned / Admin]
Feature built: ___________
Lecture(s): ___
Video status: [Edited / Scheduled / Published]

Friday Session:
[ ] 6am: Planning complete
[ ] 6:30am-9:30am: Coded + recorded
[ ] 9:30am: Session notes written
[ ] 9:30am-12pm: [Continued coding / Edited / Learned / Admin]
Feature built: ___________
Lecture(s): ___
Video status: [Edited / Scheduled / Published]

WEEK SUMMARY:
Videos published: ___/5
Total work hours: ~30 hours (6hrs × 5 days)
Lectures completed: ___
Course progress: ___/183 (___%)
Total subscribers: ___
Most helpful prompt this week: ___________
Biggest learning: ___________
Energy level end of week: ___/10 (adjust intensity if <6)
```

### Monthly Goals Tracker:

```
MONTH: [Month, Year]

Work commitment: 30 hours/week × 4 weeks = 120 hours
Videos published: ___ (target: 20-22 for 5/week)
Lectures completed: ___
Course completion: ___%
Multi-tenant site features complete:
  [ ] Authentication
  [ ] User profiles
  [ ] Tenant management
  [ ] [Other features...]

YouTube stats:
  Subscribers: ___
  Total views: ___
  Avg watch time: ___%
  Top performing video: ___________

Top 3 learnings this month:
1. ___________
2. ___________
3. ___________

How sustainable was this pace? (1-10): ___
Adjustments needed for next month:
___________

Next month's focus:
___________
```

---

## ⚠️ COMMON TRAPS & HOW TO AVOID

### Trap 1: "This session was boring, no good content"
**Reality:** Your most "boring" sessions (lots of debugging, confusion) are your BEST content.
**Solution:** Record everything. Decide in editing what to use.

### Trap 2: "Let me re-record, I made a mistake"
**Reality:** Mistakes ARE the content. Your audience needs to see struggle.
**Solution:** Never re-record. Embrace errors. Voiceover can add context.

### Trap 3: "I need to understand this perfectly before filming"
**Reality:** The learning process IS the video. Don't pre-learn.
**Solution:** Hit record THEN learn. Document confusion → understanding.

### Trap 4: "This video needs to be perfect"
**Reality:** Consistency > perfection. 5 good videos per week > 1 perfect video per week.
**Solution:** 90-minute editing limit. Ship it. Improve next time.

### Trap 5: "I should explain this better in the video"
**Reality:** You're not a teacher (yet). You're a learner documenting.
**Solution:** Voiceover should say "Here's what I learned" not "Here's how to do it."

### Trap 6: "I'll batch record 3 sessions then edit later"
**Reality:** Memory fades. Editing gets harder. Footage debt accumulates.
**Solution:** Same-day editing ONLY. Code Monday? Edit Monday evening.

### Trap 7: "I need better equipment before I start"
**Reality:** Your Infinix phone + OBS is enough for 20+ videos.
**Solution:** Create 20 videos first. THEN evaluate equipment upgrades.

---

## 🎯 SUCCESS METRICS THAT MATTER

**Focus on these, ignore vanity metrics for first 30 days:**

### Daily Success (Monday-Friday):
- [ ] Did I clock in at 6am? (Yes/No)
- [ ] Did I work the full 6-hour block? (Yes/No)
- [ ] Did I record my coding session? (Yes/No)
- [ ] Did I learn something new? (Yes/No)
- [ ] Did I treat this like a job? (Yes/No)

### Weekly Success:
- [ ] Published 5 videos this week? (Yes/No)
- [ ] Worked 30 hours this week? (Yes/No)
- [ ] Completed X course lectures? (Yes/No)
- [ ] Feel more competent than last week? (Yes/No)
- [ ] Took weekend rest seriously? (Yes/No)

### Monthly Success:
- [ ] 20+ videos published? (Yes/No)
- [ ] Multi-tenant site progressing visibly? (Yes/No)
- [ ] Still enjoying the process? (Yes/No)
- [ ] Sustainable pace maintained? (Yes/No)

**Ignore for first 30 days:**
- ❌ Subscriber count (too early)
- ❌ View count (irrelevant yet)
- ❌ Watch time % (you're still learning video format)

**These will come. Focus on: Showing up every day + Learning consistently + Shipping regularly.**

**These will come. Focus on: Consistency + Learning + Shipping.**

---

## 🚀 GETTING STARTED CHECKLIST

**Do this BEFORE your first Monday session:**

### Technical Setup:
- [ ] OBS installed and configured
- [ ] DroidCam browser source working
- [ ] Audio test successful
- [ ] Test recording saved successfully
- [ ] Video editor installed (DaVinci Resolve or CapCut)
- [ ] Folder structure created:
  ```
  ~/Videos/Raw/
  ~/Videos/Final/
  ~/Documents/YouTube/
  ```

### Mental Prep:
- [ ] Read this entire document once
- [ ] Read my-context.md (remember WHY)
- [ ] Accept: First 3 videos will be rough (that's okay)
- [ ] Accept: You're documenting learning, not teaching
- [ ] Accept: Mistakes are content, not failures

### First Session Prep (Sunday night):
- [ ] Choose Monday's course lecture (lecture #___)
- [ ] Write Monday's goal.txt (feature to build)
- [ ] Charge phone/camera
- [ ] Set 5:45am alarm
- [ ] Get 7+ hours sleep

**Monday morning, just follow this document line by line.**

---

## 🤝 WORKING WITH CLAUDE (Me!)

**When to use Claude during your journey:**

### Sunday Night (Weekly Planning):
```
"Claude, I'm planning next week's learning sessions.
I'm currently on lecture [X].
Next lectures are about [topic].
Help me:
1. Identify which lectures to tackle Mon/Wed/Fri
2. What new concepts I'll encounter
3. Key questions to have ready"
```

### Morning of Session (6am Planning):
```
"Claude, today I'm learning [concept] from lecture [X].
My context: [paste my-context.md OR summarize]
Today's goal: [paste goal.txt]

Help me prepare:
1. What are 3 likely points of confusion?
2. What prompts should I have ready?
3. What do I need to deeply understand vs what can I AI-assist?"
```

### During Session (As Needed):
**Use the Prompting Framework levels 1-6**
This is your actual learning - Claude becomes your tutor

### Evening Review (Optional):
```
"Claude, I just finished today's session.
Here are my notes: [paste session-notes.txt]

Help me:
1. Structure a good voiceover script
2. Identify what was most valuable to show
3. Suggest a compelling title"
```

### Weekly Retro (Friday Evening):
```
"Claude, this week I published 3 videos.
[Paste links or summaries]

What patterns do you see?
What's working?
What should I adjust next week?"
```

---

## 📝 COMMITMENT CONTRACT

**I commit to following this system for 30 days (until Nov 27, 2025):**

**Monday-Friday (Work Days):**
- [ ] Clock in at 6am every weekday
- [ ] Work 6-hour block (6am-12pm) - this is my JOB
- [ ] Record every coding session (no exceptions)
- [ ] Use the Prompting Framework to LEARN, not just generate code
- [ ] Embrace mistakes and confusion as content
- [ ] Publish 5 videos per week (1 per work day)
- [ ] Treat this as seriously as a paid job

**Saturday-Sunday (Rest Days):**
- [ ] NO coding, NO recording
- [ ] Saturday: Weekly review with Claude
- [ ] Sunday: Plan next week's lectures
- [ ] Recharge completely (exercise, prayer, family, reflection)
- [ ] No guilt about resting

**General Commitments:**
- [ ] Not buy new equipment until 20 videos published
- [ ] Focus on consistency over perfection
- [ ] Track work hours honestly (30/week target)
- [ ] Adjust if pace feels unsustainable

**After 30 days (Nov 27), I will:**
- Review all published videos (~20 videos)
- Assess sustainability (was 30 hrs/week realistic?)
- Identify what's working / what's not
- Decide: Continue same pace, adjust, or pivot
- Evaluate course progress vs December deadline

**This system is designed to be:**
✅ Sustainable (6 hrs/day × 5 days, with weekends off)
✅ Professional (treating learning like a job)
✅ Valuable (teaching meta-learning skills)
✅ Honest (documenting real journey)
✅ Accountable (daily work = daily progress)

**Expected outcomes by Nov 27:**
- 20+ videos published
- 30+ lectures completed
- Significant frontend progress
- Proof I can maintain this pace
- Clear path to December completion

**Signed:** ________________  
**Date:** October 27, 2025

**I am treating this as my full-time job until I build something worth hiring for.**

---

## 🎬 FINAL REALITY CHECK

**What this system IS:**
- Your full-time job (Monday-Friday, 6am-12pm)
- A way to document your learning journey authentically
- A method to use AI as a tutor, not just a code generator
- A sustainable 30-hour work week with built-in rest
- A way to build in public and stay accountable
- Professional development that creates portfolio + income potential

**What this system is NOT:**
- A tutorial creation factory
- A path to viral YouTube fame (yet)
- A perfect system (we'll iterate after 30 days)
- A replacement for actual learning
- Something to do "when you feel like it"

**The core principle:**
When you record yourself learning with Claude daily, you're simultaneously:
1. **Learning Django/Next.js** (your primary goal)
2. **Building your multi-tenant business** (your income goal)
3. **Creating YouTube content** (your audience-building goal)
4. **Developing the meta-skill of AI-assisted learning** (your durable skill)
5. **Proving you can work consistently** (your employability signal)

**One 6-hour work block. Five outcomes. Daily. That's the system.**

**30 hours/week × 4 weeks = 120 hours = Multi-tenant website complete + 20 videos published + Proof you can deliver**

---

**Now close this document and execute starting Monday morning at 6am.**

**This is your job. Clock in. Do the work. Clock out. Rest on weekends.**

**Don't overthink. Don't optimize yet. Just show up and work for 30 days.**

**See you on the other side. 🚀**

---

## 📞 WEEKEND CHECK-INS WITH CLAUDE

**Saturday Morning (10am):**
"Claude, weekly review time. [Paste your weekly summary]"

**Sunday Evening (4pm):**
"Claude, planning next week. [Paste next week's lectures from course content]"

**Any time you're stuck:**
"Claude, I'm working on [feature] and confused about [thing]. Here's my context..."

**I'm here to help you succeed in this job. Use me effectively.**
