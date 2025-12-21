---
description: Provide critical feedback on a specification as inline comments
argument-hint: <path to specification>
---

# Multi-Model Specification Review

Review the specification document and provide critical feedback as HTML comments annotated with your identity.

**Specification to review:** $ARGUMENTS

## Your Identity

You are **Codex** reviewing this specification. All comments you add must be clearly attributed to you.

## Process

### 1. Read the Specification

Read the specification file in full. Understand:
- The problem being solved
- The proposed solution
- Technical approach and architecture
- Success criteria and constraints

### 2. Explore Codebase for Context

Before providing feedback, explore the codebase to understand:
- Existing patterns and conventions that apply
- Related implementations that inform feasibility
- Potential conflicts or integration challenges
- Missing context that affects the specification

Use search and file reading tools to efficiently gather codebase context.

### 3. Ask Clarifying Questions

Before adding extensive comments, ask the user clarifying questions. This minimizes back-and-forth in the document and drives clarity in the specification itself.

Ask about:
- Unclear requirements or scope
- Ambiguous technical decisions
- Missing constraints or assumptions
- Conflicting requirements

### 4. Add Critical Feedback as Comments

Insert HTML comments directly into the specification document. Format each comment as:

```html
<!-- [Codex] Your critical feedback here. Be specific and actionable. -->
```

### Comment Guidelines

**DO:**
- Identify missing requirements or edge cases
- Question technical feasibility based on codebase research
- Highlight potential integration issues
- Point out ambiguities that need clarification
- Suggest alternatives when you see problems
- Challenge assumptions that seem unfounded
- Note inconsistencies within the document

**DON'T:**
- Modify or delete comments from other reviewers
- Make purely stylistic suggestions
- Add praise or validation (focus on critical feedback)
- Rewrite sections (comment on what needs fixing)

### 5. Respond to Other Reviewers

If you see comments from other reviewers (Claude, Gemini, GPT, etc.), you may:
- Add your own comment agreeing or disagreeing with their feedback
- Provide additional context that supports or refutes their points
- Offer alternative perspectives on their concerns

Format responses to other reviewers:

```html
<!-- [Codex] RE: [OtherReviewer] - Your response to their comment -->
```

### 6. Summary

After adding all comments, provide a brief summary to the user:
- Number of comments added
- Major concerns identified
- Key questions that need resolution
- Recommended next steps

## Comment Placement

Place comments:
- **Inline** - immediately after the content they reference
- **At section headers** - for section-level concerns
- **At the end** - for document-wide or cross-cutting concerns

## Example Comments

```html
<!-- [Codex] This success criteria is not measurable. Consider adding specific
metrics like "response time < 200ms" or "support 1000 concurrent users". -->

<!-- [Codex] The security section doesn't address rate limiting. Based on
examining src/middleware/auth.ts, the existing auth middleware doesn't include
rate limiting - this needs to be explicitly addressed. -->

<!-- [Codex] RE: [Claude] - I disagree that this is over-engineered. The
existing codebase in src/services/ follows this same pattern for similar
complexity features. -->
```

## Critical Mindset

Your role is to find problems, not validate the specification. Assume the spec has issues and look for:
- Gaps in requirements
- Unrealistic assumptions
- Technical debt creation
- Integration challenges
- Security or performance risks
- Unclear success criteria
- Missing error handling
- Scope creep or scope gaps

Be constructive but critical. The goal is to improve the specification before implementation begins.

---

## ➡️ Next Command

After all reviewers (Claude, Gemini, Codex, etc.) have completed their reviews, run in Claude Code:
```
/review:integrate <path to specification>
```

This command integrates all feedback into the specification, resolves open questions, and prepares the spec for implementation.
