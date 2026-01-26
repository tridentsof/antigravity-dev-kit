#!/usr/bin/env python3
"""
Security Scanner - Security vulnerability detection and analysis
Used by security-auditor agent to scan for security issues.

Usage:
    python security_scan.py <project_path>
    python security_scan.py <project_path> --severity high
"""

import subprocess
import sys
import re
import json
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


def scan_hardcoded_secrets(project_path: str) -> List[Dict[str, str]]:
    """Scan for hardcoded secrets and credentials."""
    findings = []
    path = Path(project_path)
    
    # Patterns to search for
    secret_patterns = {
        'password': r'password\s*=\s*["\'](?!.*\{.*\})([^"\']+)["\']',
        'api_key': r'(api[_-]?key|apikey)\s*[=:]\s*["\']([^"\']+)["\']',
        'secret': r'secret\s*[=:]\s*["\'](?!.*\{.*\})([^"\']+)["\']',
        'token': r'(access[_-]?token|auth[_-]?token)\s*[=:]\s*["\']([^"\']+)["\']',
        'connection_string': r'(connectionstring|connection[_-]string)\s*[=:]\s*["\'](?!.*\{.*\})([^"\']+)["\']',
        'private_key': r'(private[_-]?key|privatekey)\s*[=:]\s*["\']([^"\']+)["\']',
    }
    
    # File extensions to scan
    extensions = ['.cs', '.ts', '.js', '.vue', '.json', '.config', '.yaml', '.yml']
    
    for ext in extensions:
        for file_path in path.glob(f"**/*{ext}"):
            # Skip node_modules, bin, obj directories
            if any(skip in str(file_path) for skip in ['node_modules', 'bin', 'obj', '.git']):
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    for pattern_name, pattern in secret_patterns.items():
                        matches = re.finditer(pattern, content, re.IGNORECASE)
                        for match in matches:
                            # Skip if it looks like a placeholder or environment variable
                            matched_value = match.group(0)
                            if any(skip in matched_value.lower() for skip in ['example', 'placeholder', 'your_', 'xxx', '***', 'env.']):
                                continue
                            
                            findings.append({
                                'type': pattern_name,
                                'file': str(file_path.relative_to(path)),
                                'line': content[:match.start()].count('\n') + 1,
                                'severity': 'HIGH',
                                'message': f'Potential hardcoded {pattern_name.replace("_", " ")}'
                            })
            except Exception:
                continue
    
    return findings


def scan_npm_vulnerabilities(project_path: str) -> List[Dict[str, str]]:
    """Scan npm packages for known vulnerabilities."""
    findings = []
    package_json = Path(project_path) / "package.json"
    
    if not package_json.exists():
        return findings
    
    # Run npm audit
    code, output = run_command(["npm", "audit", "--json"], project_path)
    
    try:
        audit_data = json.loads(output)
        
        # Parse vulnerabilities
        if 'vulnerabilities' in audit_data:
            for pkg_name, vuln_info in audit_data['vulnerabilities'].items():
                severity = vuln_info.get('severity', 'unknown').upper()
                
                findings.append({
                    'type': 'npm_vulnerability',
                    'file': 'package.json',
                    'package': pkg_name,
                    'severity': severity,
                    'message': f"{pkg_name}: {vuln_info.get('via', ['Unknown issue'])[0] if isinstance(vuln_info.get('via'), list) else 'Vulnerability detected'}"
                })
    except json.JSONDecodeError:
        # Fallback to text parsing
        if 'vulnerabilities' in output.lower():
            findings.append({
                'type': 'npm_vulnerability',
                'file': 'package.json',
                'severity': 'UNKNOWN',
                'message': 'npm audit found vulnerabilities (run npm audit for details)'
            })
    
    return findings


def scan_dotnet_vulnerabilities(project_path: str) -> List[Dict[str, str]]:
    """Scan .NET packages for known vulnerabilities."""
    findings = []
    
    # Check if dotnet is available
    code, _ = run_command(["dotnet", "--version"])
    if code != 0:
        return findings
    
    # Run dotnet list package --vulnerable
    code, output = run_command(["dotnet", "list", "package", "--vulnerable"], project_path)
    
    if code == 0 and output:
        lines = output.split('\n')
        for line in lines:
            if 'vulnerable' in line.lower() or 'severity' in line.lower():
                findings.append({
                    'type': 'nuget_vulnerability',
                    'file': 'packages',
                    'severity': 'MEDIUM',
                    'message': line.strip()
                })
    
    return findings


def scan_insecure_patterns(project_path: str) -> List[Dict[str, str]]:
    """Scan for insecure coding patterns."""
    findings = []
    path = Path(project_path)
    
    insecure_patterns = {
        'sql_injection': {
            'pattern': r'(ExecuteRawSql|FromSqlRaw|ExecuteSqlCommand)\s*\([^)]*\+',
            'message': 'Potential SQL injection - avoid string concatenation in SQL queries',
            'severity': 'HIGH'
        },
        'xss': {
            'pattern': r'innerHTML\s*=\s*(?!["\']\s*["\'])',
            'message': 'Potential XSS vulnerability - avoid innerHTML with user input',
            'severity': 'HIGH'
        },
        'weak_crypto': {
            'pattern': r'(MD5|SHA1)\.Create\(',
            'message': 'Weak cryptographic algorithm - use SHA256 or stronger',
            'severity': 'MEDIUM'
        },
        'eval_usage': {
            'pattern': r'\beval\s*\(',
            'message': 'Dangerous eval() usage - avoid evaluating dynamic code',
            'severity': 'HIGH'
        },
        'http_not_https': {
            'pattern': r'http://(?!localhost|127\.0\.0\.1)',
            'message': 'HTTP URL detected - use HTTPS for external resources',
            'severity': 'MEDIUM'
        }
    }
    
    extensions = ['.cs', '.ts', '.js', '.vue']
    
    for ext in extensions:
        for file_path in path.glob(f"**/*{ext}"):
            if any(skip in str(file_path) for skip in ['node_modules', 'bin', 'obj', '.git']):
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    for pattern_name, pattern_info in insecure_patterns.items():
                        matches = re.finditer(pattern_info['pattern'], content, re.IGNORECASE)
                        for match in matches:
                            findings.append({
                                'type': pattern_name,
                                'file': str(file_path.relative_to(path)),
                                'line': content[:match.start()].count('\n') + 1,
                                'severity': pattern_info['severity'],
                                'message': pattern_info['message']
                            })
            except Exception:
                continue
    
    return findings


def check_security_headers(project_path: str) -> List[Dict[str, str]]:
    """Check for security header configurations."""
    findings = []
    path = Path(project_path)
    
    # Check for ASP.NET security configurations
    startup_files = list(path.glob("**/Startup.cs")) + list(path.glob("**/Program.cs"))
    
    for startup_file in startup_files:
        try:
            with open(startup_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Check for HSTS
                if 'UseHsts' not in content:
                    findings.append({
                        'type': 'missing_hsts',
                        'file': str(startup_file.relative_to(path)),
                        'severity': 'MEDIUM',
                        'message': 'HSTS not configured - add app.UseHsts()'
                    })
                
                # Check for HTTPS redirection
                if 'UseHttpsRedirection' not in content:
                    findings.append({
                        'type': 'missing_https_redirect',
                        'file': str(startup_file.relative_to(path)),
                        'severity': 'MEDIUM',
                        'message': 'HTTPS redirection not configured'
                    })
        except Exception:
            continue
    
    return findings


def format_report(all_findings: List[Dict[str, str]], severity_filter: str = None) -> Tuple[str, int]:
    """Format security scan report."""
    # Filter by severity if specified
    if severity_filter:
        all_findings = [f for f in all_findings if f['severity'] == severity_filter.upper()]
    
    # Group by severity
    by_severity = {'HIGH': [], 'MEDIUM': [], 'LOW': [], 'UNKNOWN': []}
    for finding in all_findings:
        severity = finding.get('severity', 'UNKNOWN')
        by_severity[severity].append(finding)
    
    report = []
    report.append("=" * 60)
    report.append("🔒 SECURITY SCAN REPORT")
    report.append("=" * 60)
    
    report.append("")
    report.append("📊 Summary:")
    report.append(f"  Total findings: {len(all_findings)}")
    report.append(f"  HIGH:    {len(by_severity['HIGH'])} 🔴")
    report.append(f"  MEDIUM:  {len(by_severity['MEDIUM'])} 🟡")
    report.append(f"  LOW:     {len(by_severity['LOW'])} 🟢")
    
    # Report HIGH severity issues
    if by_severity['HIGH']:
        report.append("")
        report.append("🔴 HIGH Severity Issues:")
        for finding in by_severity['HIGH'][:15]:
            report.append(f"  • {finding['file']}:{finding.get('line', '?')}")
            report.append(f"    {finding['message']}")
        if len(by_severity['HIGH']) > 15:
            report.append(f"  ... and {len(by_severity['HIGH']) - 15} more")
    
    # Report MEDIUM severity issues
    if by_severity['MEDIUM']:
        report.append("")
        report.append("🟡 MEDIUM Severity Issues:")
        for finding in by_severity['MEDIUM'][:10]:
            report.append(f"  • {finding['file']}:{finding.get('line', '?')}")
            report.append(f"    {finding['message']}")
        if len(by_severity['MEDIUM']) > 10:
            report.append(f"  ... and {len(by_severity['MEDIUM']) - 10} more")
    
    report.append("")
    report.append("=" * 60)
    
    # Determine exit code
    if by_severity['HIGH']:
        report.append("❌ Security scan failed - HIGH severity issues found")
        return "\n".join(report), 1
    elif by_severity['MEDIUM']:
        report.append("⚠️  Security scan completed with warnings")
        return "\n".join(report), 0
    else:
        report.append("✅ No security issues found")
        return "\n".join(report), 0


def main():
    if len(sys.argv) < 2:
        print("Usage: python security_scan.py <project_path> [--severity high|medium|low]")
        sys.exit(1)
    
    project_path = sys.argv[1]
    severity_filter = None
    
    if "--severity" in sys.argv:
        sev_index = sys.argv.index("--severity") + 1
        if sev_index < len(sys.argv):
            severity_filter = sys.argv[sev_index]
    
    print("🔒 Security Scanner")
    print("=" * 60)
    print(f"Project: {project_path}")
    if severity_filter:
        print(f"Severity filter: {severity_filter.upper()}")
    print()
    
    all_findings = []
    
    # Run scans
    print("Scanning for hardcoded secrets...")
    all_findings.extend(scan_hardcoded_secrets(project_path))
    
    print("Scanning npm vulnerabilities...")
    all_findings.extend(scan_npm_vulnerabilities(project_path))
    
    print("Scanning .NET vulnerabilities...")
    all_findings.extend(scan_dotnet_vulnerabilities(project_path))
    
    print("Scanning for insecure patterns...")
    all_findings.extend(scan_insecure_patterns(project_path))
    
    print("Checking security headers...")
    all_findings.extend(check_security_headers(project_path))
    
    print()
    print("-" * 60)
    
    # Generate and print report
    report, exit_code = format_report(all_findings, severity_filter)
    print(report)
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
