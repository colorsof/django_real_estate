🧩 THE PROMPTING FRAMEWORK REFERENCE
Keep this handy during your coding session
LEVEL 1: Understanding Prompts
Use when: You encounter a new concept/technology

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
- "Explain Redux..." (for state management)
- "Explain JWT tokens..." (for authentication)
- "Explain REST APIs..." (for backend communication)
- "Explain React hooks..." (for frontend logic)







LEVEL 2: Planning Prompts
Use when: You understand the concept, need implementation guidance
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
- "I need to build user login with JWT..."
- "I need to create a form that posts to Django API..."
- "I need to store authentication state in Redux..."






LEVEL 3: Learning from Differences Prompts
Use when: Course/tutorial suggests one approach, Claude suggests another
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
- "Course uses class components, you suggested functional..."
- "Course uses fetch(), you suggested axios..."
- "Course stores token in localStorage, you suggested httpOnly cookies..."






LEVEL 4: Implementation with Explanation Prompts
Use when: Ready to code, want Claude to explain as you go
Template:
"Let's build [FEATURE] following [chosen approach].

As we code:
- Explain what each piece does and WHY
- Point out what I need to deeply understand vs what's boilerplate
- Connect this to concepts we discussed earlier

I'll type. You guide and explain.
Start with: [first file/function]"

Examples:
- "Let's build the authSlice.js Redux file..."
- "Let's create the login form component..."
- "Let's set up the API endpoint for user registration..."







LEVEL 5: Debugging & Understanding Prompts
Use when: Code doesn't work, or works but you don't know why
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
- "Getting 'undefined is not a function' error..."
- "The login works but token doesn't persist..."
- "Code works but I don't understand the async/await part..."








LEVEL 6: Testing Understanding Prompts
Use when: You think you understand, want to verify
Template:
"I've built [FEATURE] and I think I understand it.

Let me explain [CONCEPT] back to you in my own words:
[Your explanation]

Is my understanding correct?
What am I missing or misunderstanding?"

Examples:
- "Let me explain how Redux works..."
- "Let me explain the JWT authentication flow..."
- "Let me explain why we use serializers in Django..."