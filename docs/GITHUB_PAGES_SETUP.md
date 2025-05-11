# GitHub Pages Setup Instructions

To enable GitHub Pages for your Architecture CRUD Application documentation:

## 1. Repository Settings

1. Go to your repository on GitHub
2. Click on "Settings" tab
3. Scroll down to "Pages" section in the left sidebar

## 2. Configure GitHub Pages

1. Under "Build and deployment":
   - Source: Select "GitHub Actions"
   
2. Save the changes

## 3. First Deployment

The documentation will be automatically deployed when you:
- Push changes to the `main` branch that affect the `docs/` directory
- Manually trigger the workflow from the Actions tab

To manually trigger the deployment:
1. Go to the "Actions" tab in your repository
2. Select "Publish Documentation" workflow
3. Click "Run workflow"
4. Select the branch (usually `main`)
5. Click "Run workflow"

## 4. Accessing Your Documentation

After the workflow completes successfully, your documentation will be available at:

```
https://[your-github-username].github.io/[repository-name]/
```

For example:
- If your username is `johndoe` 
- And your repository is `architecture-crud-app`
- The URL would be: `https://johndoe.github.io/architecture-crud-app/`

## 5. Troubleshooting

### Workflow Fails

If the workflow fails:
1. Check the Actions tab for error messages
2. Common issues:
   - Missing docToolchain configuration
   - Incorrect file paths
   - Permission issues

### Pages Not Showing

If the pages don't appear:
1. Wait a few minutes (initial deployment can take time)
2. Check if GitHub Pages is enabled in repository settings
3. Verify the workflow completed successfully
4. Clear your browser cache

### Custom Domain (Optional)

To use a custom domain:
1. In the Pages settings, add your custom domain
2. Configure your DNS provider to point to GitHub Pages
3. Wait for DNS propagation (can take up to 24 hours)

## Local Testing

Before pushing changes, you can test the documentation build locally:

```bash
# From the project root
./dtcw generateMicrosite
```

Then open `build/microsite/index.html` in your browser.

## Automatic Builds

The documentation is automatically rebuilt and published when:
- You push changes to files in the `docs/` directory
- You modify the `docToolchainConfig.groovy` file
- You update the workflow file itself

This ensures your documentation is always up-to-date with your latest changes.
