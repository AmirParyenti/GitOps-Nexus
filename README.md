# GitOps Nexus Project

- Developed a Python based application with PostgreSQL database integration, enabling seamless data storage and retrieval for efficient information management.

- Configured a CI pipeline in Jenkins using Multibranch Pipeline to manage separate testing and production environments. Triggered by GitLab, the pipeline handles testing, creating a Merge Request, pushing a new image with a unique tag, updating the Helm chart, and deploying to production.

- Deployed the infrastructure using ArgoCD, that detects changes in the Helm chart within GitLab and updates running pods with new ones using the newly created image.

- Enhanced security by using Kubernetes Secrets for secure and encrypted database access from the application.

- Integrated monitoring with Prometheus & Grafana, set up custom metrics, alerts and dashboards.

