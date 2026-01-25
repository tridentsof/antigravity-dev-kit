#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const TEMPLATE_DIR = path.join(__dirname, '..', 'template');
const TARGET_DIR = path.join(process.cwd(), '.agent');

const commands = {
  init: initKit,
  update: updateKit,
  help: showHelp
};

function main() {
  const args = process.argv.slice(2);
  const command = args[0] || 'help';
  
  if (commands[command]) {
    commands[command](args.slice(1));
  } else {
    console.error(`Unknown command: ${command}`);
    showHelp();
    process.exit(1);
  }
}

function initKit(args) {
  console.log('\n🚀 Antigravity DevKit - Vue3 + ASP.NET + Azure\n');
  
  const force = args.includes('--force') || args.includes('-f');
  
  if (fs.existsSync(TARGET_DIR) && !force) {
    console.error('❌ .agent folder already exists!');
    console.log('   Use --force to overwrite: npx antigravity-devkit init --force\n');
    process.exit(1);
  }
  
  console.log('📁 Copying DevKit to .agent/...\n');
  
  try {
    copyDirectory(TEMPLATE_DIR, TARGET_DIR);
    
    console.log('✅ DevKit installed successfully!\n');
    console.log('📂 Created: .agent/');
    console.log('   ├── README.md');
    console.log('   ├── ARCHITECTURE.md');
    console.log('   ├── rules/GEMINI.md');
    console.log('   ├── agents/ (12 specialists)');
    console.log('   ├── skills/ (20 modules)');
    console.log('   ├── workflows/ (10 commands)');
    console.log('   └── scripts/ (validation tools)\n');
    
    console.log('🎯 Quick Start:');
    console.log('   /plan my new feature');
    console.log('   /code create a component');
    console.log('   /test generate tests\n');
    
    console.log('📖 See .agent/README.md for full documentation\n');
    
  } catch (error) {
    console.error('❌ Error installing DevKit:', error.message);
    process.exit(1);
  }
}

function updateKit(args) {
  console.log('\n🔄 Updating Antigravity DevKit...\n');
  
  if (!fs.existsSync(TARGET_DIR)) {
    console.error('❌ .agent folder not found!');
    console.log('   Run "npx antigravity-devkit init" first\n');
    process.exit(1);
  }
  
  // Backup existing customizations
  const customSkills = path.join(TARGET_DIR, 'skills');
  const backupDir = path.join(process.cwd(), '.agent-backup');
  
  console.log('📦 Backing up existing .agent to .agent-backup...');
  
  try {
    if (fs.existsSync(backupDir)) {
      fs.rmSync(backupDir, { recursive: true });
    }
    copyDirectory(TARGET_DIR, backupDir);
    
    // Remove and reinstall
    fs.rmSync(TARGET_DIR, { recursive: true });
    copyDirectory(TEMPLATE_DIR, TARGET_DIR);
    
    console.log('✅ DevKit updated successfully!');
    console.log('📂 Backup saved to .agent-backup/\n');
    console.log('⚠️  If you had custom skills, merge them from .agent-backup/\n');
    
  } catch (error) {
    console.error('❌ Error updating DevKit:', error.message);
    process.exit(1);
  }
}

function showHelp() {
  console.log(`
🚀 Antigravity DevKit CLI
   Vue3 + ASP.NET + Azure Development Toolkit

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

INSTALLATION OPTIONS:

  Option 1: One-time use (npx)
  $ npx antigravity-devkit init

  Option 2: Global install (recommended for frequent use)
  $ npm install -g antigravity-devkit
  $ antigravity-devkit init

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

COMMANDS:

  init              Install DevKit to .agent/ folder
  init --force      Overwrite existing .agent/ folder
  update            Update DevKit (backs up existing to .agent-backup/)
  help              Show this help message

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EXAMPLES:

  # First time setup in a project
  cd my-project
  antigravity-devkit init

  # Reinstall/reset the kit
  antigravity-devkit init --force

  # Update to latest version
  npm update -g antigravity-devkit
  antigravity-devkit update

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AFTER INSTALLATION:

  The kit will be installed to .agent/ folder.
  Start using slash commands in your AI assistant:

  /plan my new feature
  /code create a component
  /test generate tests
  /deploy to production

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Documentation: https://github.com/yourusername/antigravity-devkit
`);
}

function copyDirectory(src, dest) {
  if (!fs.existsSync(dest)) {
    fs.mkdirSync(dest, { recursive: true });
  }
  
  const entries = fs.readdirSync(src, { withFileTypes: true });
  
  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    
    if (entry.isDirectory()) {
      copyDirectory(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

main();
