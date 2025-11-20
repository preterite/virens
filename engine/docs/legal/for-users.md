---
title: VIRENS License Guide for Users
license: CC-BY-SA-4.0
copyright: "(c) 2025 Mike Edwards
framework/docs/legal/for-users.md
---

# VIRENS Licensing for Users

This guide answers licensing questions for individual researchers using VIRENS.

## The Short Answer

**Yes, you can use VIRENS for free, forever, for any research purpose.**

The AGPL-3.0 license grants you:
- ✅ Free personal use
- ✅ Free academic use
- ✅ Freedom to modify for your workflow
- ✅ Freedom to share with colleagues

**No fees. No registration. No restrictions.**

## Common User Questions

### Can I use VIRENS for my dissertation?
**Yes, absolutely.** AGPL-3.0 permits all research use.

### Do I need to pay if I'm using it professionally?
**No.** "Professional use" (you're a professor, researcher, graduate student) is free. AGPL doesn't restrict commercial *use* - only creating proprietary closed-source versions.

### Can I modify VIRENS scripts for my workflow?
**Yes.** AGPL explicitly grants modification rights. Your personal modifications are yours.

### Do I have to share my modifications?
**Only if** you run modified VIRENS as a service for others. Personal modifications stay private.

**Examples:**
- ✅ You customize Obsidian integration for your vault → Private
- ✅ You create personal Hazel rules → Private  
- ⚠️ You create a web service where others use your modified VIRENS → Must share code

For individual research use, you never need to share.

### Can I use VIRENS at a for-profit company?
**Yes.** You work at a pharmaceutical company doing research? Fine. Private equity firm doing analysis? Fine.

AGPL allows use at for-profit entities. The restriction is on creating *proprietary derivatives*, not on who uses it.

### What if my institution requires proprietary software agreements?
**AGPL is not proprietary.** It's open source. Your institution's IT should approve it like they approve:
- Firefox (open source)
- Python (open source)
- Git (open source)
- R/RStudio (open source)

If they balk, show them [For Institutions](for-institutions.md).

### Can I put VIRENS-generated outputs in my published papers?
**Yes, of course.** Your research outputs are yours. AGPL covers the tool, not what you create with it.

**Analogy:** You use R (GPL license) for analysis. You don't license your paper under GPL. Same here.

### Should I cite VIRENS in my publications?
**Appreciated but not legally required.** Academic citation is separate from licensing.

**Suggested citation:**
```
Edwards, Mike. (2025). VIRENS: Verdant Inquiry Research Environment 
for Scholars [Computer software]. https://github.com/preterite/virens
```

### Can I teach VIRENS workflows in my class?
**Yes.** Both teaching and students using it are permitted.

### Can I share my VIRENS configuration with labmates?
**Yes.** AGPL explicitly allows redistribution.

**Note:** Don't share your *personal data* (your Obsidian vault contents, bibliography, private configs). Share the *framework*.

### What about the documentation license (CC-BY-SA)?
**For users:** This mainly affects if you copy/republish documentation.

**Examples:**
- ✅ Reading guides → No restrictions
- ✅ Following tutorials → No restrictions
- ✅ Printing for personal reference → Fine
- ⚠️ Copying tutorial into your course materials → Must attribute
- ⚠️ Adapting guide for your blog → Must attribute and share under CC-BY-SA

### I'm on a proprietary platform (Windows, macOS). Can I still use VIRENS?
**Yes.** AGPL doesn't require open source *operating systems*, only that VIRENS code stays open.

macOS is the primary VIRENS platform.

### Can I create closed-source plugins for VIRENS?
**No, not really.** If your plugin is a derivative work (incorporates VIRENS code, links with VIRENS libraries), it must be AGPL.

If it's a completely independent tool that just *interacts* with VIRENS (via APIs, files, etc.), it can be separate.

**Grey area.** Ask if unsure.

### What if I want to commercialize my VIRENS-based workflow?
**Depends:**

- ✅ Selling services (consulting, training, support) → Allowed
- ✅ Creating content about VIRENS (courses, books) → Allowed
- ❌ Selling closed-source modified VIRENS → Not allowed
- ⚠️ Offering hosted VIRENS service → Allowed but must share code

See [For Consultants](for-consultants.md) for details.

### Can I request features or report bugs?
**Yes!** Open a GitHub issue. No license implications.

### What happens if I violate the license?
**Practically:** For personal/academic use, unlikely to be an issue. VIRENS is about community, not litigation.

**Legally:** License terminates, you'd need to stop using VIRENS unless you cure the violation.

**Realistically:** The main concern is commercial entities creating proprietary versions. Individual researchers aren't the target.

### Can I use VIRENS if my employer has IP assignment clauses?
**Check your employment contract.** Some employers claim rights to everything you create. AGPL doesn't override employment law.

**Likely fine if:**
- You created personal configs on personal time/equipment
- Your employer doesn't claim ownership of your research tools

**Ask your employer if unsure.**

### What's the relationship between copyright and licensing?
- **Copyright:** Mike Edwards (and contributors) own the code
- **License (AGPL):** Grants you permission to use/modify/share

You don't own VIRENS (copyright), but you have extensive rights (license).

### Do I need a lawyer to use VIRENS?
**No.** AGPL is a standard, widely-used open source license. Thousands of projects use it.

If your institution's legal department has questions, point them to:
- [GNU AGPL FAQ](https://www.gnu.org/licenses/gpl-faq.html)
- [For Institutions](for-institutions.md)

## Summary Table

| Scenario | Allowed? | Notes |
|----------|----------|-------|
| Personal research use | ✅ Yes | Free, no restrictions |
| Institutional use | ✅ Yes | No fees |
| Modify for personal use | ✅ Yes | Modifications stay private |
| Share with colleagues | ✅ Yes | Share framework, not personal data |
| Teach in courses | ✅ Yes | No permission needed |
| Use at for-profit company | ✅ Yes | Using ≠ creating proprietary version |
| Publish papers using VIRENS | ✅ Yes | Your outputs are yours |
| Create proprietary derivative | ❌ No | Must stay open source |
| Offer VIRENS as paid service | ⚠️ Conditional | Must share modified code |

## Still Unsure?

- Read the [FAQ](faq.md)
- Review [License Explained](license-explained.md)
- Ask on GitHub Discussions
- Email licensing@virens.io

**Bottom line:** If you're doing normal research, you're fine. Use VIRENS, modify it, enjoy it.

---

*This guide is licensed under [CC-BY-SA-4.0](../../LICENSE-DOCS)*
