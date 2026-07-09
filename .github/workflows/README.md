# CI/CD Pipeline Setup Guide

This document explains how to set up and use the GitHub Actions CI/CD pipeline for building and pushing Docker images to Docker Hub.

## Repository Structure

The repository contains the following services that will be built as Docker images:

- **api-gateway** - Main API gateway service (port 5000)
- **ml-prediction-service** - ML prediction service (port 5001)
- **model-training-service** - Model training service (port 5002)
- **data-service** - Data service (port 5003)
- **frontend** - Nginx-based frontend

## Docker Hub Image Naming Convention

Images will be pushed to Docker Hub with the following naming pattern:
- `docker.io/<DOCKER_HUB_USERNAME>/<repo-name>-api-gateway`
- `docker.io/<DOCKER_HUB_USERNAME>/<repo-name>-ml-prediction-service`
- `docker.io/<DOCKER_HUB_USERNAME>/<repo-name>-model-training-service`
- `docker.io/<DOCKER_HUB_USERNAME>/<repo-name>-data-service`
- `docker.io/<DOCKER_HUB_USERNAME>/<repo-name>-frontend`

## Required Secrets and Variables

Before the pipeline can push images to Docker Hub, you need to configure the following in your GitHub repository:

### 1. Repository Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions → New repository secret

Create these secrets:

| Secret Name | Description | Example Value |
|-------------|-------------|---------------|
| `DOCKER_HUB_USERNAME` | Your Docker Hub username | `myusername` |
| `DOCKER_HUB_TOKEN` | Docker Hub access token | `dckr_pat_xxxxxxxxxxxx` |

**How to create a Docker Hub Access Token:**
1. Log in to Docker Hub
2. Go to Account Settings → Security
3. Click "New Access Token"
4. Give it a name (e.g., "GitHub Actions")
5. Select permissions (at minimum: Read, Write, Delete)
6. Copy the token and save it securely

### 2. Repository Variables

Go to your GitHub repository → Settings → Secrets and variables → Actions → Variables → New repository variable

Create this variable:

| Variable Name | Description | Example Value |
|---------------|-------------|---------------|
| `DOCKER_HUB_USERNAME` | Your Docker Hub username (same as secret) | `myusername` |

## Pipeline Workflow

### Triggers

The pipeline runs on:
- Pushes to `main` or `master` branches
- Pull requests targeting `main` or `master` branches
- Version tags (e.g., `v1.0.0`, `v2.1.3`)

### Jobs

1. **build-and-push**: Builds and pushes all backend services in parallel
   - Runs on every push and pull request
   - On PRs: builds but doesn't push (for validation)
   - On branch pushes: builds and pushes with appropriate tags

2. **build-frontend**: Builds and pushes the frontend image
   - Only runs on pushes (not PRs)
   - Depends on successful completion of build-and-push

3. **update-helm-values**: Updates Helm chart values with new image tags
   - Only runs on main/master branch pushes and version tags
   - Automatically updates `helm-charts/ml-app/values.yaml`
   - Commits and pushes changes back to the repository

### Image Tags

The pipeline automatically generates the following tags:
- Branch name (e.g., `main`, `feature-xyz`)
- Pull request number (e.g., `pr-123`)
- Semantic version (for tags like `v1.0.0`)
- Short commit SHA (e.g., `sha-abc1234`)
- `latest` (only for pushes to main/master)

## Usage Examples

### Triggering a Build

Simply push to your main branch:
```bash
git push origin main
```

### Creating a Release

Create and push a version tag:
```bash
git tag v1.0.0
git push origin v1.0.0
```

This will:
- Build all images with tags `v1.0.0`, `v1.0`, `sha-xxxxx`, and `latest`
- Update the Helm chart values with the new version

## Monitoring Builds

View build progress and logs:
1. Go to your GitHub repository
2. Click on "Actions" tab
3. Select the workflow run
4. Click on individual jobs to see detailed logs

## Troubleshooting

### Build Fails with Authentication Error
- Verify `DOCKER_HUB_USERNAME` and `DOCKER_HUB_TOKEN` secrets are correctly set
- Ensure the Docker Hub token has proper permissions
- Check if the token has expired

### Images Not Appearing in Docker Hub
- Check if the workflow completed successfully
- Verify the Docker Hub username is correct
- For PRs, remember images are not pushed (only built)

### Helm Chart Update Fails
- Ensure the workflow has write permissions to the repository
- Check if there are conflicting changes to `values.yaml`

## Customization

### Adding New Services

To add a new service, edit `.github/workflows/ci-cd.yml` and add it to the matrix:

```yaml
strategy:
  matrix:
    service:
      # ... existing services ...
      - name: new-service
        context: ./backend/new-service
        dockerfile: ./backend/new-service/Dockerfile
        port: 5004
```

### Changing Build Platforms

To modify supported platforms, update the `platforms` parameter in the build step:
```yaml
platforms: linux/amd64,linux/arm64
```

### Disabling Multi-platform Builds

For faster builds during development, you can remove the `platforms` parameter to build only for the runner's architecture.

## Security Best Practices

1. **Never commit Docker Hub credentials** to the repository
2. Use Docker Hub access tokens instead of passwords
3. Regularly rotate access tokens
4. Limit token permissions to only what's necessary
5. Use branch protection rules for main/master branches

## Support

For issues or questions about this CI/CD pipeline, please open an issue in the repository.
