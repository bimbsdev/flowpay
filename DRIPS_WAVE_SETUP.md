# Drips Wave Setup Guide for FlowPay

## Overview

FlowPay is now ready for the **Drips Wave** program! Drips Wave is a recurring bounty program where:
- **You** (as maintainer) post issues for contributors to fix
- **Contributors** earn points/rewards for merged PRs
- **Drips** handles the tracking and distribution

This guide walks you through setting up FlowPay for Drips Wave.

---

## ✅ What's Included

### 1. **65 Pre-Created Issues** 📋
All categorized with complexity points and acceptance criteria:

- **Documentation (6 issues)** - 1-3 points each
- **Bug Fixes (7 issues)** - 2-5 points each
- **Testing (6 issues)** - 3-13 points each
- **Frontend (7 issues)** - 2-8 points each
- **Security (6 issues)** - 3-13 points each
- **Performance (5 issues)** - 3-13 points each
- **Architecture (6 issues)** - 5-13 points each
- **Features (7 issues)** - 3-21 points each
- **Infrastructure (5 issues)** - 3-13 points each
- **Blockchain (5 issues)** - 5-13 points each
- **Polish (5 issues)** - 1-3 points each

**Total:** 65 issues across all difficulty levels

### 2. **Issues Are Stored In**
📄 [DRIPS_WAVE_ISSUES.md](./DRIPS_WAVE_ISSUES.md) - Complete issue catalog with full descriptions and acceptance criteria

### 3. **Automated Issue Creation Script**
🔧 `scripts/create-drips-issues.sh` - Bash script using GitHub CLI to batch-create all issues

---

## 🚀 Quick Start Options

### **Option A: Authenticate GitHub CLI & Auto-Create (Recommended)**

This automatically creates all 65 issues in your GitHub repo.

```bash
# Step 1: Authenticate with GitHub
gh auth login

# When prompted:
# - Choose "HTTPS" as protocol
# - Answer "Yes" to authenticate Git
# - Open the browser link and enter the device code

# Step 2: Run the issue creation script
bash scripts/create-drips-issues.sh
```

**Result:** All 65 issues created automatically with labels and descriptions ✅

---

### **Option B: Manual Creation in GitHub UI**

If you prefer not to use CLI:

1. Go to your repository: `https://github.com/YOUR_USERNAME/flowpay-stellar`
2. Click **Issues** tab
3. Click **New Issue**
4. Copy-paste issues from [DRIPS_WAVE_ISSUES.md](./DRIPS_WAVE_ISSUES.md)
5. Add labels: `drips-wave`, `N-points`, and category label

---

### **Option C: One-at-a-Time with GitHub Web UI**

Create issues using the GitHub interface:

```markdown
Template for each issue:

Title: [Copy from DRIPS_WAVE_ISSUES.md]
Description: [Copy the Description and Acceptance Criteria sections]
Labels: [drips-wave, X-points (1/2/3/5/8/13/21), category]
```

---

## 🔐 GitHub CLI Authentication Troubleshooting

### If browser auth doesn't work:
```bash
# Use token-based auth instead
gh auth login

# Choose:
# - Hostname: github.com
# - Protocol: HTTPS
# - Enter PAT (Personal Access Token) when prompted
```

**To create a PAT:**
1. Go to: https://github.com/settings/tokens/new
2. Select scopes: `repo`, `write:org`
3. Generate and copy token
4. Paste in terminal when prompted

---

## 📊 Issues Summary

### By Complexity Level
| Level | Count | Description |
|-------|-------|-------------|
| 🟢 Easy | 28 | 1-5 points (1-3 hour tasks) |
| 🟡 Medium | 28 | 5-13 points (half-day tasks) |
| 🔴 Hard | 9 | 13+ points (multi-day tasks) |

### By Category
| Category | Count | Examples |
|----------|-------|----------|
| 📚 Documentation | 6 | API docs, deployment guides |
| 🐛 Bug Fixes | 7 | Race conditions, validation issues |
| ✅ Testing | 6 | Unit, integration, E2E tests |
| 🎨 Frontend | 7 | Forms, modals, dark mode |
| 🔐 Security | 6 | CSRF, sanitization, encryption |
| 🚀 Performance | 5 | Caching, optimization |
| 🏗️ Architecture | 6 | Refactoring, patterns, DI |
| 📊 Features | 7 | Analytics, refunds, multi-currency |
| 📱 Infrastructure | 5 | Docker, K8s, monitoring |
| 🌐 Blockchain | 5 | Stellar integration, contracts |
| 🐞 Polish | 5 | Typos, UX tweaks |

---

## 🎯 After Creating Issues

### 1. **Add Issue Labels** (if not auto-created)
```bash
# For each issue, add labels:
- drips-wave          (identifies as Drips Wave issue)
- N-points            (1, 2, 3, 5, 8, 13, or 21 points)
- category            (documentation, bug, frontend, etc.)
```

### 2. **Create GitHub Projects Board** (Optional)
- New Project: "Drips Wave - Wave 1"
- Add all 65 issues
- Status columns: Todo, In Progress, In Review, Done
- Share link with contributors

### 3. **Create README Section for Contributors**
Add to your main README.md:

```markdown
## 🌊 Contributing via Drips Wave

FlowPay is part of the Stellar ecosystem's Drips Wave program!

### 🎯 How to Contribute
1. Browse [open issues](./issues?q=label%3Adrips-wave)
2. Pick an issue matching your skill level
3. Create a fork and start coding
4. Submit a PR when ready
5. Earn points toward Drips Wave rewards

### 📊 Issues by Difficulty
- 🟢 Easy (1-5 points): [View](./issues?q=label%3Adrips-wave+label%3A1-points)
- 🟡 Medium (5-13 points): [View](./issues?q=label%3Adrips-wave+label%3A5-points)
- 🔴 Hard (13+ points): [View](./issues?q=label%3Adrips-wave+label%3A13-points)

Learn more: [DRIPS_WAVE_ISSUES.md](./DRIPS_WAVE_ISSUES.md)
```

### 4. **Set Up Drips Wave Program**
Go to: https://drips.network/wave

1. Log in with GitHub
2. Apply your repository to the Wave program
3. Select issues you want contributors to work on
4. Set point values and rewards
5. Launch the Wave!

---

## 💡 Tips for Success

### For Attracting Contributors
✅ **Start with easy issues** to onboard new contributors
✅ **Clear acceptance criteria** - be specific about what "done" means
✅ **Mention prerequisite knowledge** if needed
✅ **Link to relevant docs** for context
✅ **Be responsive** to PR questions

### For Managing the Wave
✅ **Review PRs promptly** (within 2-3 days if possible)
✅ **Provide feedback** to help contributors improve
✅ **Merge early** to keep momentum going
✅ **Report progress** to Drips Wave organizers

### Issue Best Practices
✅ **Break big issues into smaller ones** (5-10 points is sweet spot)
✅ **Avoid ambiguous requirements** - be specific
✅ **Include examples** in code-heavy issues
✅ **Link to related issues** for context
✅ **Update issue status** as work progresses

---

## 🔗 Useful Links

- **FlowPay Issues:** [All 65 Drips Wave Issues](./DRIPS_WAVE_ISSUES.md)
- **Drips Wave Program:** https://drips.network/wave
- **Stellar Ecosystem:** https://drips.network/wave/ecosystems
- **Contributor Guide:** https://docs.drips.network/wave/contributors
- **Maintainer Guide:** https://docs.drips.network/wave/maintainers

---

## 📋 Issue Creation Checklist

Before launching your Wave:

- [ ] All 65 issues created in GitHub
- [ ] Each issue has appropriate labels
- [ ] Issue descriptions are clear
- [ ] Links to documentation are working
- [ ] README updated with contributor section
- [ ] Project board created (optional)
- [ ] FlowPay repo applied to Drips Wave program
- [ ] Wave launch date set
- [ ] Contributors invited/announced
- [ ] Monitoring dashboard set up

---

## ⚠️ Common Issues & Solutions

### Problem: "gh: command not found"
**Solution:** Install GitHub CLI
```bash
brew install gh
```

### Problem: "Authentication failed"
**Solution:** Use personal access token
```bash
gh auth login
# Choose: Paste a token instead
# Create token at: https://github.com/settings/tokens/new
```

### Problem: "Issues not showing labels"
**Solution:** Manually add labels after creation
```bash
gh issue edit ISSUE_NUMBER --add-label "drips-wave,5-points,backend"
```

### Problem: "Duplicate issues created"
**Solution:** List issues and delete duplicates
```bash
gh issue list --limit 100
gh issue delete ISSUE_NUMBER  # Delete the duplicate
```

---

## 🎉 Next Steps

1. **Create all 65 issues** using one of the methods above
2. **Verify issues look good** in your GitHub repo
3. **Apply to Drips Wave** at https://drips.network/wave
4. **Set up project board** for tracking (optional)
5. **Announce to community** - share the Wave launch!
6. **Monitor progress** and support contributors
7. **Distribute rewards** when Wave completes

---

## 📞 Support

For questions about:
- **GitHub CLI:** `gh --help` or https://cli.github.com
- **Drips Wave:** https://docs.drips.network/wave
- **FlowPay issues:** See [DRIPS_WAVE_ISSUES.md](./DRIPS_WAVE_ISSUES.md)

---

**Status:** ✅ FlowPay is fully prepared for Drips Wave!

Next: Authenticate GitHub CLI and run the issue creation script.
