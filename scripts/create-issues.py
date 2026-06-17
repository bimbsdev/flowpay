#!/usr/bin/env python3
"""
FlowPay Drips Wave Issues Creator
Creates all 65 GitHub issues for the Drips Wave program using the GitHub API.

Usage:
    python3 scripts/create-issues.py YOUR_GITHUB_TOKEN

Prerequisites:
    - Python 3.8+
    - requests library: pip install requests
    - GitHub Personal Access Token with 'repo' scope
"""

import requests
import json
import sys
import os

# Load issues from JSON file
ISSUES_FILE = os.path.join(os.path.dirname(__file__), '..', 'drips-issues.json')

def load_issues():
    """Load issues from JSON file"""
    try:
        with open(ISSUES_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {ISSUES_FILE} not found")
        sys.exit(1)

def get_repo_info():
    """Get repository owner and name from git config or prompt"""
    try:
        result = os.popen('git config --get remote.origin.url').read().strip()
        if 'github.com' in result:
            # Extract owner/repo from URL
            parts = result.split('/')
            repo = parts[-1].replace('.git', '')
            owner = parts[-2]
            return owner, repo
    except:
        pass
    
    # Fallback: prompt user
    owner = input("Enter GitHub username: ").strip()
    repo = input("Enter repository name: ").strip()
    return owner, repo

def create_issue(owner, repo, token, issue):
    """Create a single issue via GitHub API"""
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {
        "title": issue["title"],
        "body": issue["body"],
        "labels": issue.get("labels", [])
    }
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 201:
        return True, response.json()["number"]
    else:
        return False, response.text

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/create-issues.py YOUR_GITHUB_TOKEN")
        print("\nTo get a token:")
        print("1. Go to https://github.com/settings/tokens/new")
        print("2. Select 'repo' scope")
        print("3. Generate and copy the token")
        sys.exit(1)
    
    token = sys.argv[1]
    owner, repo = get_repo_info()
    
    print(f"\n📊 Creating Drips Wave issues for {owner}/{repo}")
    print("=" * 60)
    
    issues = load_issues()
    created = 0
    failed = 0
    
    for i, issue in enumerate(issues, 1):
        sys.stdout.write(f"\r[{i}/{len(issues)}] Creating issues...")
        sys.stdout.flush()
        
        success, result = create_issue(owner, repo, token, issue)
        
        if success:
            created += 1
            # Print issue number every 10 issues
            if created % 10 == 0:
                print(f"\n✅ Created #{result}: {issue['title'][:50]}")
        else:
            failed += 1
            print(f"\n❌ Failed: {issue['title']}")
            print(f"   Error: {result}")
    
    print("\n" + "=" * 60)
    print(f"✅ Successfully created {created} issues")
    if failed > 0:
        print(f"❌ Failed to create {failed} issues")
    print(f"\n📍 View your issues: https://github.com/{owner}/{repo}/issues")

if __name__ == "__main__":
    main()
