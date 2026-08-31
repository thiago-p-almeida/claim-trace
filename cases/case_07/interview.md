**Interviewer:** Tell me more about the Kubernetes migration.

**Patrícia:** It was an 8-month project. The biggest challenge was ordering
the migration of services without downtime, because some had circular data
dependencies. I created a phased rollout plan with feature flags for rapid
rollback if anything went wrong.

**Interviewer:** And the CI/CD pipeline, how does it work today?

**Patrícia:** Every PR runs tests and a canary deploy to 5% of traffic
before releasing 100% — automated via GitHub Actions.