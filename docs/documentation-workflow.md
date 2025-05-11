# Documentation Workflow

This document describes the complete workflow for maintaining and publishing documentation for the Architecture CRUD Application.

## Overview

The documentation workflow consists of:

1. Writing documentation in AsciiDoc format
2. Building documentation locally with docToolchain
3. Committing and pushing changes
4. Automatic publishing via GitHub Actions
5. Live documentation on GitHub Pages

## Workflow Diagram

```
Developer → Write Docs → Build Locally → Git Push → GitHub Actions → GitHub Pages
   ↑                                                                      ↓
   └────────────── Review Published Documentation ────────────────────────┘
```

## Step-by-Step Workflow

### 1. Writing Documentation

- Use AsciiDoc format (`.adoc` files)
- Follow arc42 template structure
- Place files in appropriate directories:
  - `docs/arc42/` - Architecture documentation
  - `docs/specification/` - Specifications
  - `docs/` - Guides and progress reports

### 2. Local Build and Preview

```bash
# Quick preview with auto-refresh
./generate-docs.sh preview

# Or build manually
./dtcw generateMicrosite

# Preview at http://localhost:8080
```

### 3. Version Control

```bash
# Add documentation changes
git add docs/

# Commit with descriptive message
git commit -m "docs: update architecture decisions"

# Push to trigger deployment
git push origin main
```

### 4. Automatic Deployment

GitHub Actions automatically:
- Detects changes in `docs/` directory
- Runs docToolchain in Docker
- Generates microsite
- Deploys to GitHub Pages

### 5. Verification

Check the live documentation at:
`https://[username].github.io/architecture-crud-app/`

## File Structure

```
architecture-crud-app/
├── docs/
│   ├── arc42/                    # Architecture documentation
│   │   ├── 01_introduction_and_goals/
│   │   ├── 02_constraints/
│   │   └── ...
│   ├── specification/            # Project specifications
│   ├── index.adoc               # Documentation home page
│   └── custom.css               # Custom styling
├── docToolchainConfig.groovy    # docToolchain configuration
├── dtcw                         # docToolchain wrapper
└── .github/
    └── workflows/
        └── publish-docs.yml     # GitHub Actions workflow
```

## Best Practices

### Writing

1. **Consistent Formatting**
   - Use consistent heading levels
   - Follow AsciiDoc best practices
   - Include diagrams where helpful

2. **Modular Content**
   - Split large documents into sections
   - Use includes for reusable content
   - Keep files focused and concise

3. **Version Control**
   - Commit documentation with code changes
   - Use meaningful commit messages
   - Tag releases with documentation

### Building

1. **Always Preview Locally**
   - Test changes before pushing
   - Verify links and includes work
   - Check formatting and styling

2. **Clean Builds**
   - Use `./generate-docs.sh clean` when needed
   - Remove old artifacts before major changes

3. **Docker Usage**
   - Keep Docker updated
   - Use the provided wrapper scripts
   - Don't modify Docker images directly

### Publishing

1. **Branch Strategy**
   - Publish from `main` branch only
   - Use feature branches for major doc changes
   - Review before merging to main

2. **Monitoring**
   - Check GitHub Actions logs for errors
   - Verify deployment completes successfully
   - Test live site after deployment

## Troubleshooting

### Common Issues

1. **Build Failures**
   ```bash
   # Clean and rebuild
   ./generate-docs.sh clean
   ./generate-docs.sh all
   ```

2. **GitHub Actions Failures**
   - Check workflow logs in Actions tab
   - Verify file permissions
   - Ensure all includes exist

3. **Pages Not Updating**
   - Check GitHub Pages settings
   - Verify workflow completed
   - Clear browser cache

### Debug Commands

```bash
# Verbose docToolchain output
./dtcw generateHTML --info

# Check Docker
docker info
docker images | grep doctoolchain

# Test includes
grep -r "include::" docs/
```

## Maintenance

### Regular Tasks

1. **Weekly**
   - Review and update documentation
   - Fix broken links
   - Update progress reports

2. **Monthly**
   - Review documentation structure
   - Update diagrams
   - Check for outdated content

3. **Per Release**
   - Update version numbers
   - Document new features
   - Archive old documentation

### Updating docToolchain

To update docToolchain version:

1. Edit `DTC_VERSION` in `dtcw`
2. Update Docker image in workflows
3. Test thoroughly before committing

## Integration with Development

### Documentation-Driven Development

1. Update specs before implementation
2. Document architecture decisions
3. Keep documentation in sync with code

### Code and Docs Together

```bash
# Example workflow
git checkout -b feature/new-component

# Implement feature
# Update documentation
# Commit together
git add src/ docs/
git commit -m "feat: add new component with documentation"

# Create PR with code and docs
```

## Advanced Topics

### Custom Themes

1. Modify `custom.css` for styling
2. Update `docToolchain-microsite.yml` for structure
3. Add custom JavaScript if needed

### Automation

1. Pre-commit hooks for doc validation
2. Automated link checking
3. Documentation linting with Vale

### Monitoring

1. Google Analytics integration
2. Broken link detection
3. Documentation coverage metrics

## Resources

- [AsciiDoc User Guide](https://asciidoc.org/userguide.html)
- [docToolchain Documentation](https://doctoolchain.github.io/docToolchain/)
- [arc42 Template](https://arc42.org/)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)

This workflow ensures documentation stays current, accurate, and easily accessible to all stakeholders.
