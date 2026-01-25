#!/usr/bin/env python3
"""
Verify All - Comprehensive project verification
Run before deployment or releases.

Usage:
    python .agent-antigravity/scripts/verify_all.py .
    python .agent-antigravity/scripts/verify_all.py . --url http://localhost:3000
"""

import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime


def run_command(cmd: list[str], cwd: str = ".") -> tuple[int, str]:
    """Run a command and return exit code and output."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=600
        )
        return result.returncode, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return 1, "Command timed out"
    except FileNotFoundError:
        return 1, f"Command not found: {cmd[0]}"


class Verifier:
    def __init__(self, project_path: str, url: str = None):
        self.project_path = project_path
        self.url = url
        self.results = []
    
    def add_result(self, category: str, name: str, passed: bool, details: str = ""):
        self.results.append({
            "category": category,
            "name": name,
            "passed": passed,
            "details": details
        })
    
    def run_all(self):
        """Run all verification checks."""
        print("=" * 70)
        print("COMPREHENSIVE PROJECT VERIFICATION")
        print(f"Started: {datetime.now().isoformat()}")
        print("=" * 70)
        
        self.verify_security()
        self.verify_code_quality()
        self.verify_tests()
        self.verify_build()
        self.verify_dependencies()
        
        if self.url:
            self.verify_runtime(self.url)
        
        self.print_summary()
    
    def verify_security(self):
        """Security verification."""
        print("\n[SECURITY]")
        
        # Check for secrets
        secret_patterns = [
            ("password", "password="),
            ("api_key", "apikey="),
            ("secret", "secret="),
            ("connection_string", "connectionstring="),
        ]
        
        for name, pattern in secret_patterns:
            code, output = run_command(
                ["grep", "-ri", pattern, "--include=*.cs", "--include=*.ts"],
                self.project_path
            )
            passed = code != 0 or not output.strip()
            self.add_result("Security", f"No hardcoded {name}", passed)
            print(f"  {'✅' if passed else '❌'} No hardcoded {name}")
        
        # npm audit
        package_json = Path(self.project_path) / "package.json"
        if package_json.exists():
            code, output = run_command(["npm", "audit", "--audit-level=critical"], self.project_path)
            passed = code == 0
            self.add_result("Security", "npm audit (critical)", passed, output[:200])
            print(f"  {'✅' if passed else '❌'} npm audit (critical)")
    
    def verify_code_quality(self):
        """Code quality verification."""
        print("\n[CODE QUALITY]")
        
        # Frontend lint
        package_json = Path(self.project_path) / "package.json"
        if package_json.exists():
            code, output = run_command(["npm", "run", "lint"], self.project_path)
            passed = code == 0
            self.add_result("Code Quality", "Frontend lint", passed)
            print(f"  {'✅' if passed else '❌'} Frontend lint")
            
            # TypeScript
            code, output = run_command(["npx", "tsc", "--noEmit"], self.project_path)
            passed = code == 0
            self.add_result("Code Quality", "TypeScript check", passed)
            print(f"  {'✅' if passed else '❌'} TypeScript check")
        
        # Backend lint (if applicable)
        csproj_files = list(Path(self.project_path).glob("**/*.csproj"))
        if csproj_files:
            code, output = run_command(["dotnet", "format", "--verify-no-changes"], self.project_path)
            passed = code == 0
            self.add_result("Code Quality", "C# formatting", passed)
            print(f"  {'✅' if passed else '❌'} C# formatting")
    
    def verify_tests(self):
        """Test verification."""
        print("\n[TESTS]")
        
        # Frontend tests
        package_json = Path(self.project_path) / "package.json"
        if package_json.exists():
            code, output = run_command(["npm", "run", "test", "--", "--run"], self.project_path)
            passed = code == 0
            self.add_result("Tests", "Frontend tests", passed)
            print(f"  {'✅' if passed else '❌'} Frontend tests")
        
        # Backend tests
        sln_files = list(Path(self.project_path).glob("*.sln"))
        if sln_files:
            code, output = run_command(["dotnet", "test"], self.project_path)
            passed = code == 0
            self.add_result("Tests", "Backend tests", passed)
            print(f"  {'✅' if passed else '❌'} Backend tests")
    
    def verify_build(self):
        """Build verification."""
        print("\n[BUILD]")
        
        # Frontend build
        package_json = Path(self.project_path) / "package.json"
        if package_json.exists():
            code, output = run_command(["npm", "run", "build"], self.project_path)
            passed = code == 0
            self.add_result("Build", "Frontend build", passed)
            print(f"  {'✅' if passed else '❌'} Frontend build")
        
        # Backend build
        sln_files = list(Path(self.project_path).glob("*.sln"))
        if sln_files:
            code, output = run_command(["dotnet", "build", "-c", "Release"], self.project_path)
            passed = code == 0
            self.add_result("Build", "Backend build", passed)
            print(f"  {'✅' if passed else '❌'} Backend build")
    
    def verify_dependencies(self):
        """Dependency verification."""
        print("\n[DEPENDENCIES]")
        
        # npm outdated
        package_json = Path(self.project_path) / "package.json"
        if package_json.exists():
            code, output = run_command(["npm", "outdated"], self.project_path)
            # outdated returns 1 if there are outdated packages
            self.add_result("Dependencies", "npm packages", True, "Check npm outdated for details")
            print(f"  ℹ️  npm outdated check complete")
        
        # dotnet outdated (if tool installed)
        sln_files = list(Path(self.project_path).glob("*.sln"))
        if sln_files:
            code, output = run_command(["dotnet", "list", "package", "--outdated"], self.project_path)
            self.add_result("Dependencies", "NuGet packages", True, "Check dotnet list package for details")
            print(f"  ℹ️  NuGet outdated check complete")
    
    def verify_runtime(self, url: str):
        """Runtime verification (if URL provided)."""
        print("\n[RUNTIME]")
        
        # Health check
        code, output = run_command(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", f"{url}/health"])
        passed = output.strip() == "200"
        self.add_result("Runtime", "Health check", passed)
        print(f"  {'✅' if passed else '❌'} Health check")
    
    def print_summary(self):
        """Print verification summary."""
        print("\n" + "=" * 70)
        print("VERIFICATION SUMMARY")
        print("=" * 70)
        
        categories = {}
        for r in self.results:
            cat = r["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(r)
        
        total_passed = 0
        total_count = 0
        
        for cat, items in categories.items():
            print(f"\n{cat}:")
            for item in items:
                status = "✅" if item["passed"] else "❌"
                print(f"  {status} {item['name']}")
                total_count += 1
                if item["passed"]:
                    total_passed += 1
        
        print("\n" + "-" * 70)
        print(f"Total: {total_passed}/{total_count} checks passed")
        
        if total_passed < total_count:
            print("\n❌ Some checks failed. Review and fix before deployment.")
            sys.exit(1)
        else:
            print("\n✅ All checks passed! Ready for deployment.")


def main():
    if len(sys.argv) < 2:
        print("Usage: python verify_all.py <project_path> [--url <url>]")
        sys.exit(1)
    
    project_path = sys.argv[1]
    url = None
    if "--url" in sys.argv:
        url_index = sys.argv.index("--url") + 1
        if url_index < len(sys.argv):
            url = sys.argv[url_index]
    
    verifier = Verifier(project_path, url)
    verifier.run_all()


if __name__ == "__main__":
    main()
