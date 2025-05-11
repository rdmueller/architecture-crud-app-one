# Architecture CRUD Application Documentation

This directory contains the documentation for the Architecture CRUD Application.

## Structure

- `arc42/` - Architecture documentation following the arc42 template
- `specification/` - Application specifications
- Various progress reports and guides

## Building the Documentation

The documentation is built using docToolchain and published as GitHub Pages.

### Prerequisites

- Docker (for running docToolchain)
- Git

### Local Build

To build the documentation locally:

```bash
# From the project root directory
./dtcw generateHTML
./dtcw generateMicrosite
```

The generated documentation will be in the `build/` directory.

### Automatic Publishing

The documentation is automatically published to GitHub Pages when:
- Changes are pushed to the `main` branch
- Changes affect files in the `docs/` directory
- Changes affect the docToolchain configuration

The published documentation will be available at:
`https://[your-username].github.io/[repository-name]/`

## docToolchain

This project uses [docToolchain](https://doctoolchain.github.io/docToolchain/) to generate documentation from AsciiDoc files.

The configuration is in `docToolchainConfig.groovy` in the project root.

## GitHub Pages Setup

To enable GitHub Pages for your repository:

1. Go to your repository settings
2. Navigate to "Pages" section
3. Under "Build and deployment", select "GitHub Actions" as the source
4. The documentation will be automatically published when you push changes

## Writing Documentation

- Use AsciiDoc format for all documentation files
- Follow the arc42 template structure
- Include diagrams using PlantUML or other supported formats
- Keep documentation up-to-date with code changes
