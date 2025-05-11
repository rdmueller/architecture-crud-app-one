# Building Documentation Locally

This guide explains how to build and preview the documentation locally before pushing to GitHub.

## Prerequisites

- Docker installed and running
- Git repository cloned locally

## Quick Start

Use the convenient script:

```bash
# Generate microsite and preview it
./generate-docs.sh preview
```

This will:
1. Generate the microsite
2. Start a preview server on http://localhost:8080

## Manual Build Options

### 1. Using the Wrapper Script

```bash
# Generate HTML documentation
./dtcw generateHTML

# Generate microsite for GitHub Pages
./dtcw generateMicrosite
```

### 2. Using Docker Compose

```bash
# Build and preview the documentation
docker-compose -f docToolchain-docker-compose.yml up preview

# Live reload mode (for development)
docker-compose -f docToolchain-docker-compose.yml --profile dev up
```

### 3. Using the generate-docs.sh Script

```bash
# Generate HTML only
./generate-docs.sh html

# Generate microsite only
./generate-docs.sh microsite

# Generate both HTML and microsite
./generate-docs.sh all

# Clean build directory
./generate-docs.sh clean

# Start preview server
./generate-docs.sh preview

# Start live reload mode
./generate-docs.sh live
```

## Output Locations

- **HTML Documentation**: `build/`
- **Microsite**: `build/microsite/`

## Preview Options

### Option 1: Docker Compose (Recommended)

```bash
./generate-docs.sh preview
```

Opens at: http://localhost:8080

### Option 2: Python HTTP Server

```bash
cd build/microsite
python -m http.server 8000
```

Opens at: http://localhost:8000

### Option 3: Direct File Access

Open `build/microsite/index.html` directly in your browser.

## Development Workflow

1. Make changes to documentation files
2. Run `./generate-docs.sh preview` to see changes
3. Or use `./generate-docs.sh live` for automatic rebuilds
4. Commit and push when satisfied

## Troubleshooting

### Docker Issues

If you get Docker permission errors:

```bash
# Fix file permissions
sudo chown -R $USER:$USER .

# Or run with sudo (not recommended)
sudo ./dtcw generateMicrosite
```

### Build Errors

If the build fails:

1. Check Docker is running: `docker info`
2. Clean build directory: `./generate-docs.sh clean`
3. Check for syntax errors in AsciiDoc files
4. Ensure all included files exist

### Preview Server Issues

If the preview server doesn't start:

1. Check if port 8080 is already in use
2. Stop other services using the port
3. Or modify the port in `docToolchain-docker-compose.yml`

## Tips

- Use live reload mode during active documentation development
- Always preview locally before pushing to GitHub
- Check the generated site structure matches expectations
- Validate links work correctly in the preview

## Next Steps

After building and previewing locally:

1. Commit your changes
2. Push to GitHub
3. GitHub Actions will automatically publish to GitHub Pages
4. Check the live site at your GitHub Pages URL
