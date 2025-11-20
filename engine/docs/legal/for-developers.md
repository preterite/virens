---
title: VIRENS License Guide for Developers
license: CC-BY-SA-4.0
copyright: © 2025 Mike Edwards
framework/docs/legal/for-developers.md
---

# VIRENS Licensing for Developers

This guide addresses licensing questions for developers who want to contribute to, fork, or build upon VIRENS.

## Executive Summary

**VIRENS welcomes contributions under AGPL-3.0.**

Key points for developers:

- ✅ **Contributions welcome:** No CLA required, just submit PRs
- ✅ **Fork friendly:** You can create derivatives under AGPL-3.0
- ✅ **Attribution preserved:** Git history maintains your credit
- ✅ **Copyleft protection:** Derivatives must stay open source
- ⚠️ **Network copyleft:** Hosted services must share source
- ❌ **No proprietary derivatives:** Can't close-source your fork

## Understanding AGPL-3.0 for Developers

### What AGPL Means Technically

**AGPL-3.0 = GPL-3.0 + Network Copyleft Clause**

**Standard GPL requirements:**
- Derivative works must be GPL-compatible
- Source code must be available with distributions
- License and copyright notices preserved
- No additional restrictions

**AGPL addition (Section 13):**
- If you run modified AGPL software as a network service
- Users interacting with it remotely must be able to download source
- Prevents "SaaS loophole" where GPL could be circumvented

### What Counts as a "Derivative Work"?

**Clearly derivative (must be AGPL):**
- Modifications to VIRENS source files
- New modules that import VIRENS code
- Plugins that link against VIRENS libraries
- Scripts that incorporate VIRENS functions
- Extensions that subclass VIRENS classes

**Potentially independent (could be separate):**
- Separate programs that read/write VIRENS data files
- External tools that call VIRENS via command-line
- Independent services that interact via APIs only
- Configuration files and templates (arguably data, not code)

**Grey area - ask if unsure:**
- Plugins with minimal VIRENS dependencies
- Wrapper scripts that orchestrate VIRENS
- GUI front-ends that shell out to VIRENS commands

### What "Network Service" Means

**Network copyleft triggers when:**
- You run modified VIRENS on a server
- Users access it via HTTP, SSH, or other network protocol
- The interaction is more than trivial (actual functionality, not just downloading)

**Examples that trigger network copyleft:**
- Web-based VIRENS portal for multiple users
- Cloud-hosted VIRENS-as-a-service
- API service built on modified VIRENS
- Hosted research platform using VIRENS backend

**Examples that DON'T trigger:**
- Installing VIRENS on users' own machines
- Providing VIRENS installation scripts
- Running VIRENS locally for your own use
- Offering VIRENS via download (distribution, not service)

## Contributing to VIRENS

### How to Contribute

**Step-by-step:**

1. **Fork** the repository on GitHub
2. **Clone** your fork locally
   ```
   git clone https://github.com/yourusername/virens.git
   cd virens
   ```
3. **Create a branch** for your changes
   ```
   git checkout -b feature/your-feature-name
   ```
4. **Make changes** following code style guidelines
5. **Test** thoroughly on macOS
6. **Commit** with clear messages
   ```
   git commit -m "Add feature: brief description"
   ```
7. **Push** to your fork
   ```
   git push origin feature/your-feature-name
   ```
8. **Open Pull Request** on main repository

### License Grant for Contributions

**By submitting a pull request, you agree:**

- Your contribution is licensed under AGPL-3.0 (for code)
- Your contribution is licensed under CC-BY-SA-4.0 (for docs)
- You have the right to submit this contribution
- You grant VIRENS project the right to use/modify/distribute it

**No CLA signing required.** PR submission = acceptance.

### Code Headers

**Add these headers to new files:**

**Shell scripts:**
```
#!/usr/bin/env zsh
# Copyright © 2025 Mike Edwards and contributors
# SPDX-License-Identifier: AGPL-3.0-or-later
```

**Python files:**
```
#!/usr/bin/env python3
# Copyright © 2025 Mike Edwards and contributors
# SPDX-License-Identifier: AGPL-3.0-or-later
```

**Documentation:**
```
---
title: Your Document Title
license: CC-BY-SA-4.0
copyright: © 2025 Mike Edwards and contributors
---
```

### Copyright Attribution

**For new files:**
- Copyright line: `Copyright © 2025 Mike Edwards and contributors`
- This acknowledges both original author and community contributions
- Git history preserves individual contributor credit

**For modified files:**
- Keep existing copyright line
- Add your changes via Git commit
- Don't add separate copyright lines per contributor (Git tracks this)

**You retain copyright on your contributions.** You grant VIRENS a license to use them under AGPL/CC-BY-SA.

### Contribution Guidelines

**Code quality:**
- Follow existing code style (see CONTRIBUTING.md)
- Include tests for new features
- Document public APIs
- Keep changes focused (one feature/fix per PR)

**Documentation:**
- Update README if changing core functionality
- Add docstrings to new functions
- Update user guides for user-facing changes
- Write in clear, concise English

**Commit messages:**
- First line: Brief summary (50 chars or less)
- Blank line
- Detailed description if needed
- Reference issues: "Fixes #123"

**Communication:**
- Discuss major changes in issues first
- Respond to code review feedback promptly
- Be respectful and constructive
- Ask questions if requirements unclear

## Forking VIRENS

### You Can Fork If...

**Valid reasons to fork:**
- Different feature priorities than main project
- Experimental features not ready for upstream
- Specialized version for your institution/field
- Learning by building your own variant
- Disagreement with project direction

**AGPL allows forking.** This is a feature, not a bug.

### Fork Requirements

**Must do:**
1. Keep AGPL-3.0 license
2. Preserve copyright notices
3. Credit original VIRENS project
4. Share your source code
5. Document your changes

**Should do:**
- Give fork a distinct name
- Clearly state it's a VIRENS fork
- Maintain CHANGELOG
- Consider contributing improvements upstream
- Don't disparage original project

**Example fork README:**
```
# AcademicFlow

AcademicFlow is a fork of [VIRENS](https://github.com/preterite/virens)
focused on legal scholarship workflows.

## Changes from VIRENS
- Added case law citation support
- Integrated with Westlaw API
- Custom templates for law journals

## License
AcademicFlow inherits AGPL-3.0 from VIRENS.
Copyright © 2025 [Your Name]
Original VIRENS copyright © 2025 Mike Edwards
```

### Coordinating with Upstream

**Best practices:**
- Open issues on main repo before major forks
- Contribute generally-useful features back
- Track upstream changes (periodic merges)
- Coordinate on compatibility

**Fork vs. Contribute decision:**

| Scenario | Fork | Contribute |
|----------|------|------------|
| Small bug fix | ❌ | ✅ Contribute |
| New core feature | ❌ | ✅ Contribute first |
| Breaking changes | ✅ | ❌ Probably fork |
| Niche specialty feature | ✅ | ⚠️ Could go either way |
| Experimental ideas | ✅ | ⚠️ Fork, then contribute if successful |

## Building on VIRENS

### Creating Extensions

**Plugin architecture:**
- VIRENS doesn't yet have formal plugin system
- Contributions to create one welcome
- Currently: extend via scripts in user instance

**If you build extensions:**
- Keep them AGPL-3.0 if they incorporate VIRENS code
- Document dependencies clearly
- Submit to community plugin repository (if created)

### Integration Projects

**Examples of projects that could build on VIRENS:**

**Separate tools (potentially non-AGPL):**
- GUI wrapper that shells out to VIRENS commands
- Web dashboard that reads VIRENS data files
- Mobile app that syncs with VIRENS via files
- Notification service that monitors VIRENS events

**Key question:** Does it link/import VIRENS code, or just interact with data?

**Derivative works (must be AGPL):**
- Modified VIRENS with new modules
- VIRENS library imported into your app
- Fork with integrated features
- Service built on VIRENS backend

**Grey area:** Consult [AGPL FAQ](https://www.gnu.org/licenses/gpl-faq.html) or ask.

### API Development

**Currently:** VIRENS doesn't expose APIs (command-line and file-based)

**If you build APIs:**
- Consider contributing to main project
- If separate: Can be independent (if not derivative)
- If integrated: Must be AGPL

**Example independent API:**
```
VIRENS (command-line) → Data files → Your API (reads files) → HTTP endpoints
```
This could potentially be non-AGPL (just reading data files).

**Example derivative API:**
```
from virens import core  # Imports VIRENS code
# Your API must be AGPL
```

### Using VIRENS as a Library

**Current state:** VIRENS is a framework, not a library

**If you want to use VIRENS code programmatically:**
- Your project becomes AGPL derivative
- Must share your source code
- Copyleft applies

**Alternative:** Interact via command-line/files instead of importing code.

## License Compatibility

### Can I Mix VIRENS with Other Licenses?

**Compatible open source licenses:**
- ✅ GPL-3.0 (AGPL is GPL-compatible)
- ✅ LGPL-3.0 (as library, not derivative)
- ✅ MIT (can incorporate into AGPL project)
- ✅ Apache-2.0 (compatible with AGPL)
- ✅ BSD (can incorporate into AGPL project)

**Incompatible licenses:**
- ❌ GPL-2.0-only (version conflict)
- ❌ Proprietary/closed-source
- ❌ Licenses with additional restrictions
- ❌ CC-BY-NC (NonCommercial conflicts)

**Direction matters:**
- AGPL can incorporate MIT code → ✅ Works
- MIT project cannot incorporate AGPL code → ❌ Becomes AGPL

### Dual Licensing

**VIRENS currently uses:**
- Code: AGPL-3.0
- Documentation: CC-BY-SA-4.0

**This is common and compatible.**

**Could VIRENS add MIT/commercial licensing?**
- Theoretically yes, if copyright holder agrees
- Would require all contributors to agree (for past contributions)
- Or new code only dual-licensed (complex)
- Currently not offered

### GPL vs. AGPL

**AGPL-3.0 is GPL-3.0-compatible.**

**You can:**
- Use GPL-3.0 libraries in AGPL project
- Mix GPL and AGPL code

**Result:** Combined work is AGPL (stricter license wins).

**You cannot:**
- Take AGPL code and release under GPL-only
- AGPL requires network copyleft, GPL doesn't

## Common Developer Questions

### Can I use VIRENS code in my PhD project?

**Yes, if your project is AGPL-compatible.**

**Scenarios:**

**Open source project:** ✅ Use VIRENS freely, keep your code AGPL.

**Proprietary project:** ❌ Cannot incorporate VIRENS code.

**Research tool (private):** ✅ Use locally, no sharing required unless you offer as service.

**Academic paper:** ✅ Describing VIRENS or citing it is fine.

### Do I need to publish my research code if I use VIRENS?

**Not automatically.**

**If you:**
- Write scripts that call VIRENS commands → Not necessarily derivative
- Import VIRENS code as library → Becomes AGPL derivative
- Just use VIRENS as a tool → Your code is independent

**Academic best practice:** Publish research code anyway (reproducibility).

### Can I include VIRENS in my software portfolio?

**Yes, but clarify your role:**

**Good:**
- "Contributed X feature to VIRENS (AGPL open source project)"
- "Built custom VIRENS extensions for [institution]"
- "Experience with VIRENS research workflow system"

**Avoid:**
- Implying you own VIRENS
- Taking credit for others' contributions

**Linking to contributions:**
- Include GitHub profile with commit history
- Link to specific PRs or issues
- Describe technical challenges solved

### What if I want to use VIRENS code in a startup?

**AGPL complicates proprietary SaaS startups.**

**Options:**

**1. Keep it open source:**
- Build AGPL-compliant service
- Compete on service quality, not proprietary code
- Examples: GitLab, Nextcloud
- **Viable:** Yes, if your value is service/hosting

**2. Don't use VIRENS code:**
- Build similar functionality from scratch
- Interact with VIRENS via files/commands only
- **Viable:** Yes, but significant effort

**3. Contact developer about commercial licensing:**
- Request proprietary licensing option
- Currently not offered, but theoretically possible
- Would likely require payment
- **Viable:** Maybe, if developer agrees

**4. Different approach:**
- Build proprietary complementary tools (not derivatives)
- Integrate with VIRENS without incorporating code
- **Viable:** Yes, if truly independent

### Can I get paid for my contributions?

**Not directly from license, but potentially:**

**Funding:**
- Apply for grants to work on VIRENS
- Crowdfunding for features (community-funded)
- Employer paying you to contribute (common in corporate open source)

**Indirect benefits:**
- Reputation building → Consulting opportunities
- Job opportunities (employers value open source contributions)
- Speaking engagements
- Professional network

**Developer may eventually:**
- Hire core contributors
- Offer bounties for features
- Create foundation with paid positions

### What about patents?

**AGPL-3.0 includes patent provisions:**

- Contributors grant patent license for their contributions
- If you contribute code, you grant patent rights to users
- Protects project from patent trolling

**If you hold relevant patents:**
- Contributing = granting patent license
- Can't contribute then sue for patent infringement
- Standard open source practice

**If VIRENS infringes your patent:**
- Contact developer before legal action
- Community can work around patent
- Fork if necessary (AGPL allows this)

### Can I remove features or simplify VIRENS?

**Yes, AGPL allows modification.**

**You can:**
- Strip down to minimal functionality
- Remove modules you don't need
- Simplify installation process
- Optimize for specific use cases

**You must:**
- Keep AGPL license
- Preserve copyright notices
- Share your modified version (if offering as service)

**Example:** "VIRENS Lite" - stripped-down version for undergrads.

### What if VIRENS changes direction and I disagree?

**Fork it.**

**AGPL protects your ability to:**
- Take current version and maintain it
- Take project in different direction
- Preserve features that might be removed
- Serve users with different needs

**Famous examples:**
- MariaDB (forked from MySQL)
- LibreOffice (forked from OpenOffice)
- Nextcloud (forked from ownCloud)

**This is a feature of AGPL, not a bug.**

### How do I handle dependencies?

**When adding dependencies to VIRENS:**

**Permissive licenses (MIT, BSD, Apache):**
- ✅ Can incorporate into AGPL project
- Result: Combined work is AGPL
- Document in README

**Copyleft licenses (GPL, LGPL):**
- ✅ GPL-3.0 compatible with AGPL
- ✅ LGPL as library (dynamically linked)
- Check version compatibility

**Restrictive licenses:**
- ❌ Proprietary libraries create problems
- ❌ Incompatible copyleft (GPL-2.0-only)
- Find alternatives

**Best practice:**
- Prefer permissive or AGPL dependencies
- Document all dependency licenses
- Check compatibility before adding

### Can I copyright my contributions?

**Yes, you retain copyright.**

**Standard practice:**
- You own copyright on your specific contributions
- Git history proves authorship
- File header says "and contributors"
- No need for separate copyright lines per contributor

**License grant:**
- You grant VIRENS project perpetual license under AGPL
- You can still use your code elsewhere (you own it)
- Can't revoke license already granted

**Example:**
- You write a new module → You own copyright
- You license it to VIRENS under AGPL → Project can use it
- You can also use same code in your other AGPL projects → Your code

## Technical Implementation

### SPDX License Identifiers

**Use in all files:**
```
SPDX-License-Identifier: AGPL-3.0-or-later
```

**Benefits:**
- Machine-readable license identification
- Standard format across projects
- Easy compliance checking

**"or-later" vs. "only":**
- `AGPL-3.0-or-later` → Can use this version or any later AGPL version
- `AGPL-3.0-only` → Only this specific version
- VIRENS uses `or-later` for future compatibility

### License File Location

**Required files in repository root:**
- `LICENSE` (full AGPL-3.0 text)
- `LICENSE-DOCS` (full CC-BY-SA-4.0 text)
- `CONTRIBUTING.md` (contributor guidelines)
- `README.md` (with license section)

**In documentation:**
- `framework/docs/legal/` (detailed guides)

### Compliance Checking

**Tools for checking license compliance:**

```
# Check for license headers
rg -l "SPDX-License-Identifier" --files-without-match

# Find files without copyright
rg -l "Copyright" --files-without-match

# Verify AGPL-3.0 identifier
rg "AGPL-3.0-or-later"
```

**CI/CD integration:**
- Add license checking to GitHub Actions
- Fail builds with missing licenses
- Automated compliance

### Source Code Disclosure (for services)

**If you offer VIRENS as a network service:**

**Minimum compliance:**
```
<!-- In your web interface -->
<footer>
  <a href="/source">Download Source Code</a>
</footer>
```

**Provide:**
- Complete source code
- Build instructions
- Configuration files
- Any modifications you made

**Methods:**
- Direct download link
- Git repository URL
- Source code on request (respond promptly)

## Development Ethics

### Best Practices

**Technical:**
- Write clean, maintainable code
- Test thoroughly before submitting
- Document clearly
- Follow project conventions

**Community:**
- Be respectful in discussions
- Help newcomers
- Review others' PRs constructively
- Give credit where due

**Legal:**
- Follow license requirements strictly
- Don't submit code you don't have rights to
- Be honest about compatibility issues
- Disclose conflicts of interest

### Building Your Reputation

**Open source contributions help your career:**

**Visibility:**
- GitHub profile showcases contributions
- Employers value open source experience
- Community recognition

**Skills:**
- Real-world project experience
- Code review practice
- Collaboration skills
- Communication improvement

**Network:**
- Connect with other developers
- Mentorship opportunities
- Job referrals
- Conference invitations

**Make contributions count:**
- Focus on quality over quantity
- Solve real problems
- Document your work
- Help others learn

## Summary for Developers

| Action | Allowed? | Requirements |
|--------|----------|-------------|
| Contributing code | ✅ Yes | Must be AGPL-3.0 |
| Contributing docs | ✅ Yes | Must be CC-BY-SA-4.0 |
| Forking VIRENS | ✅ Yes | Fork stays AGPL-3.0 |
| Creating plugins | ✅ Yes | Plugins must be AGPL |
| Using as library | ✅ Yes | Your code becomes AGPL |
| Proprietary extensions | ❌ No | AGPL prohibits this |
| Offering as service | ✅ Yes | Must share source code |
| Removing features | ✅ Yes | Modified version still AGPL |
| Commercial use | ✅ Yes | Follow AGPL requirements |

## Resources for Developers

**Legal:**
- [GNU AGPL-3.0 Full Text](https://www.gnu.org/licenses/agpl-3.0.html)
- [GNU AGPL FAQ](https://www.gnu.org/licenses/gpl-faq.html)
- [SPDX License List](https://spdx.org/licenses/)

**Technical:**
- [CONTRIBUTING.md](../../CONTRIBUTING.md)
- [GitHub Repository](https://github.com/preterite/virens)
- [Issue Tracker](https://github.com/preterite/virens/issues)

**Community:**
- Discord/Forum links
- Developer mailing list
- Monthly contributor calls

## Still Have Questions?

- Read the [FAQ](faq.md)
- Review [License Explained](license-explained.md)
- Ask in GitHub Discussions
- Email developer: licensing@virens.io

**Bottom line:** AGPL ensures VIRENS stays open. Contribute freely, fork if needed, respect the license, and help build better research tools for everyone.

---

*This guide is licensed under [CC-BY-SA-4.0](../../LICENSE-DOCS)*