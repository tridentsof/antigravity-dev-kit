#!/usr/bin/env python3
"""
Schema Validator - Database schema validation and analysis
Used by database-architect agent to validate SQL Server schemas.

Usage:
    python schema_validator.py <project_path>
    python schema_validator.py <project_path> --connection-string "Server=..."
"""

import subprocess
import sys
import re
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


def find_sql_files(project_path: str) -> Dict[str, List[Path]]:
    """Find SQL migration and schema files."""
    path = Path(project_path)
    
    sql_files = {
        'migrations': [],
        'schemas': [],
        'stored_procedures': [],
        'other': []
    }
    
    for sql_file in path.glob("**/*.sql"):
        file_lower = sql_file.name.lower()
        
        if 'migration' in file_lower or 'migrations' in str(sql_file.parent).lower():
            sql_files['migrations'].append(sql_file)
        elif 'schema' in file_lower:
            sql_files['schemas'].append(sql_file)
        elif 'proc' in file_lower or 'procedure' in file_lower or 'sp_' in file_lower:
            sql_files['stored_procedures'].append(sql_file)
        else:
            sql_files['other'].append(sql_file)
    
    return sql_files


def validate_sql_syntax(sql_file: Path) -> Tuple[bool, List[str]]:
    """Validate SQL file for common syntax issues."""
    issues = []
    
    try:
        with open(sql_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Check for common issues
            
            # 1. Missing GO statements in migrations
            if 'migration' in sql_file.name.lower():
                if 'CREATE TABLE' in content.upper() and 'GO' not in content.upper():
                    issues.append("Missing GO statement after CREATE TABLE")
            
            # 2. Missing primary keys
            if 'CREATE TABLE' in content.upper():
                # Simple check - look for PRIMARY KEY keyword
                if 'PRIMARY KEY' not in content.upper() and 'CONSTRAINT' not in content.upper():
                    issues.append("Table creation without explicit PRIMARY KEY")
            
            # 3. Missing indexes on foreign keys
            if 'FOREIGN KEY' in content.upper():
                # This is a suggestion, not an error
                if 'CREATE INDEX' not in content.upper() and 'CREATE NONCLUSTERED INDEX' not in content.upper():
                    issues.append("Consider adding indexes on foreign key columns")
            
            # 4. Using SELECT * (bad practice)
            if re.search(r'SELECT\s+\*\s+FROM', content, re.IGNORECASE):
                issues.append("Avoid using SELECT * - specify columns explicitly")
            
            # 5. Missing NULL constraints
            if 'CREATE TABLE' in content.upper():
                # Check if columns have NULL/NOT NULL specified
                lines = content.split('\n')
                for line in lines:
                    if re.search(r'\w+\s+(VARCHAR|INT|DATETIME|DECIMAL|BIT)', line, re.IGNORECASE):
                        if 'NULL' not in line.upper():
                            issues.append(f"Column definition missing NULL constraint: {line.strip()[:50]}")
                            break  # Only report once
            
            # 6. SQL Injection risks in dynamic SQL
            if 'EXEC' in content.upper() or 'EXECUTE' in content.upper():
                if '@' in content and '+' in content:
                    issues.append("Potential SQL injection risk - review dynamic SQL construction")
            
            # 7. Missing transaction handling
            if 'INSERT' in content.upper() or 'UPDATE' in content.upper() or 'DELETE' in content.upper():
                if 'BEGIN TRANSACTION' not in content.upper() and 'BEGIN TRAN' not in content.upper():
                    if 'migration' in sql_file.name.lower():
                        issues.append("Consider wrapping migrations in transactions")
    
    except Exception as e:
        issues.append(f"Error reading file: {str(e)}")
        return False, issues
    
    return len(issues) == 0, issues


def check_naming_conventions(sql_files: Dict[str, List[Path]]) -> List[str]:
    """Check SQL file naming conventions."""
    issues = []
    
    # Check migration naming
    for migration in sql_files['migrations']:
        # Migrations should have timestamp or version number
        if not re.search(r'\d{8,}', migration.name):  # At least 8 digits (YYYYMMDD)
            issues.append(f"Migration file should include timestamp: {migration.name}")
    
    # Check stored procedure naming
    for sp in sql_files['stored_procedures']:
        # Should start with sp_ or usp_
        if not re.match(r'(sp_|usp_)', sp.name, re.IGNORECASE):
            issues.append(f"Stored procedure should start with sp_ or usp_: {sp.name}")
    
    return issues


def analyze_schema_quality(sql_files: Dict[str, List[Path]]) -> Dict[str, Any]:
    """Analyze overall schema quality."""
    analysis = {
        'total_files': sum(len(files) for files in sql_files.values()),
        'migrations_count': len(sql_files['migrations']),
        'schemas_count': len(sql_files['schemas']),
        'stored_procedures_count': len(sql_files['stored_procedures']),
        'syntax_issues': [],
        'naming_issues': [],
        'recommendations': []
    }
    
    # Validate each SQL file
    for category, files in sql_files.items():
        for sql_file in files:
            is_valid, issues = validate_sql_syntax(sql_file)
            if not is_valid:
                for issue in issues:
                    analysis['syntax_issues'].append(f"{sql_file.name}: {issue}")
    
    # Check naming conventions
    analysis['naming_issues'] = check_naming_conventions(sql_files)
    
    # Generate recommendations
    if analysis['migrations_count'] == 0:
        analysis['recommendations'].append("No migration files found - consider using migration-based schema management")
    
    if analysis['stored_procedures_count'] > 0:
        analysis['recommendations'].append("Review stored procedures for performance and maintainability")
    
    return analysis


def format_report(sql_files: Dict[str, List[Path]], analysis: Dict[str, Any]) -> Tuple[str, int]:
    """Format validation report."""
    report = []
    report.append("=" * 60)
    report.append("SQL SCHEMA VALIDATION REPORT")
    report.append("=" * 60)
    
    report.append("")
    report.append("📊 File Summary:")
    report.append(f"  Total SQL files: {analysis['total_files']}")
    report.append(f"  Migrations:      {analysis['migrations_count']}")
    report.append(f"  Schemas:         {analysis['schemas_count']}")
    report.append(f"  Stored Procs:    {analysis['stored_procedures_count']}")
    report.append(f"  Other:           {len(sql_files['other'])}")
    
    # Syntax Issues
    if analysis['syntax_issues']:
        report.append("")
        report.append("⚠️  Syntax Issues:")
        for issue in analysis['syntax_issues'][:20]:  # Limit to 20
            report.append(f"  • {issue}")
        if len(analysis['syntax_issues']) > 20:
            report.append(f"  ... and {len(analysis['syntax_issues']) - 20} more")
    else:
        report.append("")
        report.append("✅ No syntax issues found")
    
    # Naming Issues
    if analysis['naming_issues']:
        report.append("")
        report.append("⚠️  Naming Convention Issues:")
        for issue in analysis['naming_issues'][:10]:
            report.append(f"  • {issue}")
        if len(analysis['naming_issues']) > 10:
            report.append(f"  ... and {len(analysis['naming_issues']) - 10} more")
    
    # Recommendations
    if analysis['recommendations']:
        report.append("")
        report.append("💡 Recommendations:")
        for rec in analysis['recommendations']:
            report.append(f"  • {rec}")
    
    report.append("")
    report.append("=" * 60)
    
    # Overall status
    total_issues = len(analysis['syntax_issues']) + len(analysis['naming_issues'])
    if total_issues == 0:
        report.append("✅ Schema validation passed!")
        return "\n".join(report), 0
    else:
        report.append(f"⚠️  Found {total_issues} issue(s) - review recommended")
        return "\n".join(report), 1


def main():
    if len(sys.argv) < 2:
        print("Usage: python schema_validator.py <project_path> [--connection-string <conn_str>]")
        sys.exit(1)
    
    project_path = sys.argv[1]
    connection_string = None
    
    if "--connection-string" in sys.argv:
        conn_index = sys.argv.index("--connection-string") + 1
        if conn_index < len(sys.argv):
            connection_string = sys.argv[conn_index]
    
    print("🗄️  SQL Schema Validator")
    print("=" * 60)
    print(f"Project: {project_path}")
    if connection_string:
        print("Connection: [CONFIGURED]")
    print()
    
    # Find SQL files
    print("Scanning for SQL files...")
    sql_files = find_sql_files(project_path)
    
    total_files = sum(len(files) for files in sql_files.values())
    if total_files == 0:
        print("⚠️  No SQL files found in project")
        print("\nExpected locations:")
        print("  • Migrations/")
        print("  • Database/")
        print("  • SQL/")
        sys.exit(0)
    
    print(f"✅ Found {total_files} SQL file(s)")
    print()
    
    # Analyze schema
    print("Analyzing schema quality...")
    print("-" * 60)
    analysis = analyze_schema_quality(sql_files)
    
    # Generate and print report
    report, exit_code = format_report(sql_files, analysis)
    print(report)
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
