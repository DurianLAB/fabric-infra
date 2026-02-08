# Agent Guidelines

This document contains guidelines and constraints for AI agents working on this repository.

## Constraints

### No Emojis

**Rule:** Do NOT use emojis in any files, documentation, code comments, commit messages, or any other content in this repository.

**Applies to:**
- README files
- Documentation (all .md files)
- Code comments
- Variable names
- Function names
- Commit messages
- Pull request descriptions
- Configuration files
- Any other text content

**Examples of prohibited content:**
```
# Bad - contains emojis
✅ Success
🚀 Deployment complete
⚠️ Warning: Check this
🔥 Hot fix
💰 Cost: $1-2/month
```

```
# Good - no emojis
Success
Deployment complete
Warning: Check this
Hot fix
Cost: $1-2/month
```

**Rationale:** 
- Emojis can cause rendering issues in different terminals and environments
- They may not display correctly in all documentation viewers
- Plain text is more universally compatible
- Keeps the codebase clean and professional

### Text Replacements

Use these text alternatives instead of emojis:

| Instead of | Use |
|------------|-----|
| ✅ | [OK], [DONE], [SUCCESS] |
| ❌ | [FAIL], [ERROR], [X] |
| ⚠️ | [WARNING], [CAUTION] |
| 🚀 | [DEPLOY], [LAUNCH] |
| 🔥 | [HOT], [CRITICAL] |
| 💰 | [COST], [PRICE] |
| 📝 | [NOTE], [DOC] |
| 🔧 | [CONFIG], [SETUP] |
| 📊 | [CHART], [DIAGRAM] |
| 💡 | [TIP], [IDEA] |
| 🎯 | [GOAL], [TARGET] |
| 🏗️ | [ARCH], [BUILD] |
| 📦 | [PACKAGE] |
| 🔗 | [LINK] |
| ✓ | [OK], [YES] |
| ✗ | [X], [NO] |

### Commit Messages

Follow conventional commit format without emojis:

```
feat: Add new feature
fix: Fix bug in module
docs: Update documentation
refactor: Refactor code
```

NOT:
```
✨ feat: Add new feature
🐛 fix: Fix bug
📚 docs: Update docs
```

## Workflow Guidelines

1. Always check existing files for emoji usage before editing
2. Remove any emojis found in existing content
3. Use text-based indicators (like [OK], [WARNING]) instead of emojis
4. Keep all communication professional and emoji-free

## Review Checklist

Before submitting any changes, verify:
- [ ] No emojis in modified files
- [ ] No emojis in commit messages
- [ ] No emojis in documentation
- [ ] No emojis in code comments
- [ ] Text alternatives used where appropriate
