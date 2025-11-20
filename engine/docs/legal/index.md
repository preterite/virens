---
title: VIRENS Licensing Guide
license: CC-BY-SA-4.0
copyright: "(c) 2025 Mike Edwards
framework/docs/legal/index.md
---

# VIRENS Licensing Guide

VIRENS uses **dual licensing** to appropriately protect different types of content:

## Quick Reference

| Content Type | License | Why |
|-------------|---------|-----|
| Code (scripts, modules, automation) | [AGPL-3.0](../../LICENSE) | Ensures improvements stay open source |
| Documentation (guides, tutorials) | [CC-BY-SA-4.0](../../LICENSE-DOCS) | Standard for academic/educational content |
| Website content | CC-BY-SA-4.0 | Allows reuse with attribution |
| Website code (Jekyll themes) | MIT | Maximum compatibility |

## Understanding the Licenses

### AGPL-3.0 (Code)

The **GNU Affero General Public License v3.0** is a copyleft license that:

- ✅ Allows free use, modification, and distribution
- ✅ Permits commercial use (including consulting services)
- ✅ Requires sharing modifications if you run VIRENS as a service
- ✅ Prevents proprietary closed-source derivatives
- ✅ Protects against "SaaS loopholes" (network copyleft)

**Why AGPL over MIT?** AGPL ensures that improvements to VIRENS benefit everyone. If someone forks VIRENS and offers it as a hosted service, they must share their improvements.

**Why AGPL over GPL?** The "network copyleft" clause addresses modern cloud/web services that might otherwise avoid sharing improvements.

### CC-BY-SA-4.0 (Documentation)

The **Creative Commons Attribution-ShareAlike 4.0** license:

- ✅ Allows free sharing and adaptation
- ✅ Requires attribution when reusing
- ✅ Requires derivatives to use the same license
- ✅ Is the standard for educational and scholarly content

**Why CC-BY-SA?** It's the academic standard. When you cite a paper, you attribute the author - CC-BY-SA formalizes this for documentation.

## Detailed Guides

Choose the guide that matches your situation:

- **[For Users](for-users.md)** - "Can I use VIRENS for my research?"
- **[For Institutions](for-institutions.md)** - "Can my university adopt VIRENS?"
- **[For Consultants](for-consultants.md)** - "Can I offer VIRENS training?"
- **[For Developers](for-developers.md)** - "Can I contribute? Can I fork?"
- **[FAQ](faq.md)** - Common questions answered

## Plain English Summary

**You can:**
- Use VIRENS for free (personal, academic, commercial)
- Modify it for your needs
- Offer training and consulting services
- Fork and create derivatives

**You must:**
- Keep license notices
- Share code modifications if running as a service
- Attribute documentation when reusing
- Use the same licenses for derivatives

**You cannot:**
- Make closed-source proprietary versions
- Remove copyright/license information

## Still Have Questions?

- Read the [FAQ](faq.md)
- Open a [GitHub issue](https://github.com/preterite/virens/issues)
- Email licensing@virens.io

---

*This guide is licensed under [CC-BY-SA-4.0](../../LICENSE-DOCS)*
