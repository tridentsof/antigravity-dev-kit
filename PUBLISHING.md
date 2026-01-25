# Publishing to npm

## Directory Structure for npm Package

Before publishing, reorganize the folder structure:

```
antigravity-devkit-vue-aspnet/
├── package.json          # npm package config
├── bin/
│   └── cli.js            # CLI tool
├── template/             # Kit files (copied to user's .agent/)
│   ├── README.md
│   ├── ARCHITECTURE.md
│   ├── rules/
│   ├── agents/
│   ├── skills/
│   ├── workflows/
│   └── scripts/
├── LICENSE
└── README.md             # npm README (can be same as template)
```

## Step-by-Step Publishing Guide

### 1. Prepare the Package

```bash
# Create a new folder for the npm package
mkdir antigravity-devkit-vue-aspnet
cd antigravity-devkit-vue-aspnet

# Copy package files
cp /path/to/.agent-antigravity/package.json .
cp /path/to/.agent-antigravity/LICENSE .
cp -r /path/to/.agent-antigravity/bin .

# Create template folder and copy kit contents
mkdir template
cp /path/to/.agent-antigravity/README.md template/
cp /path/to/.agent-antigravity/ARCHITECTURE.md template/
cp -r /path/to/.agent-antigravity/rules template/
cp -r /path/to/.agent-antigravity/agents template/
cp -r /path/to/.agent-antigravity/skills template/
cp -r /path/to/.agent-antigravity/workflows template/
cp -r /path/to/.agent-antigravity/scripts template/

# Copy README for npm page
cp template/README.md .
```

### 2. Update package.json

Edit `package.json`:
- Update `name` to your package name
- Update `author` with your info
- Update `repository` with your GitHub URL

### 3. Login to npm

```bash
npm login
# Enter your npm username, password, and email
```

### 4. Publish

```bash
# First time: just publish
npm publish

# Subsequent updates: bump version first
npm version patch  # or minor, or major
npm publish
```

### 5. Verify

```bash
# Test installation in a new project
mkdir test-project && cd test-project
npm init -y
npx antigravity-devkit-vue-aspnet init
```

---

## Quick Script for Reorganization

Save this as `prepare-npm.sh`:

```bash
#!/bin/bash

# Create npm package folder
PACKAGE_DIR="npm-package"
SOURCE_DIR="."

rm -rf $PACKAGE_DIR
mkdir -p $PACKAGE_DIR/template
mkdir -p $PACKAGE_DIR/bin

# Copy npm files
cp package.json $PACKAGE_DIR/
cp LICENSE $PACKAGE_DIR/
cp bin/cli.js $PACKAGE_DIR/bin/

# Copy template files
cp README.md $PACKAGE_DIR/template/
cp ARCHITECTURE.md $PACKAGE_DIR/template/
cp -r rules $PACKAGE_DIR/template/
cp -r agents $PACKAGE_DIR/template/
cp -r skills $PACKAGE_DIR/template/
cp -r workflows $PACKAGE_DIR/template/
cp -r scripts $PACKAGE_DIR/template/

# Copy README for npm page
cp README.md $PACKAGE_DIR/

echo "✅ Package prepared in $PACKAGE_DIR/"
echo "   cd $PACKAGE_DIR && npm publish"
```

---

## Alternative: GitHub Package

If you prefer GitHub Packages:

```bash
# Update package.json
{
  "name": "@yourusername/antigravity-devkit-vue-aspnet",
  "publishConfig": {
    "registry": "https://npm.pkg.github.com"
  }
}

# Login to GitHub Packages
npm login --registry=https://npm.pkg.github.com

# Publish
npm publish
```

---

## User Installation

Once published, users have two options:

### Option 1: One-time use with npx (No install)

```bash
cd my-project
npx antigravity-devkit-vue-aspnet init
```

Best for: Trying the kit, one-time setup, CI/CD scripts

### Option 2: Global install (Recommended for developers)

```bash
# Install once globally
npm install -g antigravity-devkit-vue-aspnet

# Then use in any project
cd my-project
antigravity-devkit init

cd another-project
antigravity-devkit init
```

Best for: Developers who use the kit frequently

### Available Commands

| Command | Description |
|---------|-------------|
| `antigravity-devkit init` | Install kit to `.agent/` |
| `antigravity-devkit init --force` | Overwrite existing `.agent/` |
| `antigravity-devkit update` | Update kit (backs up to `.agent-backup/`) |
| `antigravity-devkit help` | Show help |

### Updating Global Install

```bash
# Update to latest version
npm update -g antigravity-devkit-vue-aspnet

# Then update in each project
cd my-project
antigravity-devkit update
```

This will:
1. Backup existing `.agent/` to `.agent-backup/`
2. Install fresh copy of the kit
3. User can merge any custom skills from backup
