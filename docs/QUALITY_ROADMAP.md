# Repository Quality Roadmap

This roadmap defines how to upgrade the 39 assignments without breaking their original learning goals or deleting useful work.

## Quality gates for every assignment

- [ ] Confirm the assignment's original requirements and learning outcomes.
- [ ] Inspect the full folder tree and identify the real entry point.
- [ ] Check Python syntax and notebook JSON validity.
- [ ] Verify imports, relative paths, and data-file references.
- [ ] Identify dependency versions and document a reproducible setup.
- [ ] Move credentials to environment variables; add only sanitized examples.
- [ ] Add input validation and clear, actionable error messages where appropriate.
- [ ] Add focused tests for reusable or non-trivial logic.
- [ ] Run the project using its documented command when dependencies and credentials are available.
- [ ] Update the README with setup, execution, expected output, limitations, and attribution.
- [ ] Record what was actually tested; never claim an unrun test passed.

## Upgrade phases

### Phase 1 — Repository foundation
Completed: root README, 39-topic roadmap, ignore/editor settings, contribution standards, Python/notebook validator, and GitHub Actions workflow.

### Phase 2 — Assignment-by-assignment audit
Inspect each assignment before editing. Fix broken paths, imports, unsafe credential handling, stale instructions, and avoidable duplication. Keep original deliverables unless redundancy is confirmed.

### Phase 3 — Reliability
Add focused tests and reproducible dependency instructions. Validate notebooks and scripts. Exercise app/API entry points where services and credentials are available.

### Phase 4 — Learning experience
Improve explanations, architecture diagrams, sample inputs/outputs, screenshots, and troubleshooting notes. Keep explanations accurate and appropriate to the assignment's level.

### Phase 5 — Portfolio polish
Add a consistent catalog, meaningful summaries, technology tags, and verified demo links. Do not publish placeholder URLs as live demos.

## Important boundaries

- This repository contains independent assignments, not one monolithic application.
- Do not blindly merge dependency files across assignments.
- Do not delete datasets, notebooks, ZIP submissions, or generated outputs until their role is understood.
- Do not fabricate API responses, screenshots, benchmark results, deployment status, or test results.
- Review licensing and repository suitability before removing or replacing large datasets and model artifacts.
