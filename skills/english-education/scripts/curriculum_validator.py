#!/usr/bin/env python3
"""
Curriculum Validator - Validate English education content
Checks lesson plans, quizzes, and curriculum materials.

Usage:
    python curriculum_validator.py <file_or_folder>
"""

import sys
import re
from pathlib import Path


class CurriculumValidator:
    """Validate English education content."""
    
    CEFR_LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]
    
    REQUIRED_LESSON_SECTIONS = [
        "Overview",
        "Warm-up",
        "Practice",
        "Wrap-up"
    ]
    
    REQUIRED_QUIZ_SECTIONS = [
        "Level",
        "Time",
        "Questions"
    ]
    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def validate_file(self, file_path: Path) -> bool:
        """Validate a single file."""
        content = file_path.read_text(encoding="utf-8")
        filename = file_path.name.lower()
        
        if "lesson" in filename:
            return self.validate_lesson(content, file_path)
        elif "quiz" in filename:
            return self.validate_quiz(content, file_path)
        else:
            return self.validate_generic(content, file_path)
    
    def validate_lesson(self, content: str, file_path: Path) -> bool:
        """Validate a lesson plan."""
        valid = True
        
        # Check for required sections
        for section in self.REQUIRED_LESSON_SECTIONS:
            if section.lower() not in content.lower():
                self.errors.append(f"{file_path}: Missing section '{section}'")
                valid = False
        
        # Check for CEFR level
        if not self._has_cefr_level(content):
            self.warnings.append(f"{file_path}: No CEFR level specified")
        
        # Check for objectives
        if "objective" not in content.lower():
            self.warnings.append(f"{file_path}: No learning objectives found")
        
        # Check for duration
        if not re.search(r"\d+\s*(min|minute|hour)", content, re.I):
            self.warnings.append(f"{file_path}: No duration specified")
        
        return valid
    
    def validate_quiz(self, content: str, file_path: Path) -> bool:
        """Validate a quiz."""
        valid = True
        
        # Check for level
        if not self._has_cefr_level(content):
            self.errors.append(f"{file_path}: No CEFR level specified")
            valid = False
        
        # Check for questions
        if "question" not in content.lower() and "##" not in content:
            self.errors.append(f"{file_path}: No questions found")
            valid = False
        
        # Check for answer key
        if "answer" not in content.lower():
            self.warnings.append(f"{file_path}: No answer key found")
        
        # Check for point values
        if not re.search(r"\d+\s*point", content, re.I):
            self.warnings.append(f"{file_path}: No point values specified")
        
        return valid
    
    def validate_generic(self, content: str, file_path: Path) -> bool:
        """Generic content validation."""
        valid = True
        
        # Check minimum content length
        if len(content) < 100:
            self.warnings.append(f"{file_path}: Content seems too short")
        
        # Check for proper markdown structure
        if "#" not in content:
            self.warnings.append(f"{file_path}: No markdown headings found")
        
        return valid
    
    def _has_cefr_level(self, content: str) -> bool:
        """Check if content has a CEFR level."""
        for level in self.CEFR_LEVELS:
            if level in content.upper():
                return True
        return False
    
    def validate_folder(self, folder_path: Path) -> bool:
        """Validate all markdown files in a folder."""
        valid = True
        
        for file_path in folder_path.glob("**/*.md"):
            if not self.validate_file(file_path):
                valid = False
        
        return valid
    
    def report(self):
        """Print validation report."""
        print("=" * 60)
        print("CURRICULUM VALIDATION REPORT")
        print("=" * 60)
        
        if self.errors:
            print("\n❌ ERRORS:")
            for error in self.errors:
                print(f"  - {error}")
        
        if self.warnings:
            print("\n⚠️  WARNINGS:")
            for warning in self.warnings:
                print(f"  - {warning}")
        
        if not self.errors and not self.warnings:
            print("\n✅ All content validated successfully!")
        
        print("\n" + "-" * 60)
        print(f"Errors: {len(self.errors)}")
        print(f"Warnings: {len(self.warnings)}")
        
        return len(self.errors) == 0


def main():
    if len(sys.argv) < 2:
        print("Usage: python curriculum_validator.py <file_or_folder>")
        sys.exit(1)
    
    target = Path(sys.argv[1])
    validator = CurriculumValidator()
    
    if target.is_file():
        validator.validate_file(target)
    elif target.is_dir():
        validator.validate_folder(target)
    else:
        print(f"Error: {target} not found")
        sys.exit(1)
    
    success = validator.report()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
