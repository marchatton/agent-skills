# Example JSON PRD (Ralph schema)

```json
{
  "version": 1,
  "project": "Task Priority System",
  "overview": "Add priority levels to tasks so users can focus on what matters most.",
  "goals": [
    "Allow assigning priority (high/medium/low) to any task",
    "Enable filtering by priority"
  ],
  "nonGoals": [
    "No automatic priority assignment"
  ],
  "successMetrics": [
    "Users can change priority in under 2 clicks"
  ],
  "openQuestions": [
    "Should priority affect ordering within a column?"
  ],
  "stack": {
    "framework": "Next.js",
    "database": "Postgres"
  },
  "routes": [
    { "path": "/tasks", "name": "Task List", "purpose": "View and filter tasks" },
    { "path": "/tasks/:id", "name": "Task Detail", "purpose": "Edit task priority" }
  ],
  "uiNotes": [
    "Priority badge colors: high=red, medium=yellow, low=gray"
  ],
  "dataModel": [
    { "entity": "Task", "fields": ["id", "title", "priority"] }
  ],
  "importFormat": {
    "description": "Not applicable",
    "example": {}
  },
  "rules": [
    "Priority defaults to medium when not set"
  ],
  "qualityGates": ["pnpm lint", "pnpm test", "pnpm build"],
  "stories": [
    {
      "id": "US-001",
      "title": "Persist priority for tasks",
      "status": "open",
      "dependsOn": [],
      "description": "As a user, I want tasks to store priority so it persists across sessions.",
      "acceptanceCriteria": [
        "Add priority field with allowed values: high | medium | low (default: medium)",
        "Example: create a task without specifying priority -> priority is medium",
        "Negative case: set priority to 'urgent' -> validation error",
        "Quality gates pass"
      ],
      "passes": false,
      "notes": ""
    },
    {
      "id": "US-002",
      "title": "Show priority badge in task list UI",
      "status": "open",
      "dependsOn": ["US-001"],
      "description": "As a user, I want to see task priority at a glance in the list.",
      "acceptanceCriteria": [
        "Each task card shows a priority badge: high/medium/low",
        "Example: a high-priority task renders a red badge",
        "Negative case: tasks with missing priority still render (badge shows medium/default)",
        "Verify in browser using $dev-browser: confirm badge is visible without hover and readable",
        "Capture screenshot evidence at <dossier>/artifacts/e2e/priority-badge.png",
        "Quality gates pass"
      ],
      "passes": false,
      "notes": ""
    }
  ]
}
```
