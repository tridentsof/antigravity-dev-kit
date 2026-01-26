#!/usr/bin/env python3
"""
Vitest Runner - Frontend test execution and validation
Used by frontend-specialist agent to run and validate Vue3/TypeScript tests.

Usage:
    python vitest_runner.py <project_path>
    python vitest_runner.py <project_path> --coverage
    python vitest_runner.py <project_path> --watch
"""

import subprocess
import sys
import json
from pathlib import Path
from typing import Tuple, Dict, Any


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


def check_vitest_installed(project_path: str) -> Tuple[bool, str]:
    """Check if Vitest is installed in the project."""
    package_json = Path(project_path) / "package.json"
    
    if not package_json.exists():
        return False, "No package.json found in project"
    
    try:
        with open(package_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
            deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
            
            if 'vitest' not in deps:
                return False, "Vitest not found in dependencies"
            
            return True, f"Vitest {deps['vitest']} installed"
    except Exception as e:
        return False, f"Error reading package.json: {str(e)}"


def run_vitest(project_path: str, coverage: bool = False, watch: bool = False) -> Tuple[int, str, Dict[str, Any]]:
    """Run Vitest tests and return results."""
    cmd = ["npm", "run", "test", "--"]
    
    if watch:
        cmd.append("--watch")
    else:
        cmd.append("--run")
    
    if coverage:
        cmd.append("--coverage")
    
    # Add reporter for better parsing
    cmd.extend(["--reporter=verbose"])
    
    code, output = run_command(cmd, project_path)
    
    # Parse test results
    results = parse_vitest_output(output)
    
    return code, output, results


def parse_vitest_output(output: str) -> Dict[str, Any]:
    """Parse Vitest output to extract test statistics."""
    results = {
        'total': 0,
        'passed': 0,
        'failed': 0,
        'skipped': 0,
        'duration': 0,
        'coverage': None,
        'errors': []
    }
    
    lines = output.split('\n')
    
    for line in lines:
        # Parse test counts
        if 'Test Files' in line:
            # Example: "Test Files  2 passed (2)"
            parts = line.split()
            for i, part in enumerate(parts):
                if part == 'passed' and i > 0:
                    try:
                        results['passed'] = int(parts[i-1])
                    except ValueError:
                        pass
                if part == 'failed' and i > 0:
                    try:
                        results['failed'] = int(parts[i-1])
                    except ValueError:
                        pass
        
        # Parse duration
        if 'Duration' in line or 'Time' in line:
            # Try to extract duration
            pass
        
        # Collect error messages
        if 'FAIL' in line or 'Error' in line:
            results['errors'].append(line.strip())
    
    results['total'] = results['passed'] + results['failed'] + results['skipped']
    
    return results


def format_summary(code: int, results: Dict[str, Any], output: str) -> str:
    """Format test results into a readable summary."""
    summary = []
    summary.append("=" * 60)
    summary.append("VITEST TEST RESULTS")
    summary.append("=" * 60)
    
    if code == 0:
        summary.append("✅ All tests passed!")
    else:
        summary.append("❌ Some tests failed")
    
    summary.append("")
    summary.append("Statistics:")
    summary.append(f"  Total:   {results['total']}")
    summary.append(f"  Passed:  {results['passed']} ✅")
    summary.append(f"  Failed:  {results['failed']} ❌")
    summary.append(f"  Skipped: {results['skipped']} ⏭️")
    
    if results['errors']:
        summary.append("")
        summary.append("Errors/Failures:")
        for error in results['errors'][:10]:  # Limit to first 10 errors
            summary.append(f"  • {error}")
        
        if len(results['errors']) > 10:
            summary.append(f"  ... and {len(results['errors']) - 10} more")
    
    summary.append("")
    summary.append("=" * 60)
    
    return "\n".join(summary)


def main():
    if len(sys.argv) < 2:
        print("Usage: python vitest_runner.py <project_path> [--coverage] [--watch]")
        sys.exit(1)
    
    project_path = sys.argv[1]
    coverage = "--coverage" in sys.argv
    watch = "--watch" in sys.argv
    
    print("🧪 Vitest Test Runner")
    print("=" * 60)
    print(f"Project: {project_path}")
    print(f"Coverage: {coverage}")
    print(f"Watch mode: {watch}")
    print()
    
    # Check if Vitest is installed
    installed, message = check_vitest_installed(project_path)
    if not installed:
        print(f"❌ Error: {message}")
        print("\nTo install Vitest:")
        print("  npm install -D vitest @vue/test-utils")
        sys.exit(1)
    
    print(f"✅ {message}")
    print()
    
    # Run tests
    print("Running tests...")
    print("-" * 60)
    code, output, results = run_vitest(project_path, coverage, watch)
    
    # Print full output
    print(output)
    print()
    
    # Print summary
    summary = format_summary(code, results, output)
    print(summary)
    
    # Exit with test result code
    sys.exit(code)


if __name__ == "__main__":
    main()
