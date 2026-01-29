#!/usr/bin/env python3
"""
Course Companion FTE Initialization Script

This script helps set up and initialize the Course Companion FTE system
for educational tutoring platforms.
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional


class CourseCompanionInitializer:
    """Initialize and configure Course Companion FTE system."""

    def __init__(self, project_dir: str = "."):
        self.project_dir = project_dir
        self.config = {}

    def create_project_structure(self):
        """Create the basic directory structure for Course Companion FTE."""
        dirs_to_create = [
            "backend",
            "frontend",
            "courses",
            "quizzes",
            "students",
            "assets",
            "logs"
        ]

        for directory in dirs_to_create:
            path = os.path.join(self.project_dir, directory)
            os.makedirs(path, exist_ok=True)
            print(f"Created directory: {path}")

    def create_config_file(self, course_topic: str = "ai-agent-development"):
        """Create a configuration file for the Course Companion FTE."""
        config = {
            "course_companion_fte": {
                "version": "1.0",
                "course_topic": course_topic,
                "architecture": {
                    "phase": 1,
                    "backend_llm": False,
                    "features": {
                        "content_delivery": True,
                        "navigation": True,
                        "grounded_qa": True,
                        "rule_based_quizzes": True,
                        "progress_tracking": True,
                        "freemium_gate": True
                    }
                },
                "components": {
                    "backend": {
                        "framework": "fastapi",
                        "storage": "cloudflare_r2"
                    },
                    "frontend": {
                        "platform": "chatgpt_app_or_web",
                        "framework": "nextjs_react"
                    }
                },
                "created_at": datetime.now().isoformat(),
                "cost_efficiency": {
                    "target_users_monthly": 10000,
                    "estimated_cost_range": "$16-$41",
                    "cost_per_user": "$0.002-$0.004"
                }
            }
        }

        config_path = os.path.join(self.project_dir, "config.json")
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)

        print(f"Created configuration file: {config_path}")
        return config

    def create_course_template(self, course_name: str):
        """Create a template for a new course."""
        course_dir = os.path.join(self.project_dir, "courses", course_name)
        os.makedirs(course_dir, exist_ok=True)

        # Create basic course structure
        course_files = {
            "syllabus.md": f"# {course_name.replace('-', ' ').title()} Course Syllabus\n\n## Overview\n\n## Learning Objectives\n\n## Modules\n\n## Assessment\n",
            "modules.json": json.dumps({
                "course": course_name,
                "modules": [],
                "prerequisites": [],
                "learning_objectives": []
            }, indent=2),
            "quizzes.json": json.dumps({
                "course": course_name,
                "quizzes": []
            }, indent=2)
        }

        for filename, content in course_files.items():
            filepath = os.path.join(course_dir, filename)
            with open(filepath, 'w') as f:
                f.write(content)
            print(f"Created course file: {filepath}")

    def initialize_system(self, course_topic: str = "ai-agent-development"):
        """Complete initialization of the Course Companion FTE system."""
        print("Initializing Course Companion FTE System...")

        self.create_project_structure()
        self.create_config_file(course_topic)
        self.create_course_template(course_topic)

        print("\nCourse Companion FTE system initialized successfully!")
        print(f"Project directory: {self.project_dir}")
        print(f"Course topic: {course_topic}")
        print("\nNext steps:")
        print("1. Review config.json for customization")
        print("2. Add course content to courses/ directory")
        print("3. Configure quizzes in quizzes/ directory")
        print("4. Set up backend and frontend components")


def main():
    """Main entry point for the initialization script."""
    import argparse

    parser = argparse.ArgumentParser(description="Initialize Course Companion FTE system")
    parser.add_argument("--dir", default=".", help="Project directory (default: current directory)")
    parser.add_argument("--topic", default="ai-agent-development",
                       choices=["ai-agent-development", "cloud-native-python",
                               "generative-ai-fundamentals", "modern-python"],
                       help="Course topic to initialize")

    args = parser.parse_args()

    initializer = CourseCompanionInitializer(args.dir)
    initializer.initialize_system(args.topic)


if __name__ == "__main__":
    main()