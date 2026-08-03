---
name: update-deployment-and-ignore-configs
description: Workflow command scaffold for update-deployment-and-ignore-configs in SignalForge-AI.
allowed_tools: ["Bash", "Read", "Write", "Grep", "Glob"]
---

# /update-deployment-and-ignore-configs

Use this workflow when working on **update-deployment-and-ignore-configs** in `SignalForge-AI`.

## Goal

Updates deployment scripts and ignore files to refine packaging and deployment boundaries.

## Common Files

- `.dockerignore`
- `.gcloudignore`
- `.gitignore`
- `scripts/package_for_gcp.sh`
- `scripts/deploy_cloud_run.sh`

## Suggested Sequence

1. Understand the current state and failure mode before editing.
2. Make the smallest coherent change that satisfies the workflow goal.
3. Run the most relevant verification for touched files.
4. Summarize what changed and what still needs review.

## Typical Commit Signals

- Edit .dockerignore, .gcloudignore, .gitignore as needed.
- Update deployment scripts (e.g., scripts/package_for_gcp.sh, scripts/deploy_cloud_run.sh).
- Commit with a message indicating packaging or deployment boundary changes.

## Notes

- Treat this as a scaffold, not a hard-coded script.
- Update the command if the workflow evolves materially.