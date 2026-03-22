# Product Discovery Guide

Load this file when conducting discovery interviews. Contains detailed probing questions, red flags, and research guidance for each section.

---

## Red Flags (Challenge Immediately)

- **"There's no competition"** → Search before accepting. Name what you find.
- **"The market is huge"** → Who specifically? Do they pay for things in this category?
- **"Developers would love this"** → Which developers? What context? Have you talked to any?
- **"It could also work for..."** → You're reaching. Who does it *actually* work for?
- **"Eventually we'd add..."** → What does v1 do without that?
- **Defending the idea instead of examining it** → Name it: "That sounds like a defense, not an examination."

## Green Flags (Acknowledge and Document)

- "I built this because I wanted it" — honest origin, often the real customer
- Naming a specific person who has the problem (not a category)
- Evidence that people pay for adjacent things (price anchors exist)
- A moat based on something structural, not just "we'll execute better"
- "Actually, now that you mention it..." — new realization surfacing
- "The real problem is..." — getting to the core

---

## Section 1: The Spark

### Questions
- What specifically triggered this? (A moment, a frustration, a job-to-be-done)
- Is this a problem you have, or a problem you observed?
- Why now? What's different about now vs. six months ago?
- Why you specifically? What makes you positioned to solve this?

### Push Back If
- The spark is vague ("I thought it would be cool")
- The answer is "I saw a market opportunity" with no personal connection — possible but warrants scrutiny
- The timeline doesn't make sense (why is this the right time?)

---

## Section 2: The Customer

### Questions
- Describe the specific person in your head when you explain this product. Job title, context, what they're doing when they need this.
- How often would they use it? (Daily / weekly / monthly / annually / once)
- Who makes the decision to use it — them, their employer, someone else?
- What's their success metric? Not yours — theirs. How do they know it worked?
- What's their emotional state when they'd seek this out? (Frustrated, overwhelmed, curious, bored)

### Push Back If
- Customer is a category ("developers", "small businesses", "content creators")
- Frequency is vague ("whenever they need it")
- Success metric is from your perspective ("they use it 5x/week"), not theirs ("they got the report done before the meeting")

### Frame It
"Who is the one person you'd show this to first? Describe that person."

---

## Section 3: Competitive Landscape

### Research First
Before asking the user, search:
- "[problem] tool", "[problem] software", "[category] alternatives"
- "[problem] reddit" or "[problem] hacker news" — often surfaces what people actually use
- "[obvious category] pricing" to understand price anchors

Name what you find before the user asserts there's no competition.

### Questions
- What would someone do if this didn't exist? (The real alternative is often "nothing" or "spreadsheet" — that's fine, but name it)
- What does that alternative do better than you? No hedging.
- What can you do that the alternative *fundamentally cannot* — not just "better", cannot?
- Are you competing with the right thing? Sometimes the real competitor isn't the obvious one.

### Push Back If
- "There's no competition" before you've searched
- Competitive advantage is "better UI" or "easier to use" — these are execution claims, not structural moats
- The real alternative is a behavior, not a tool (e.g., "just not tracking it at all")

---

## Section 4: Willingness to Pay

### Questions
- What do the alternatives charge? (Even "free" alternatives — what's the paid tier?)
- Would *you* pay for this? How much would feel cheap? How much would feel expensive?
- Who holds the budget here — the user or their employer? (Changes the price ceiling significantly)
- Is this a "nice to have" or a "costs me money / time if I don't have it" problem?

### Research
Search "[competitor] pricing" for 2-3 alternatives to establish price anchors.

### Push Back If
- "People will pay for value" without any price anchors
- B2B pricing assumptions without understanding the buyer (individual vs. team vs. company)
- The problem is in the "nice to have" category but the pricing assumes "must have"

---

## Section 5: Monetization Model

### Options to Discuss (pick 1-2 that fit)

| Model | Good for | Watch out for |
|-------|----------|---------------|
| **Subscription** | Recurring workflow tools, ongoing value | Churn if value isn't felt regularly |
| **One-time purchase** | Utilities, tools used occasionally | No recurring revenue; hard to fund ongoing development |
| **Freemium** | Products that get better with more users, viral loops | Free tier must deliver real value; support burden |
| **Usage-based** | AI/API products, high variable cost | Revenue unpredictable; complex to price |
| **Consulting wrapper** | Niche expertise + tool | Your time is the bottleneck |
| **Open source + paid hosting** | Developer tools with community value | Hard to monetize unless hosting is genuinely easier |

### Questions
- Who pays — the user themselves, or does someone else (employer, client) pay?
- How often do they derive value? (Guides subscription vs. one-time)
- Is there a natural "free" tier, or would a trial period work better?

### Push Back If
- "Freemium" chosen without a clear free→paid conversion trigger
- "Subscription" chosen for a tool used monthly or less (one-time may fit better)
- No thought given to who actually holds the credit card

---

## Section 6: Distribution

### Questions
- How do people currently find solutions to this problem? (Google, reddit, word of mouth, their manager told them?)
- Where does your specific customer spend time online?
- Do you have existing access to this audience? (Newsletter, community, past customers, social following)
- What's your realistic first 100 customers plan?

### Channels to Discuss

| Channel | Works when | Doesn't work when |
|---------|-----------|-------------------|
| **SEO** | Clear problem people search for | Problem isn't Googled; competitive keyword space |
| **Community** | You're already a member; niche audience | Community doesn't exist; you're an outsider |
| **Word of mouth** | Product creates visible results others want | Outcome is private; low usage frequency |
| **Cold outreach** | B2B, high ticket, clear target list | B2C; low-value product; no list |
| **Product Hunt** | Developer/maker audience; launch moment | Consumer product; needs ongoing distribution |
| **Content/newsletter** | You already create content in this space | Starting from zero; slow to compound |

### Push Back If
- "I'll post on Twitter/X" without an existing audience
- "SEO" without evidence people search for this problem
- No answer to "how do your first 10 customers hear about you"

---

## Section 7: MVP Hypothesis

### Frame It
"What's the one assumption that, if wrong, makes the whole thing not worth building?"

### Questions
- What's the smallest version that tests that assumption?
- What does "it's working" look like in 60-90 days? (Specific signal — not "people like it")
- What would you do differently if you knew the core assumption was wrong?

### Push Back If
- MVP includes more than 1-2 core flows
- "It's working" metric is vague (engagement, interest, traffic)
- MVP tests execution rather than the core assumption

---

## Section 8: Verdict

### Criteria for Go
- Specific customer identified with believable problem
- Evidence (or strong analog) of willingness to pay
- At least one structural advantage over alternatives
- Realistic path to first 10 customers
- MVP tests the core assumption

### Criteria for Conditional Go
- Most criteria met but one significant open question remains
- State the condition explicitly: "Go if [X] is true"

### Criteria for No-Go
- Core assumption can't be tested without major investment
- No believable path to willingness to pay
- No structural advantage — only execution advantage
- No realistic distribution path

### Always Document: What Would Need to Be True
Even for a definite No-Go, document conditions that would change the verdict. These may include:
- A competitor shutting down or pivoting
- A regulatory change
- A technology becoming available or affordable
- A market that doesn't exist yet maturesThese are sleeping ideas, not dead ones.
