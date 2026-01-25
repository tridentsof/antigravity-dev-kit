#!/usr/bin/env python3
"""
Checklist - Priority-based project validation
Run during development and pre-commit.

Usage:
    python .agent-antigravity/scripts/checklist.py .
    python .agent-antigravity/scripts/checklist.py . --url http://localhost:3000
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(cmd: list[str], cwd: str = ".") -> tuple[int, str]:
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
        return 1, "Command timed out"
    except FileNotFoundError:
        return 1, f"Command not found: {cmd[0]}"


def check_frontend_lint(project_path: str) -> tuple[bool, str]:
    """Check frontend linting."""
    package_json = Path(project_path) / "package.json"
    if not package_json.exists():
        return True, "No package.json found, skipping frontend lint"
    
    code, output = run_command(["npm", "run", "lint"], project_path)
    return code == 0, output


def check_frontend_types(project_path: str) -> tuple[bool, str]:
    """Check TypeScript types."""
    package_json = Path(project_path) / "package.json"
    if not package_json.exists():
        return True, "No package.json found, skipping type check"
    
    code, output = run_command(["npm", "run", "type-check"], project_path)
    if code != 0:
        # Try alternative command
        code, output = run_command(["npx", "tsc", "--noEmit"], project_path)
    return code == 0, output


def check_backend_build(project_path: str) -> tuple[bool, str]:
    """Check .NET build."""
    sln_files = list(Path(project_path).glob("*.sln"))
    csproj_files = list(Path(project_path).glob("**/*.csproj"))
    
    if not sln_files and not csproj_files:
        return True, "No .NET project found, skipping build"
    
    code, output = run_command(["dotnet", "build"], project_path)
    return code == 0, output


def check_backend_tests(project_path: str) -> tuple[bool, str]:
    """Check .NET tests."""
    sln_files = list(Path(project_path).glob("*.sln"))
    if not sln_files:
        return True, "No .NET solution found, skipping tests"
    
    code, output = run_command(["dotnet", "test"], project_path)
    return code == 0, output


def check_frontend_tests(project_path: str) -> tuple[bool, str]:
    """Check frontend tests."""
    package_json = Path(project_path) / "package.json"
    if not package_json.exists():
        return True, "No package.json found, skipping tests"
    
    code, output = run_command(["npm", "run", "test", "--", "--run"], project_path)
    return code == 0, output


def check_security(project_path: str) -> tuple[bool, str]:
    """Check for security issues."""
    issues = []
    
    # Check for hardcoded secrets patterns
    secret_patterns = ["password=", "apikey=", "secret=", "connectionstring="]
    for pattern in secret_patterns:
        code, output = run_command(
            ["grep", "-ri", pattern, "--include=*.cs", "--include=*.ts", "--include=*.json"],
            project_path
        )
        if code == 0 and output.strip():
            issues.append(f"Potential secret found: {pattern}")
    
    # Check npm audit
    package_json = Path(project_path) / "package.json"
    if package_json.exists():
        code, output = run_command(["npm", "audit", "--audit-level=high"], project_path)
        if code != 0:
            issues.append("npm audit found high severity vulnerabilities")
    
    if issues:
        return False, "\n".join(issues)
    return True, "No security issues found"


def main():
    if len(sys.argv) < 2:
        print("Usage: python checklist.py <project_path> [--url <url>]")
        sys.exit(1)
    
    project_path = sys.argv[1]
    url = None
    if "--url" in sys.argv:
        url_index = sys.argv.index("--url") + 1
        if url_index < len(sys.argv):
            url = sys.argv[url_index]
    
    print("=" * 60)
    print("PROJECT CHECKLIST")
    print("=" * 60)
    
    checks = [
        ("Security", check_security),
        ("Frontend Lint", check_frontend_lint),
        ("Frontend Types", check_frontend_types),
        ("Frontend Tests", check_frontend_tests),
        ("Backend Build", check_backend_build),
        ("Backend Tests", check_backend_tests),
    ]
    
    results = []
    for name, check_fn in checks:
        print(f"\n[{name}]")
        passed, output = check_fn(project_path)
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status}")
        if not passed:
            print(f"  {output[:500]}")
        results.append((name, passed))
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    passed_count = sum(1 for _, p in results if p)
    total_count = len(results)
    
    for name, passed in results:
        status = "✅" if passed else "❌"
        print(f"  {status} {name}")
    
    print(f"\nResult: {passed_count}/{total_count} checks passed")
    
    if passed_count < total_count:
        sys.exit(1)
    
    print("\n✅ All checks passed!")


if __name__ == "__main__":
    main()
