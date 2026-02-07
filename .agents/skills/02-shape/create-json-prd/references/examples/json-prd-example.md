# Example PRD JSON (Ralph)

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
    "framework": "React",
    "hosting": "Cloudflare Pages",
    "database": "D1",
    "auth": "single shared login"
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
  "qualityGates": ["pnpm test", "pnpm run lint", "pnpm run typecheck"],
  "stories": [
    {
      "id": "US-001",
      "title": "Add priority field to database",
      "status": "open",
      "dependsOn": [],
      "description": "As a developer, I want to store task priority so it persists across sessions.",
      "acceptanceCriteria": [
        "Add priority column with default 'medium'",
        "Example: creating a task without priority -> defaults to 'medium'",
        "Negative case: invalid priority 'urgent' -> validation error",
        "Migration runs successfully"
      ]
    }
  ]
}
```
