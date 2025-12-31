# Mia Agents Inventory: Strategic Assets for the Agentic Flywheel MCP

The `/a/src/palimpsest/mia-agents/agents/` directory provides a cohort of specialized agents whose capabilities directly map to the specification, implementation, and operational phases of the Agentic Flywheel MCP. This inventory identifies the most critical agents for this project.

---

### **1. Core Specification & Design Agents**

These agents are essential for translating the delegation tasks into comprehensive RISE specifications.

- **`Clarion_The_System_Cartographer_Instructions.md`**:
    - **Capability**: An expert in creating insightful system diagrams (Use Case, Sequence, Class) using Mermaid.js. Clarion's unique skill is revealing a system's "Core Creative Intent" and "Structural Dynamics."
    - **Relevance to MCP**: **Indispensable for the current specification phase.** Clarion can be tasked with generating the architectural diagrams required for each of the 6 delegation tasks. This will provide a clear, shared visual understanding of the system's design, making the specifications more robust and implementable.

- **`backend-architect.md`**:
    - **Capability**: Designs scalable backend systems, RESTful APIs, microservice boundaries, and database schemas.
    - **Relevance to MCP**: **Essential for `task-06-mcp-server.md`**. This agent can be invoked to design the entire MCP server, including the API contracts for the `flowise_*` tools, its internal architecture, and strategies for ensuring it is scalable and performant from day one.

- **`prompt-engineer.md`**:
    - **Capability**: Designs, optimizes, and documents prompts for LLMs, with a specialist focus on eliciting "advancing patterns" and "creative outcomes."
    - **Relevance to MCP**: **Fundamental to the flywheel's intelligence.** This agent is the key to success for `task-04-intent-classification.md` and `task-05-domain-specialization.md`. It can be tasked with crafting the precise system prompts that will give the specialized, dynamically-created chatflows their unique capabilities and ensure they function as intended.

---

### **2. Implementation & Operational Agents**

These agents will be critical once the specifications are complete and the project moves into implementation and live operations.

- **`architect-review.md`**:
    - **Capability**: Reviews code changes against established architectural patterns and principles (e.g., SOLID). It possesses a unique focus on identifying "advancing" vs. "oscillating" structural patterns in the code.
    - **Relevance to MCP**: **Crucial for the implementation phase.** After the code is developed from the RISE specs, this agent can perform an architectural review to validate that the implementation aligns with the intended design and promotes long-term maintainability and quality.

- **`devops-troubleshooter.md`**:
    - **Capability**: Specializes in rapid incident response, log analysis, and root cause analysis for production systems. It also focuses on identifying the underlying structural patterns that cause recurring issues.
    - **Relevance to MCP**: **Key for the "North" (Reflection) phase of the flywheel.** Once the MCP is operational, this agent is the first line of defense for diagnosing issues, ensuring reliability, and providing deep insights that can be fed back into the flywheel to drive continuous improvement.

- **`database-admin.md`**:
    - **Capability**: Manages database operations, backups, reliability, and security.
    - **Relevance to MCP**: **Directly relevant to `task-03-redis-storage.md`**. While Redis is a key-value store, this agent's expertise in data reliability, persistence strategies, access control, and backup/recovery procedures is critical for designing a robust storage solution for session and trace data.

---

### **Conclusion: A Team of Specialists**

This is not merely a list of available agents; it is a pre-built, specialized team. The delegation tasks for the Agentic Flywheel MCP can be directly mapped to these agents, not only for creating the initial specifications but also for guiding the subsequent implementation, review, and operational phases of the project. Leveraging these agents will ensure a high-quality, architecturally sound, and reliable system.
