# AI Agent Workflow Automation

An AI-driven workflow automation system that converts business workflow definitions from Excel into executable, reusable software workflows.

The system accepts a natural-language request, identifies the appropriate workflow, executes its steps using registered tools and business logic, handles conditions and errors, and returns a structured execution result.

---

## 📌 Project Overview

The objective of this project is to build a reusable workflow automation system instead of creating a separate chatbot for every business workflow.

Workflow definitions are maintained in an Excel file and loaded dynamically into the application.

The system follows this flow:

```text
User Request
     ↓
FastAPI
     ↓
AI Workflow Agent
     ↓
Workflow Selection
     ↓
Workflow Registry
     ↓
Generic Workflow Engine
     ↓
Tool Registry / LLM
     ↓
Step Execution
     ↓
Final Result