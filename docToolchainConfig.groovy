// Configuration file for docToolchain
// See https://doctoolchain.github.io/docToolchain/2.0.x/020_tutorial/

inputPath = './docs'
outputPath = './build'
mainConfigFile = 'docToolchainConfig.groovy'

// configure Asciidoctor
asciidoctor {
    attributes = [
            'project-version': 'DEV',
            'revnumber': 'DEV',
            'revdate': new Date().format('yyyy-MM-dd'),
            'author': 'Architecture CRUD App Team',
            'email': 'team@example.com',
            'source-highlighter': 'highlightjs',
            'toc': 'left',
            'toclevels': '3',
            'numbered': true,
            'icons': 'font',
            'imagesdir': './images',
            'plantuml-config': './plantuml.cfg',
            'sectlinks': true,
            'sectanchors': true,
            'stylesheet': 'custom.css',
            'linkcss': true,
            // add more attributes here
    ]
    
    // Configure diagram generation
    javaOpts '-Dfile.encoding=UTF-8'
    requires 'asciidoctor-diagram'
    gemPath = '.asciidoctor/gems'
    backends = ['html5']
    
    sources {
        include 'index.adoc'
        include 'arc42/architecture-documentation-complete.adoc'
        include 'specification/crud-app-specification.adoc'
        include '*.md'
        include '**/*.adoc'
    }
}

// Microsite configuration
microsite {
    targetPath = 'build/microsite'
    siteTitle = 'Architecture CRUD Application'
    siteDescription = 'Documentation for the Architecture CRUD Application'
    
    // Which documents to include in the microsite
    documents = [
        ['Home', 'index.adoc'],
        ['Architecture Documentation', 'arc42/architecture-documentation-complete.adoc'],
        ['Specification', 'specification/crud-app-specification.adoc'],
        ['Installation Guide', 'INSTALLATION.md'],
        ['UI Testing Guide', 'UI_TESTING.md'],
        ['Troubleshooting', 'TROUBLESHOOTING.md'],
        ['Phase 3 Progress', 'phase3-progress.md'],
        ['Phase 4 Progress', 'phase4-progress.md'],
        ['Phase 5 Progress', 'phase5-progress.md'],
        ['Phase 6 Progress', 'phase6-progress.md'],
        ['Documentation Workflow', 'documentation-workflow.md'],
        ['Build Local Docs', 'build-local-docs.md'],
        ['GitHub Pages Setup', 'GITHUB_PAGES_SETUP.md']
    ]
    
    // Theme configuration
    theme = 'default'
    customCSS = 'custom.css'
}

// PDF generation settings
pdf {
    theme = 'default'
    
    // Configure PDF attributes
    attributes = [
        'pdf-themesdir': 'themes',
        'pdf-theme': 'default',
        'pdf-fontsdir': 'fonts',
    ]
}

// Configure PlantUML
plantUML {
    // Local PlantUML configuration
    config = file('./plantuml.cfg')
    
    // Diagram formats
    formats = ['svg', 'png']
}

// Configure includes
includes {
    // Enable includes from subdirectories
    enableSubdirs = true
    
    // Include patterns
    patterns = [
        '**/*.adoc',
        '**/*.md'
    ]
}

// Export settings
export {
    // Enable export to different formats
    formats = ['html', 'pdf']
    
    // Export directory
    targetDir = 'build/export'
}
