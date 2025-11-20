---
title: "VIRENS Licenses Explained"
license: "CC-BY-SA-4.0"
copyright: "(c) 2025 Mike Edwards"
---

# VIRENS Licenses Explained

This page provides plain-English explanations of VIRENS licensing without legal jargon.

## The Two Licenses

VIRENS uses **two different licenses** for different types of content:

### 1. AGPL-3.0 (for Code)

**What is it?** A strong "copyleft" license from the Free Software Foundation.

**Plain English:**
- You can use, modify, and share VIRENS code freely
- If you change the code and offer it as a service (web app, hosted platform), you must share your changes
- You cannot create closed-source proprietary versions
- Commercial use is allowed (you can charge for services)

**Think of it as:** "Use freely, but keep improvements open"

**The key difference from MIT:** MIT lets anyone take the code and close it. AGPL requires sharing improvements.

**The key difference from GPL:** GPL's sharing requirement only triggers on distribution. AGPL's triggers on network use too (prevents "SaaS loophole").

### 2. CC-BY-SA-4.0 (for Documentation)

**What is it?** Creative Commons license for educational and creative works.

**Plain English:**
- You can copy, share, and adapt the documentation
- You must give credit (attribution) when using it
- If you create derivatives, they must use the same license
- Perfect for academic citation practices

**Think of it as:** "Cite your sources" made official

## Why Two Licenses?

**Different content, different needs:**

| Type | License | Reason |
|------|---------|--------|
| Shell scripts, Python code, automation | AGPL-3.0 | Protects code improvements |
| User guides, tutorials, explanations | CC-BY-SA-4.0 | Standard for education |

**Real-world example:**
- Someone improves the Obsidian integration script → They must share (AGPL)
- Someone writes a blog post about VIRENS workflows → They must attribute (CC-BY-SA)

## Common Scenarios

### "I want to use VIRENS for my dissertation research"
✅ **Allowed.** Free, no restrictions. Both licenses permit personal use.

### "Can my university IT department deploy VIRENS for our faculty?"
✅ **Allowed.** AGPL permits institutional use. IT doesn't need to share code unless they modify VIRENS and run it as a service for others.

### "I want to offer VIRENS workshops and charge $500 per participant"
✅ **Allowed.** AGPL permits commercial services. You don't need permission.

### "I want to fork VIRENS and add new features"
✅ **Allowed.** Your fork must stay AGPL-3.0 (open source).

### "I want to use VIRENS code in my proprietary research tool"
❌ **Not allowed.** AGPL requires derivatives to stay open source.

### "I want to quote VIRENS documentation in my book"
✅ **Allowed.** Just provide attribution: "Adapted from VIRENS documentation (CC-BY-SA-4.0)"

### "I want to create a SaaS platform based on VIRENS"
⚠️ **Allowed, but...** You must share your modified source code. AGPL's network copyleft clause requires this.

## The Academic Open Source Ethos

VIRENS licensing reflects academic values:

1. **Knowledge should be free** → Code and docs are free forever
2. **Build on others' work** → Modification and forking allowed
3. **Cite your sources** → Attribution required (CC-BY-SA)
4. **Share improvements** → Changes stay open (AGPL)
5. **No gatekeeping** → Anyone can use, teach, or consult

## What Happens to Contributions?

When you contribute to VIRENS:
- Your code becomes AGPL-3.0 (same as the project)
- Your documentation becomes CC-BY-SA-4.0 (same as the project)
- You retain copyright on your contribution
- Git history preserves your authorship
- You grant VIRENS project the right to use your contribution under these licenses

**No signing required.** Submitting a pull request = agreement.

## Comparison with Other Licenses

| License | Code Protection | Requires Sharing | Allows Proprietary Forks | Institutional Safe |
|---------|----------------|------------------|------------------------|-------------------|
| **AGPL-3.0** (VIRENS) | Strong | Yes (including services) | No | Yes |
| GPL-3.0 | Strong | Yes (on distribution) | No | Yes |
| MIT | Minimal | No | Yes | Yes |
| CC-BY-NC-SA | N/A (not for code) | Yes | No | **Risky** |

**Why not MIT?** We want improvements to benefit everyone.

**Why not CC-BY-NC?** NC (NonCommercial) blocks institutional adoption and is vague.

**Why not GPL?** AGPL closes the "SaaS loophole" for modern cloud services.

## Further Reading

- [For Users](for-users.md) - Detailed Q&A for researchers
- [For Institutions](for-institutions.md) - Legal considerations for universities
- [For Consultants](for-consultants.md) - Commercial service guidelines
- [For Developers](for-developers.md) - Contributing and forking
- [FAQ](faq.md) - Quick answers

---

*This guide is licensed under [CC-BY-SA-4.0](../../LICENSE-DOCS)*
