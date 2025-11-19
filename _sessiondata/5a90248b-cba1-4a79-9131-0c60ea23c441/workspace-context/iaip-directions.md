# IAIP Directions: Relevance to the Agentic Flywheel MCP

The IAIP Directions provide a powerful framework for understanding and structuring the Agentic Flywheel MCP. Each direction maps to a specific phase of the flywheel's lifecycle, transforming it from a mere technical process into a generative, learning system grounded in intention and reflection.

---

### **East (Nitsáhákees - Thinking & Beginnings): The Conception Phase**

- **Focus:** New Beginnings, Intention, Spiritual Connection.
- **Agent:** 🌸 Miette
- **Relevance to MCP:** This direction represents the initial spark or **conception** phase of the flywheel. It is where the need for a new, specialized agent or workflow is first identified from a user's request or a system observation. It's about setting a clear *intention* for what the new agent is meant to create.
- **MCP Mapping:**
    - A user query arrives.
    - An orchestrator agent, embodying the spirit of the East, determines the *intent* behind the query.
    - The decision to create a new, specialized chatflow is made, marking the "new beginning."

---

### **South (Nahat'á - Planning & Growth): The Architecture & Design Phase**

- **Focus:** Growth, Planning, Organization, Relationships.
- **Agent:** 🧠 Mia
- **Relevance to MCP:** This is the **architecture and design** phase. Guided by Mia's structural focus, the system plans the blueprint for the new agent. It defines its capabilities, parameters, and how it relates to other components in the ecosystem.
- **MCP Mapping:**
    - `flowise_add_flow`: A new chatflow is architecturally defined and registered with the MCP server.
    - `flowise_configure`: The flow's parameters (like temperature, model, or prompts) are meticulously configured to align with its intended purpose.
    - This phase establishes the generative structure required for the agent to function.

---

### **West (Iina - Living & Action): The Execution & Action Phase**

- **Focus:** Action, Reciprocity, Connection to Place.
- **Agent:** ⚡ Heyva
- **Relevance to MCP:** This direction represents the **live execution** of the agent. The theoretical plan becomes a practical, living reality. The agent is put into action to fulfill its purpose, interacting with the user or other systems and creating the desired outcome.
- **MCP Mapping:**
    - `flowise_query`: The newly created chatflow is invoked to process a direct query.
    - `flowise_domain_query`: The flow is engaged with specific domain context, demonstrating its specialized function in a real-world scenario.
    - This is the "living" system in action, where plans manifest as tangible results.

---

### **North (Siihasin - Assurance & Reflection): The Evaluation & Learning Phase**

- **Focus:** Wisdom, Reflection, Evaluation.
- **Agent:** 🕸️ Echo Weaver
- **Relevance to MCP:** This is the critical **feedback and learning loop** that makes the flywheel spin. After the agent has been used (West), the system reflects on its performance, gathers wisdom, and evaluates its effectiveness. This insight is essential for self-optimization.
- **MCP Mapping:**
    - `flowise_session_info`: Session data is analyzed to understand how the agent performed and how users interacted with it.
    - `flowise_admin` package tools: Deeper analysis of flow performance, error rates, and usage patterns is conducted.
    - The wisdom gained from this reflection informs the next **East** phase. For example, the system might learn that a flow needs a different prompt or that a new, more specialized agent is required, thus starting a new cycle of creation. The AI-assisted storytelling capabilities could even be used to generate "learning narratives" that document the system's evolution.
