

## Phase 2: Add stronger evaluation tasks

Add at least five tasks:

1. Bug fix task
2. Refactor task
3. Test-generation task
4. API endpoint task
5. Data transformation task

Each task should include:

- prompt
- starter code
- hidden or visible tests
- category
- difficulty
- expected evaluation behavior

## Phase 3: Improve the scoring model

Replace the simple pass/fail score with partial scoring.

Suggested approach:

- Count total tests
- Count passed tests
- Score = passed / total
- Save failure names
- Save execution time

## Phase 4: Add model comparison

Add a table that compares:

- model name
- task category
- score
- pass rate
- most common failure
- release recommendation

## Phase 5: Add ResearchOps features

Add fields for:

- experiment owner
- model version
- dataset version
- risk notes
- regression notes
- go/no-go recommendation

## Phase 6: Add leadership reporting

Create a report endpoint:

```text
GET /reports/leadership
```

The report should summarize:

- strongest model
- weakest task category
- release blockers
- recommendation
- next experiment

## Phase 7: Polish for recruiters

Add:

- screenshots
- architecture diagram
- demo GIF
- deployed link
- clear README
- resume bullet
- short project write-up explaining why this matters
