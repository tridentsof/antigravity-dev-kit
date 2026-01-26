#!/usr/bin/env python3
"""
Lint Runner - Code quality and style checker
Universal linting script for any agent to validate code quality.

Usage:
    python lint_runner.py <project_path>
    python lint_runner.py <project_path> --fix
    python lint_runner.py <project_path> --frontend-only
    python lint_runner.py <project_path> --backend-only
"""

import subprocess
import sys
from pathlib import Path
from typing import Tuple, Dict, Any, List


def run_command(cmd: list[str], cwd: str = ".") -> Tuple[int, str]:
    """Run a command and return exit code and output."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=300
        )
        return result.returncode, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return 1, "Command timed out after 5 minutes"
    except FileNotFoundError:
        return 1, f"Command not found: {cmd[0]}"


def detect_project_type(project_path: str) -> Dict[str, bool]:
    """Detect what types of projects exist."""
    path = Path(project_path)
    
    return {
        'frontend': (path / "package.json").exists(),
        'backend': len(list(path.glob("**/*.csproj"))) > 0 or len(list(path.glob("*.sln"))) > 0,
        'has_eslint': (path / ".eslintrc.js").exists() or (path / ".eslintrc.json").exists() or (path / "eslint.config.js").exists(),
        'has_prettier': (path / ".prettierrc").exists() or (path / ".prettierrc.json").exists(),
    }


def lint_frontend(project_path: str, fix: bool = False) -> Tuple[int, str, Dict[str, Any]]:
    """Run frontend linting (ESLint, Prettier, TypeScript)."""
    results = {
        'eslint': {'code': None, 'output': ''},
        'prettier': {'code': None, 'output': ''},
        'typescript': {'code': None, 'output': ''},
    }
    
    package_json = Path(project_path) / "package.json"
    if not package_json.exists():
        return 1, "No package.json found", results
    
    # ESLint
    print("  Running ESLint...")
    eslint_cmd = ["npm", "run", "lint"]
    if fix:
        eslint_cmd.append("--")
        eslint_cmd.append("--fix")
    
    code, output = run_command(eslint_cmd, project_path)
    results['eslint'] = {'code': code, 'output': output}
    
    # TypeScript type checking
    print("  Running TypeScript type check...")
    ts_cmd = ["npm", "run", "type-check"]
    code, output = run_command(ts_cmd, project_path)
    
    # If type-check script doesn't exist, try tsc directly
    if "Missing script" in output or code == 1:
        code, output = run_command(["npx", "tsc", "--noEmit"], project_path)
    
    results['typescript'] = {'code': code, 'output': output}
    
    # Prettier (if configured)
    prettier_config = Path(project_path) / ".prettierrc"
    if prettier_config.exists() or (Path(project_path) / ".prettierrc.json").exists():
        print("  Running Prettier...")
        prettier_cmd = ["npx", "prettier", "--check", "."]
        if fix:
            prettier_cmd = ["npx", "prettier", "--write", "."]
        
        code, output = run_command(prettier_cmd, project_path)
        results['prettier'] = {'code': code, 'output': output}
    
    # Determine overall status
    overall_code = 0
    for tool, result in results.items():
        if result['code'] is not None and result['code'] != 0:
            overall_code = 1
    
    return overall_code, "Frontend linting completed", results


def lint_backend(project_path: str, fix: bool = False) -> Tuple[int, str, Dict[str, Any]]:
    """Run backend linting (dotnet format)."""
    results = {
        'dotnet_format': {'code': None, 'output': ''},
        'dotnet_build': {'code': None, 'output': ''},
    }
    
    # Check if .NET project exists
    sln_files = list(Path(project_path).glob("*.sln"))
    csproj_files = list(Path(project_path).glob("**/*.csproj"))
    
    if not sln_files and not csproj_files:
        return 1, "No .NET project found", results
    
    # dotnet format
    print("  Running dotnet format...")
    format_cmd = ["dotnet", "format"]
    if not fix:
        format_cmd.append("--verify-no-changes")
    
    code, output = run_command(format_cmd, project_path)
    results['dotnet_format'] = {'code': code, 'output': output}
    
    # dotnet build (for additional warnings)
    print("  Running dotnet build...")
    build_cmd = ["dotnet", "build", "/warnaserror"]
    code, output = run_command(build_cmd, project_path)
    results['dotnet_build'] = {'code': code, 'output': output}
    
    # Determine overall status
    overall_code = 0
    for tool, result in results.items():
        if result['code'] is not None and result['code'] != 0:
            overall_code = 1
    
    return overall_code, "Backend linting completed", results


def format_report(project_types: Dict[str, bool], frontend_results: Dict[str, Any], backend_results: Dict[str, Any]) -> str:
    """Format linting report."""
    report = []
    report.append("=" * 60)
    report.append("🔍 CODE QUALITY REPORT")
    report.append("=" * 60)
    
    report.append("")
    report.append("📊 Project Type:")
    if project_types['frontend']:
        report.append("  ✅ Frontend (Node.js/TypeScript)")
    if project_types['backend']:
        report.append("  ✅ Backend (.NET/C#)")
    
    # Frontend results
    if frontend_results:
        report.append("")
        report.append("🎨 Frontend Linting:")
        
        for tool, result in frontend_results.items():
            if result['code'] is None:
                continue
            
            status = "✅ PASS" if result['code'] == 0 else "❌ FAIL"
            report.append(f"  {tool.upper()}: {status}")
            
            if result['code'] != 0:
                # Show first few lines of error
                error_lines = result['output'].split('\n')[:10]
                for line in error_lines:
                    if line.strip():
                        report.append(f"    {line}")
    
    # Backend results
    if backend_results:
        report.append("")
        report.append("⚙️  Backend Linting:")
        
        for tool, result in backend_results.items():
            if result['code'] is None:
                continue
            
            status = "✅ PASS" if result['code'] == 0 else "❌ FAIL"
            tool_name = tool.replace('_', ' ').title()
            report.append(f"  {tool_name}: {status}")
            
            if result['code'] != 0:
                # Show first few lines of error
                error_lines = result['output'].split('\n')[:10]
                for line in error_lines:
                    if line.strip():
                        report.append(f"    {line}")
    
    report.append("")
    report.append("=" * 60)
    
    return "\n".join(report)


def main():
    if len(sys.argv) < 2:
        print("Usage: python lint_runner.py <project_path> [--fix] [--frontend-only] [--backend-only]")
        sys.exit(1)
    
    project_path = sys.argv[1]
    fix = "--fix" in sys.argv
    frontend_only = "--frontend-only" in sys.argv
    backend_only = "--backend-only" in sys.argv
    
    print("🔍 Lint Runner")
    print("=" * 60)
    print(f"Project: {project_path}")
    print(f"Auto-fix: {fix}")
    print()
    
    # Detect project types
    project_types = detect_project_type(project_path)
    
    frontend_results = {}
    backend_results = {}
    overall_code = 0
    
    # Run frontend linting
    if project_types['frontend'] and not backend_only:
        print("Running frontend linting...")
        code, message, frontend_results = lint_frontend(project_path, fix)
        if code != 0:
            overall_code = 1
        print()
    
    # Run backend linting
    if project_types['backend'] and not frontend_only:
        print("Running backend linting...")
        code, message, backend_results = lint_backend(project_path, fix)
        if code != 0:
            overall_code = 1
        print()
    
    # Generate report
    report = format_report(project_types, frontend_results, backend_results)
    print(report)
    
    # Final status
    if overall_code == 0:
        print("✅ All linting checks passed!")
    else:
        print("❌ Linting issues found")
        if not fix:
            print("\nRun with --fix to automatically fix issues")
    
    sys.exit(overall_code)


if __name__ == "__main__":
    main()
