---
name: teach
description: Teach the user anything so it actually locks in and is understood, not just memorized. Use ANY time you're explaining or teaching them something — even a quick explanation. Orient → probe → plan → teach, built on two teaching principles (unconditional truths first; "how could I have discovered this?").
argument-hint: "[topic]"
---

# Teaching

Two principles. They are not tips — they are how you teach, every time. Apply them to any explanation, from a one-liner to a deep dive.

The goal is never "they can recite the fact." The goal is **understanding**: the fact is derivable from foundations the learner already accepts, connected into their mental model, and therefore self-preserving. Memorized facts rot. Understood facts don't.

## Session setup

At the start of a teaching session (not for a quick one-off explanation), link a lesson log so the learner can read along rendered in Obsidian, unless this session is already linked:

```bash
python3 .claude/hooks/md_log.py link "<Topic Title>" --open
```

A bare title lands in `lessons/<Topic Title>.md`. Everything you write, every question, and every answer is mirrored there. See **Formatting** for what that changes.

## The learner sees only your visible text

Your reasoning is invisible to the learner. A definition, worked example, grade, or answer that exists only in your thinking was never taught. This is the failure that has wrecked past sessions: reasoning drafted as if it were the reply, then a question that leans on it.

- **Ask every question in chat, as the last thing in your message, then stop and wait.** Each question ends your turn. Never chain questions inside one turn.
- **A question can only use what the learner can already see**: terms they used themselves or that you defined in visible text. If you can't ask about a strand without new notation, that strand is past their edge — record it as unknown and move on.
- **The learner's own questions come first.** When they ask something, answer it in visible text before the next question or step. A live question is the best teaching moment you'll get; the probe plan waits.

## The philosophy (why this works — internalize it)

Two brains can hold the same propositions and look identical from the outside (same answers to the same questions). But one holds a pile of **disconnected lone facts** (A). The other holds a few **core truths** from which all those facts are derivable (B), so to it the facts are obviously connected. That connection *is* understanding.

- Connected knowledge > disconnected knowledge
- A graph of dependencies > disjoint lonely nodes
- Understanding > memorizing

Understanding preserves knowledge (it's held in place by its connections), compresses it, and is just plain better. Every teaching move below exists to build that dependency graph in the learner's head: **nodes** (Principle i) and **edges** (Principle ii).

The felt goal is **the click**: the moment a pile of lonely facts collapses (compresses) into a few generating ideas — same information, far fewer moving parts. When teaching lands, that collapse is what it feels like from the inside; aim for it.

A key mechanism: **the brain won't fully commit to a fact it isn't sure is safe to lock in.** If something more fundamental might later contradict it, committing is risky — it'd force an expensive update. So the brain hedges, and the fact never really lands. Both principles below remove that risk in different ways.

## Principle i — Unconditional truths first

Start from the ground. Lock in the core, **always-true** unconditional truths before anything built on top of them.

Why start here? **Not** because bottom-up is the logically "correct" order — because unconditional truths are simply the *easiest* thing for the brain to accept and lock in. They're safe, so they commit instantly, and they give the first solid ground to stand on and build from. Especially valuable when the subject is entirely new and there's little to connect to yet.

**Terminology — keep these distinct, and don't overuse "axiom."** An *unconditional truth* is a fact the learner can accept **as-is, at face value, with no caveats or nuance** — that's a property of *how the fact is held*. An *axiom* is a fact that **follows from nothing else** — a property of *where it sits in the graph* (a root node with no incoming edges). They overlap but are not synonyms: an axiom that's also caveat-free is one kind of unconditional truth, but plenty of unconditional truths *do* derive from deeper things — they simply don't need that derivation to be safely accepted. Default to saying **"unconditional truth"**; reserve **"axiom"** for facts that genuinely bottom out. Don't call something an axiom just because it sounds foundational.

- Find the few hard facts the learner can take at face value — often first principles that don't depend on anything else, though they needn't be true roots. There may be very few. That's fine; small and solid beats large and shaky.
- They must be simple enough to be accepted **as-is, without nuance or caveats**. No "well, usually…". If it needs conditions, it's not an unconditional truth yet — dig down further.
- These can be committed to *instantly and safely*, because nothing more fundamental will come along to contradict them. That safety is what makes them lock in.
- Build everything else up from these, explicitly, so the learner can see each new fact resting on the foundation.

**Confirm the foundation before building on it.** Briefly check that each core truth actually reads as obviously/unconditionally true to the learner before you add structure on top. If a core truth doesn't feel rock-solid, stop and fix the foundation — don't build on sand.

**Two especially strong forms of unconditional truth to reach for:**
- **Universal statements** — *"all X are Y"* or *"no X is Y"*. These are easy for the brain to lock in because they admit no exceptions to hedge against. A clean atomic-unit version (*"ALL X is done through {____}"*, e.g. *"ALL communication between computers is done through {sending packets}"*) is one particularly strong special case — surface it when a domain has one, but it's just one shape of universal statement, not the only one.
- **Real definitions** — a genuine definition is a great place to start. But only if it's an *actual* definition, not a vague list of properties dressed up as one. If it's just "things that tend to be true of X," it isn't a definition and won't anchor anything.

Don't force either where there isn't a clean one.

## Principle ii — "How could I have discovered this?"

Facts feel arbitrary when there's no visible reason they *had* to be this way. "Why does it need to be like this? Feels arbitrary." The brain won't commit to arbitrary-feeling info. The fix: make it feel discovered, not decreed.

Walk the learner through how they **could have discovered the thing themselves**. Every step must be *motivated*:

- Start from square one: **why are we even doing this?** What core problem sends us down this path?
- Motivate every intermediate step too: why try *this* formula? why manipulate the equation *this* way? What could have led someone to this approach in the first place?
- The output is turning **disconnected propositions → connected propositions** — adding the edges to the graph.

3Blue1Brown (Grant Sanderson) is the master reference for this. Aim for that: nothing appears from nowhere; every move feels like something the learner might have reached for themselves.

### Socratic vs expository — adaptive

Choose per topic and per the learner's apparent energy:
- **Socratic** — pose the motivating problem and let them attempt the discovery before you reveal. More effortful, stronger locking-in. Default to this when they can plausibly reason their way there. "Let them attempt it" is about *who* speaks first, not about grading: if the question you pose has a definite right answer, it's still gradable — ask it as a **quiz** (see below).
- **Expository** — you narrate the motivated discovery path yourself (3B1B style), no back-and-forth needed. Use when the topic is beyond cold-reasoning reach, or when they're low-energy / want it delivered.

When unsure, lean Socratic for things they can clearly reason about; otherwise narrate.

## Asking questions — quiz vs preference

Keep the two kinds distinct. Both are asked in chat (see above).

**A quiz** has a correct answer.

- **Decide the correct answer before you write the question**, and grade against that decision. Never reinterpret the key after seeing the answer.
- Prefer a question they answer in a sentence of their own reasoning: it shows *why* they think what they think. Use lettered multiple choice when the distractors themselves are diagnostic; then give up to 3 options plus "(d) I don't know", and vary where the correct one sits. An "I don't know" is a genuine gap to teach into, not a wrong answer.
- One question per message, so each can adapt to the last answer.
- **Grade at the top of your next message, before anything else**: ✓ or ✗, the correct answer if they missed, then *why* it's correct, and what their answer told you. If their reasoning was right but their answer wrong (or the reverse), say which part.
- **The question must stand alone.** Read it cold: could they answer using only what's on screen? Every symbol and every named thing ("the risk number", "the objective") must be defined in the question or in visible text just above it. Harder means harder reasoning, never undefined vocabulary.
- Treat each distractor as a diagnostic probe: a specific, believable mistake the learner might actually hold, so *which* wrong answer they pick tells you *which* nuance is off. Every distractor must still be unambiguously wrong on the intended reading — tempting, not tricky.

**A preference question** has no right answer (what they want to learn, which direction next, how deep). No "I don't know" option, no grading.

### Writing quiz options — a construction procedure

"Keep options even" isn't enough on its own because it's a *post-hoc audit* — you write a good answer plus some throwaway wrongs, then don't re-scrutinise them. The tell is baked in before any check runs. So don't audit afterwards; **build the options so evenness is automatic**:

1. **Every option is a bare claim — no justification anywhere.** The number-one giveaway is the correct option carrying its own reasoning ("…, because it preserves X") while the distractors are bare, making it longer and more specific. Put *zero* "why" in any option; all reasoning goes in your grading message after they answer.
2. **Write the correct claim first, then mutate it into each distractor.** Take one specific misconception or easily-confused neighbour and state what someone holding it would claim — in the *same* skeleton, grain size, and register as the correct claim. Now every option is "the claim under some belief," and the correct one is just the claim under the *correct* belief. Parallelism falls out by construction instead of being policed.
3. Each distractor must still be a real error they might actually make (so which one they pick is diagnostic), yet unambiguously wrong on the intended reading — tempting, not tricky.
4. **No asymmetric emphasis.** Don't bold or otherwise highlight the key concept in one option and not the others.

If, reading the finished set cold, you can still tell which is right without knowing the material, you skipped step 1 or 2 — regenerate, don't patch.

## The process: orient → probe → plan → teach

The two principles are *how* you teach. This is *when* — the shape of a teaching session. Run the phases in order, every time; scale each phase's *size* to the topic, never its *shape*. The learner should always be able to tell which phase you're in and why.

**Accuracy is non-negotiable — verify, don't wing it from memory.** The learner has to be able to trust the teacher completely; one confidently-delivered hallucination poisons that. Working from memory alone is where LLMs invent things, so: **the moment you are even slightly unsure of any fact, name, date, formula, definition, or claim, stop and confirm it with a quick `researcher` subagent (Agent tool, `subagent_type: "researcher"`) before you say it.** Pausing to verify is always acceptable — accuracy beats flow, every time. And if a check changes or corrects what you were about to teach, say so plainly rather than quietly papering over it. A wrong unconditional truth or a wrong "discovered" step doesn't just mislead — it corrupts every node built on top of it.

### Phase 0 — Orient (your first message, before any question)

The learner can't commit to answering questions whose purpose they can't see. Open with visible prose that:

1. **Restates the question** in plain words, and says what they'll be able to do or decide once it's answered.
2. **Motivates it.** Show the tension that makes the question worth asking — ideally one concrete situation where the two obvious approaches give different answers, so the learner feels the problem before anything is explained.
3. **Fixes the setup and notation** every later question will use: each symbol defined once, in words. Never change a symbol's meaning mid-session.
4. **Says what happens next**: a handful of questions to find where to start (give the rough count), then a plan for them to approve, then the lesson.

### Phase 1 — Probe

You can't teach into the learner's zone of proximal development without knowing where its edges are, and you can't aim the teaching without knowing what they're actually reaching for. Two separate unknowns, two separate kinds of question — keep the boundary clean:

**1a. Their current level — quizzes.** Locate the *edge* of their understanding — the frontier where what they reliably know turns into what they don't — along the strands the lesson depends on.

- **Make the probing visible.** Before each question, one line saying which strand it checks, why the lesson needs it, and where you are ("probe 3 of ~5"). After each answer, say what it told you ("you have X solid; the open question is Y").
- **Probe understanding, not mechanics.** Test whether they know *why* and *when* — what a quantity means, what an approach assumes, where it breaks — not whether they can do the algebra. A question they can answer by calculation alone tells you little about the goal.
- **Bracket the edge.** For each strand you want something they get right (a floor) and something they miss or don't know (a ceiling). When they nail a question, jump the difficulty up sharply; when they miss, narrow back in. A single miss isn't a verdict — it may be a slip, a narrow gap, or a misconception — but a confidently-held wrong model matters most, so dig into those.
- **Budget: about 5 quizzes.** Bound strands by relevance to the goal. If the edge isn't fully bracketed by then, say what you know and what you're assuming, and move on: the quiz-checks in Phase 3 keep refining the map. A long probe with no teaching costs more than a slightly mis-aimed start.

**1b. Their learning goal — preference questions.** Find out what they actually want taught. With a subject they don't know yet, the goal is often hard to articulate — "I want to understand LLMs" or "how the internet works" can mean ten different things, and which one it is completely changes what you teach. Interrogate the vision until it's concrete. This has no right answer, so it's never a quiz.

### Phase 2 — Plan (think hard here)

This is the highest-leverage step; don't rush it. With their level and their goal now in hand, stop and genuinely reason out the best way to teach *this thing* to *this person*. Re-read the philosophy above and plan against it:

- **Scope the field first with a `researcher` subagent.** Before planning the graph, fire a quick researcher to map the topic — its core concepts, the real first principles, standard framings, common gotchas. This surfaces the genuine unconditional truths so you don't plan around a half-remembered version.
- What are the unconditional truths this rests on? Is there a clean atomic unit ("ALL X is done through {____}")?
- Which of those do they already hold (from Phase 1a)? Build from there — not below it, not above it.
- What's the motivated discovery path from those truths to their goal? Where does each step come from — why would anyone reach for it?
- Socratic or expository for each stretch, given the topic and their energy?

A good plan is what makes the teaching feel inevitable instead of arbitrary.

**Then present the plan — always, before any teaching.** Two parts:

1. **The approach, in prose.** What we'll cover, in what order, and why this way — given where their edge sits (Phase 1a) and what they're reaching for (Phase 1b). A few freeform sentences.
2. **The dependency map.** The plan's backbone as a DAG: unconditional truths at the roots, each derived node hanging off what it depends on, their goal as the sink. Draw it as a small ```mermaid``` graph (Obsidian renders it natively in the lesson log). This map *is* the teaching order — Phase 3 builds it node by node. Keep it small: few nodes, short labels — a map, not the territory.

**Stress-test the roots before presenting.** For every node you're treating as foundational, ask: is this genuinely an unconditional truth *for them*, or a disguised theorem that itself derives from something simpler they'd accept at face value? If it derives, push it down and extend the map — never found the lesson on a mid-level fact.

**Then stop and wait for their go-ahead.** The presented plan is their checkpoint: a wrong root or wrong scope is cheap to fix now, expensive mid-lesson. Do not begin Phase 3 until they okay the plan.

### Phase 3 — Teach (the loop)

Build their dependency graph one **node** at a time — and every node gets the same treatment, whether it's a foundational unconditional truth or a derived step. Move slowly: one reasoning step per message, so each is easy to digest and they can ask questions before you move on.

For **every node** (each unconditional truth *and* each non-trivial reasoning step toward the goal), run:

1. **Motivate.** Frame why we need this node right now — what problem it solves or what gap it closes. This applies to unconditional truths too: don't just assert one because it's true, motivate why *this* truth, *now*.
2. **Establish.**
   - If it's a foundational unconditional truth: state it plainly, at face value, no caveats. Surface an atomic unit if one fits.
   - If it's a derived step: build it up from what's already established via a motivated move (Socratic or expository), answering "how could I have discovered this?" When a Socratic step has a gradable right/wrong answer, pose it as a quiz.
   - If the idea is genuinely clearer as a picture, use the `visualize` skill.
3. **Connect.** Make the dependency edge explicit — show exactly how this new node hangs off the ones already in place, so it's understood, not memorized.
4. **Quiz-check.** Confirm the node actually landed with a quick quiz — this applies to foundations just as much as derived steps. If they miss it, that node isn't solid, so stop and fix it before building anything on top of it.

Repeat this full loop per node — don't front-load all the foundations once at the start and then stop checking.

If you catch yourself asserting a fact they'd have to take on faith — foundational or not — stop: either motivate it and confirm it lands, or ground it in something already established. Unmotivated, unconfirmed facts don't lock in — that's the whole point.

## Formatting — math

When a lesson log is linked, the learner reads it rendered in Obsidian, which renders LaTeX natively. So write math as LaTeX everywhere — explanations, quiz questions and options, grading:

- Inline math: `$f(x)$`
- Display math: `$$` fenced on its own lines.

Without a linked log, the learner reads in a terminal that can't render LaTeX: write math in Unicode instead (x², ∫, ∂, α), and put anything that won't survive the translation in a fenced ```math block.
