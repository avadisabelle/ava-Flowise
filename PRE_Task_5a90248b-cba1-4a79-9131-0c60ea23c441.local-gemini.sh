#!/bin/bash
# Enhanced Gemini-CLI Launcher for Agentic Flywheel MCP Delegation Tasks
# Session: 5a90248b-cba1-4a79-9131-0c60ea23c441
# Trace: a50f3fc2-eb8c-434d-a37e-ef9615d9c07d

_GEMINII_DEFAULT_MODEL_set pro

geminiid "# Agentic Flywheel MCP - Gemini Collaboration Context

## 🎯 Mission Overview

You are collaborating with Claude on developing RISE specifications for the **Agentic Flywheel MCP** - a system that enables intelligent Flowise chatflow orchestration with Langfuse tracing and Redis storage.

**What Claude Online Has Prepared:**

Claude has created a comprehensive delegation workspace in:
- **Workspace:** _sessiondata/5a90248b-cba1-4a79-9131-0c60ea23c441/
- **Trace Session:** a50f3fc2-eb8c-434d-a37e-ef9615d9c07d (for Langfuse)
- **Project Session:** 5a90248b-cba1-4a79-9131-0c60ea23c441

This workspace contains:
1. **6 Delegation Task Prompts** (delegations/) - Ready for parallel execution
2. **Orchestration Manifest** - Strategy and integration map
3. **Cherry-Pick Tracker** - Quality validation system
4. **Results Folder** - Where completed specs should go

## 📋 Your Role as Gemini

**Primary Task:** Help execute one or more of the 6 component specification tasks

**Available Tasks:**

1. **task-01-flowise-integration.md** (60-90 min, HIGH priority)
2. **task-02-langfuse-tracing.md** (60-90 min, HIGH priority)
3. **task-03-redis-storage.md** (45-60 min, MEDIUM priority) ⭐ Recommended start
4. **task-04-intent-classification.md** (60-75 min, HIGH priority)
5. **task-05-domain-specialization.md** (50-65 min, MEDIUM priority)
6. **task-06-mcp-server.md** (70-90 min, HIGH priority)

## 🎨 RISE Framework Guidance

All specifications must follow **RISE** principles (Reverse-engineer → Intent-extract → Specify → Export):

**Creative Orientation:**
- Focus on what users CREATE (not problems solved)
- Use 'enables users to create...' language
- Emphasize structural dynamics over willpower

✅ Use: enables, creates, manifests, advances, natural progression
❌ Avoid: solves, fixes, handles, must, forces

## 📁 Required Reading

Before starting:
1. **Master Spec:** rispecs/app.spec.md (overall vision)
2. **RISE Framework:** __llms/llms-rise-framework.txt (principles)
3. **Task Assignment:** _sessiondata/.../delegations/task-XX-[name].md
4. **Existing Code:** src/agentic_flywheel/agentic_flywheel/

## 🚀 Suggested Starting Approach

**PHASE 1: Context Gathering (20-30 min) - DO THIS FIRST**

Explore and gather context from your accessible paths:

1. **Explore IAIP Directions** (/src/IAIP/directions/)
   - Review directional guidance (EAST, SOUTH, NORTH, WEST)
   - Understand where we are in the methodology
   - Document relevance to Agentic Flywheel MCP
   - Save findings to: _sessiondata/.../workspace-context/iaip-directions.md

2. **Explore Mia Agents** (/src/palimpsest/mia-agents/agents/)
   - List available agent definitions
   - Identify agents that could help with specification tasks
   - Document agent capabilities and potential contributions
   - Save findings to: _sessiondata/.../workspace-context/mia-agents-inventory.md

3. **Explore Claude Embodiments** (/src/home/jgi/.claude/CLAUDE.md)
   - Review Claude's embodiment patterns
   - Understand collaboration protocols
   - Extract relevant patterns for this work
   - Save findings to: _sessiondata/.../workspace-context/claude-embodiments.md

4. **Create GEMINI.md Observation**
   - Document your understanding after context gathering
   - Explain how local resources inform the delegation strategy
   - Provide specific recommendations for agent collaboration
   - Save to: _sessiondata/5a90248b-cba1-4a79-9131-0c60ea23c441/GEMINI.md

**PHASE 2: Execute Specification Task (60-90 min)**

Choose one task based on gathered context:

- **task-03-redis-storage.md** (45-60 min) ⭐ Recommended for first contribution
- **task-01-flowise-integration.md** (60-90 min) If you found relevant Mia agents
- **task-02-langfuse-tracing.md** (60-90 min) If IAIP directions inform observability
- **task-04-intent-classification.md** (60-75 min) If agent patterns apply to routing
- **task-05-domain-specialization.md** (50-65 min) If embodiments show domain patterns
- **task-06-mcp-server.md** (70-90 min) If you understand full integration landscape

**PHASE 3: Collaboration Strategy (15 min)**

After completing a specification:

1. **Identify Mia Agent Contributions**
   - Which Mia agents could help validate your spec?
   - Which agents could execute the implementation?
   - Document in: _sessiondata/.../workspace-context/agent-delegation-opportunities.md

2. **Update Trace in Langfuse**
   - Use trace session: a50f3fc2-eb8c-434d-a37e-ef9615d9c07d
   - Document: What you gathered, what you created, what comes next
   - Link observations hierarchically

3. **Propose Skills** (if applicable)
   - If mobile agents need new capabilities, draft skill spec
   - Save to: _sessiondata/.../workspace-context/proposed-skills/

## 🔍 Trace Context (from _env.sh)

**Langfuse Tracing:**
- Main trace session: a50f3fc2-eb8c-434d-a37e-ef9615d9c07d
- Use coaiapy-mcp tools to document work
- Link observations hierarchically

**Session Context:**
- Workspace session: 5a90248b-cba1-4a79-9131-0c60ea23c441
- Previous work: Investigation complete, master spec created
- Current phase: Component specification development

## 💡 Success Criteria

**Context Gathering Success:**
- [ ] IAIP directions explored and documented
- [ ] Mia agents inventoried with capabilities
- [ ] Claude embodiments reviewed
- [ ] Findings stored in workspace-context/ folder
- [ ] GEMINI.md created with synthesis and recommendations

**Specification Task Success:**
- [ ] Specification follows RISE framework
- [ ] All required sections complete
- [ ] At least 3 creative advancement scenarios
- [ ] Success metrics quantified
- [ ] Another LLM could implement from spec alone
- [ ] Saved to results/ folder with correct naming

**Collaboration Success:**
- [ ] Agent delegation opportunities identified
- [ ] Langfuse trace updated with your contributions
- [ ] Proposed skills documented (if applicable)
- [ ] Clear handoff notes for Claude to cherry-pick

## 📂 Workspace Structure You'll Create

After your work, the workspace should contain:

\`\`\`
_sessiondata/5a90248b-cba1-4a79-9131-0c60ea23c441/
├── workspace-context/              # NEW - Your context gathering
│   ├── iaip-directions.md
│   ├── mia-agents-inventory.md
│   ├── claude-embodiments.md
│   ├── agent-delegation-opportunities.md
│   └── proposed-skills/
│       └── [skill-name].skill.md
├── results/                        # Your completed specs go here
│   └── [name].spec.md
└── GEMINI.md                      # Your observations and strategy
\`\`\`

---

**Questions to Guide Your Work:**
1. What IAIP direction principles apply to Agentic Flywheel MCP?
2. Which Mia agents have capabilities useful for specification or implementation?
3. How do Claude embodiments inform the delegation strategy?
4. What new skills would help mobile agents contribute effectively?
5. Which specification task benefits most from the context you gathered?

**Ready to explore, gather, create, and collaborate!**
" \
/src/IAIP/directions/ \
/src/palimpsest/mia-agents/agents/ \
/src/home/jgi/.claude/ \
/src/palimpsest/skills-mia/ \
_sessiondata/5a90248b-cba1-4a79-9131-0c60ea23c441/ \
rispecs/ \
src/agentic_flywheel/ \
__llms/ \
_env.sh
