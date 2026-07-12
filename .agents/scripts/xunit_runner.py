#!/usr/bin/env python3
"""
xUnit Runner - Backend test execution and validation
Used by backend-specialist agent to run and validate ASP.NET/C# tests.

Usage:
    python xunit_runner.py <project_path>
    python xunit_runner.py <project_path> --coverage
    python xunit_runner.py <project_path> --filter "TestName"
"""

import subprocess
import sys
import re
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


def check_dotnet_installed() -> Tuple[bool, str]:
    """Check if .NET SDK is installed."""
    code, output = run_command(["dotnet", "--version"])
    if code == 0:
        version = output.strip()
        return True, f".NET SDK {version} installed"
    return False, "dotnet command not found"


def find_test_projects(project_path: str) -> list[Path]:
    """Find all test projects (*.Tests.csproj or *Tests.csproj)."""
    path = Path(project_path)
    test_projects = []
    
    # Common test project patterns
    patterns = ["*.Tests.csproj", "*Tests.csproj", "*.Test.csproj", "*Test.csproj"]
    
    for pattern in patterns:
        test_projects.extend(path.glob(f"**/{pattern}"))
    
    # Remove duplicates
    return list(set(test_projects))


def run_dotnet_test(project_path: str, coverage: bool = False, filter_expr: str = None) -> Tuple[int, str, Dict[str, Any]]:
    """Run dotnet test and return results."""
    cmd = ["dotnet", "test"]
    
    # Add verbosity
    cmd.extend(["--verbosity", "normal"])
    
    # Add filter if specified
    if filter_expr:
        cmd.extend(["--filter", filter_expr])
    
    # Add coverage if requested
    if coverage:
        cmd.extend(["--collect:XPlat Code Coverage"])
    
    code, output = run_command(cmd, project_path)
    
    # Parse test results
    results = parse_dotnet_test_output(output)
    
    return code, output, results


def parse_dotnet_test_output(output: str) -> Dict[str, Any]:
    """Parse dotnet test output to extract test statistics."""
    results = {
        'total': 0,
        'passed': 0,
        'failed': 0,
        'skipped': 0,
        'duration': None,
        'errors': []
    }
    
    lines = output.split('\n')
    
    for line in lines:
        # Parse test summary line
        # Example: "Passed!  - Failed:     0, Passed:    10, Skipped:     0, Total:    10"
        if 'Failed:' in line and 'Passed:' in line and 'Total:' in line:
            # Extract numbers using regex
            failed_match = re.search(r'Failed:\s*(\d+)', line)
            passed_match = re.search(r'Passed:\s*(\d+)', line)
            skipped_match = re.search(r'Skipped:\s*(\d+)', line)
            total_match = re.search(r'Total:\s*(\d+)', line)
            
            if failed_match:
                results['failed'] = int(failed_match.group(1))
            if passed_match:
                results['passed'] = int(passed_match.group(1))
            if skipped_match:
                results['skipped'] = int(skipped_match.group(1))
            if total_match:
                results['total'] = int(total_match.group(1))
        
        # Parse duration
        # Example: "Time: 00:00:01.23"
        if 'Time:' in line:
            time_match = re.search(r'Time:\s*([\d:\.]+)', line)
            if time_match:
                results['duration'] = time_match.group(1)
        
        # Collect error messages
        if 'Failed' in line and '[FAIL]' in line:
            results['errors'].append(line.strip())
        elif 'Error Message:' in line:
            results['errors'].append(line.strip())
    
    return results


def format_summary(code: int, results: Dict[str, Any], test_projects: list[Path]) -> str:
    """Format test results into a readable summary."""
    summary = []
    summary.append("=" * 60)
    summary.append("XUNIT TEST RESULTS")
    summary.append("=" * 60)
    
    if code == 0:
        summary.append("✅ All tests passed!")
    else:
        summary.append("❌ Some tests failed")
    
    summary.append("")
    summary.append(f"Test Projects Found: {len(test_projects)}")
    for proj in test_projects:
        summary.append(f"  • {proj.name}")
    
    summary.append("")
    summary.append("Statistics:")
    summary.append(f"  Total:   {results['total']}")
    summary.append(f"  Passed:  {results['passed']} ✅")
    summary.append(f"  Failed:  {results['failed']} ❌")
    summary.append(f"  Skipped: {results['skipped']} ⏭️")
    
    if results['duration']:
        summary.append(f"  Duration: {results['duration']}")
    
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
        print("Usage: python xunit_runner.py <project_path> [--coverage] [--filter <expression>]")
        sys.exit(1)
    
    project_path = sys.argv[1]
    coverage = "--coverage" in sys.argv
    filter_expr = None
    
    if "--filter" in sys.argv:
        filter_index = sys.argv.index("--filter") + 1
        if filter_index < len(sys.argv):
            filter_expr = sys.argv[filter_index]
    
    print("🧪 xUnit Test Runner")
    print("=" * 60)
    print(f"Project: {project_path}")
    print(f"Coverage: {coverage}")
    if filter_expr:
        print(f"Filter: {filter_expr}")
    print()
    
    # Check if .NET is installed
    installed, message = check_dotnet_installed()
    if not installed:
        print(f"❌ Error: {message}")
        print("\nPlease install .NET SDK from: https://dotnet.microsoft.com/download")
        sys.exit(1)
    
    print(f"✅ {message}")
    
    # Find test projects
    test_projects = find_test_projects(project_path)
    if not test_projects:
        print("⚠️  No test projects found")
        print("\nTest projects should match patterns:")
        print("  • *.Tests.csproj")
        print("  • *Tests.csproj")
        print("  • *.Test.csproj")
        sys.exit(1)
    
    print(f"✅ Found {len(test_projects)} test project(s)")
    print()
    
    # Run tests
    print("Running tests...")
    print("-" * 60)
    code, output, results = run_dotnet_test(project_path, coverage, filter_expr)
    
    # Print full output
    print(output)
    print()
    
    # Print summary
    summary = format_summary(code, results, test_projects)
    print(summary)
    
    # Exit with test result code
    sys.exit(code)


if __name__ == "__main__":
    main()
