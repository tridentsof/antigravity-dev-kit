# Prepare npm package structure
# Run from .agent-antigravity folder: .\prepare-npm.ps1

$PACKAGE_DIR = "npm-package"
$SOURCE_DIR = "."

Write-Host "`n🚀 Preparing npm package...`n" -ForegroundColor Cyan

# Clean and create package folder
if (Test-Path $PACKAGE_DIR) {
    Remove-Item -Recurse -Force $PACKAGE_DIR
}

New-Item -ItemType Directory -Force -Path "$PACKAGE_DIR/template" | Out-Null
New-Item -ItemType Directory -Force -Path "$PACKAGE_DIR/bin" | Out-Null

# Copy npm files
Copy-Item "package.json" "$PACKAGE_DIR/"
Copy-Item "LICENSE" "$PACKAGE_DIR/"
Copy-Item "bin/cli.js" "$PACKAGE_DIR/bin/"

# Copy template files
Copy-Item "README.md" "$PACKAGE_DIR/template/"
Copy-Item "ARCHITECTURE.md" "$PACKAGE_DIR/template/"
Copy-Item -Recurse "rules" "$PACKAGE_DIR/template/"
Copy-Item -Recurse "agents" "$PACKAGE_DIR/template/"
Copy-Item -Recurse "skills" "$PACKAGE_DIR/template/"
Copy-Item -Recurse "workflows" "$PACKAGE_DIR/template/"
Copy-Item -Recurse "scripts" "$PACKAGE_DIR/template/"

# Copy README for npm page (root level)
Copy-Item "README.md" "$PACKAGE_DIR/"

Write-Host "✅ Package prepared in $PACKAGE_DIR/`n" -ForegroundColor Green

Write-Host "📦 Package structure:" -ForegroundColor Yellow
Write-Host "   $PACKAGE_DIR/"
Write-Host "   ├── package.json"
Write-Host "   ├── README.md"
Write-Host "   ├── LICENSE"
Write-Host "   ├── bin/"
Write-Host "   │   └── cli.js"
Write-Host "   └── template/"
Write-Host "       ├── README.md"
Write-Host "       ├── ARCHITECTURE.md"
Write-Host "       ├── rules/"
Write-Host "       ├── agents/"
Write-Host "       ├── skills/"
Write-Host "       ├── workflows/"
Write-Host "       └── scripts/`n"

Write-Host "📝 Next steps:" -ForegroundColor Yellow
Write-Host "   1. cd $PACKAGE_DIR"
Write-Host "   2. Update package.json with your info"
Write-Host "   3. npm login"
Write-Host "   4. npm publish`n"

Write-Host "🧪 To test locally:" -ForegroundColor Yellow
Write-Host "   cd $PACKAGE_DIR"
Write-Host "   npm link"
Write-Host "   cd ../test-project"
Write-Host "   npx antigravity-devkit init`n"
