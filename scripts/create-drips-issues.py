#!/usr/bin/env python3
"""
GitHub Issue Creator for Drips Wave
Creates all 65 FlowPay Drips Wave issues in your GitHub repository.

Usage:
    python3 scripts/create-drips-issues.py --owner YOUR_GITHUB_USERNAME --repo flowpay-stellar --token YOUR_PAT

Prerequisites:
    pip install requests
"""

import json
import argparse
import sys
from pathlib import Path
import requests
from typing import Optional

class GitHubIssueCreator:
    def __init__(self, owner: str, repo: str, token: str):
        self.owner = owner
        self.repo = repo
        self.token = token
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json"
        }
        self.created_count = 0
        self.failed_count = 0
        self.failed_issues = []

    def load_issues(self) -> list:
        """Load issues from issues.json"""
        script_dir = Path(__file__).parent.parent
        issues_file = script_dir / "issues.json"
        
        if not issues_file.exists():
            print(f"Error: {issues_file} not found")
            sys.exit(1)
        
        with open(issues_file, 'r') as f:
            data = json.load(f)
        
        return data['issues']

    def create_issue(self, issue: dict) -> bool:
        """Create a single issue"""
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/issues"
        
        # Format the body with acceptance criteria
        body = f"{issue['description']}\n\n"
        body += "## Acceptance Criteria\n"
        for criterion in issue['acceptanceCriteria']:
            body += f"- [ ] {criterion}\n"
        
        payload = {
            "title": issue['title'],
            "body": body,
            "labels": issue['labels']
        }
        
        try:
            response = requests.post(url, json=payload, headers=self.headers, timeout=10)
            
            if response.status_code == 201:
                issue_number = response.json()['number']
                print(f"✓ Created issue #{issue_number}: {issue['title']}")
                self.created_count += 1
                return True
            else:
                error_msg = response.json().get('message', 'Unknown error')
                print(f"✗ Failed to create: {issue['title']}")
                print(f"  Error: {error_msg}")
                self.failed_count += 1
                self.failed_issues.append({
                    'title': issue['title'],
                    'error': error_msg
                })
                return False
        
        except requests.exceptions.Timeout:
            print(f"✗ Timeout creating: {issue['title']}")
            self.failed_count += 1
            self.failed_issues.append({
                'title': issue['title'],
                'error': 'Request timeout'
            })
            return False
        
        except Exception as e:
            print(f"✗ Exception creating: {issue['title']}")
            print(f"  Error: {str(e)}")
            self.failed_count += 1
            self.failed_issues.append({
                'title': issue['title'],
                'error': str(e)
            })
            return False

    def verify_authentication(self) -> bool:
        """Verify GitHub authentication"""
        url = f"{self.base_url}/user"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                user = response.json()['login']
                print(f"✓ Authenticated as: {user}")
                return True
            else:
                print("✗ Authentication failed")
                print(f"  Status: {response.status_code}")
                print(f"  Message: {response.json().get('message', 'Unknown error')}")
                return False
        except Exception as e:
            print(f"✗ Authentication error: {str(e)}")
            return False

    def verify_repository(self) -> bool:
        """Verify repository access"""
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                repo_name = response.json()['full_name']
                print(f"✓ Repository found: {repo_name}")
                return True
            else:
                print(f"✗ Repository not found: {self.owner}/{self.repo}")
                return False
        except Exception as e:
            print(f"✗ Repository verification error: {str(e)}")
            return False

    def run(self) -> bool:
        """Run the issue creator"""
        print("=" * 60)
        print("FlowPay Drips Wave Issue Creator")
        print("=" * 60)
        print()
        
        # Verify authentication
        print("Verifying authentication...")
        if not self.verify_authentication():
            return False
        print()
        
        # Verify repository
        print("Verifying repository access...")
        if not self.verify_repository():
            return False
        print()
        
        # Load issues
        print("Loading issues from issues.json...")
        issues = self.load_issues()
        print(f"✓ Loaded {len(issues)} issues")
        print()
        
        # Create issues
        print("Creating issues...")
        print("-" * 60)
        
        for i, issue in enumerate(issues, 1):
            print(f"[{i}/{len(issues)}] ", end='')
            self.create_issue(issue)
        
        print("-" * 60)
        print()
        
        # Print summary
        print("=" * 60)
        print("Summary")
        print("=" * 60)
        print(f"✓ Successfully created: {self.created_count}")
        print(f"✗ Failed: {self.failed_count}")
        print(f"Total: {len(issues)}")
        
        if self.failed_issues:
            print()
            print("Failed Issues:")
            for failed in self.failed_issues:
                print(f"  - {failed['title']}")
                print(f"    Error: {failed['error']}")
        
        print()
        print("=" * 60)
        print(f"View issues at: https://github.com/{self.owner}/{self.repo}/issues")
        print("=" * 60)
        
        return self.failed_count == 0

def main():
    parser = argparse.ArgumentParser(
        description='Create Drips Wave issues in GitHub',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  python3 scripts/create-drips-issues.py \\
    --owner myusername \\
    --repo flowpay-stellar \\
    --token ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

  # Use environment variable for token
  export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  python3 scripts/create-drips-issues.py \\
    --owner myusername \\
    --repo flowpay-stellar

To create a GitHub Personal Access Token:
  1. Go to https://github.com/settings/tokens/new
  2. Select scopes: 'repo' and 'write:org'
  3. Generate and copy the token
  4. Use as --token argument or GITHUB_TOKEN env var
        """
    )
    
    parser.add_argument('--owner', required=True, help='GitHub username/owner')
    parser.add_argument('--repo', required=True, help='Repository name')
    parser.add_argument('--token', help='GitHub Personal Access Token (or use GITHUB_TOKEN env var)')
    
    args = parser.parse_args()
    
    # Get token from argument or environment variable
    token = args.token or os.environ.get('GITHUB_TOKEN')
    
    if not token:
        print("Error: GitHub token not provided")
        print("Use --token argument or set GITHUB_TOKEN environment variable")
        sys.exit(1)
    
    # Create and run the issue creator
    creator = GitHubIssueCreator(args.owner, args.repo, token)
    success = creator.run()
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    import os
    main()
