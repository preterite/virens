---
title: VIRENS License Guide for Institutions
license: CC-BY-SA-4.0
copyright: © 2025 Mike Edwards
framework/docs/legal/for-institutions.md
---

# VIRENS Licensing for Institutions

This guide addresses licensing questions for universities, research institutions, libraries, and IT departments considering VIRENS adoption.

## Executive Summary for Legal/IT

**VIRENS is open source software licensed under AGPL-3.0.**

Key points for institutional approval:

- ✅ **Free to use:** No licensing fees, per-user costs, or subscription charges
- ✅ **Real open source:** OSI-approved license, not "source available"
- ✅ **Institutional safe:** Used by thousands of organizations worldwide
- ✅ **Not "NonCommercial":** No ambiguity about commercial institutions
- ✅ **No vendor lock-in:** Standard license with established case law
- ✅ **Modification allowed:** Can customize for institutional needs
- ✅ **No "phone home":** No telemetry, tracking, or external dependencies

**Risk level:** Low. Standard AGPL carries no special institutional risks.

## Common Institutional Questions

### Is AGPL-3.0 acceptable for university use?

**Yes.** AGPL is a standard open source license approved by:
- Open Source Initiative (OSI)
- Free Software Foundation (FSF)
- Used by major projects: MongoDB (historically), GitLab, Nextcloud, many others

Thousands of universities use AGPL software without issue.

### Is our university considered "commercial" under AGPL?

**No.** Unlike CC-BY-NC (NonCommercial), AGPL has no "commercial vs. non-commercial" distinction.

AGPL restricts creating *proprietary closed-source versions*, not who can use the software.

**Your university can:**
- ✅ Use VIRENS for research
- ✅ Deploy for faculty/students
- ✅ Modify for your needs
- ✅ Use in grant-funded projects
- ✅ Use in industry partnerships

### Do we need to pay licensing fees?

**No.** AGPL is free. No per-user, per-seat, or subscription fees.

**Voluntary support:** You could contract with the developer for:
- Custom implementation services
- Priority support
- Training workshops
- Custom feature development

But the **license itself is free forever**.

### What are our obligations under AGPL?

**If you just use VIRENS:**
- Minimal obligations
- Keep copyright notices intact
- Provide copy of license to users

**If you modify VIRENS and offer it as a service:**
- Must share your modified source code
- Users must be able to download your version

**"Offer as a service" means:**
- ⚠️ You create a web-based institutional VIRENS portal
- ⚠️ You provide hosted VIRENS for other institutions

**"Offer as a service" does NOT mean:**
- ✅ IT department installs VIRENS for your faculty
- ✅ Library provides VIRENS training
- ✅ Faculty use VIRENS for research
- ✅ Students use VIRENS in courses

**For typical institutional adoption, you won't trigger sharing requirements.**

### Can we customize VIRENS for our environment?

**Yes.** AGPL explicitly permits modification.

**Examples:**
- Integrate with your SSO/LDAP
- Customize for your file server paths
- Add institution-specific templates
- Brand with university identity

**Sharing requirements:**
- If modifications stay internal (faculty/staff use only) → No sharing required
- If you offer modified VIRENS as service to external users → Must share code

### What if we want to keep customizations private?

**For internal use, you can.** AGPL sharing requirements trigger when you provide the software as a network service to others.

**Internal use = private customizations allowed.**

### Can we deploy VIRENS alongside proprietary systems?

**Yes.** AGPL doesn't "infect" other software just by running on the same system.

**Examples of safe integration:**
- VIRENS + Microsoft Exchange (proprietary email)
- VIRENS + Canvas LMS (proprietary)
- VIRENS + proprietary research database

**The boundary:** VIRENS code must stay AGPL. Systems that just *interact* with VIRENS can be proprietary.

### What about faculty/student IP rights?

**VIRENS license doesn't affect research outputs.**

- Faculty papers written using VIRENS → Faculty owns copyright
- Student dissertations created with VIRENS → Student owns copyright
- Research data managed via VIRENS → Researcher owns data

**AGPL covers the tool, not what you create with it.**

**Analogy:** Using Microsoft Word doesn't license your document under Microsoft's terms. Same principle.

### Can we include VIRENS in our "standard faculty laptop" image?

**Yes.** Pre-installing AGPL software is explicitly permitted.

### Do we need to track VIRENS usage?

**No legal requirement** from AGPL. Your institution's software policies might require tracking, but that's separate from licensing.

### Can we restrict which faculty/students use VIRENS?

**Legally (from AGPL), yes.** AGPL doesn't mandate universal access.

**Practically, why would you?** It's free. No per-user costs.

### What if a faculty member modifies VIRENS and publishes the modification?

**That's allowed and encouraged.** AGPL permits redistribution.

**The faculty member must:**
- Include AGPL license with their version
- Share source code
- Credit original VIRENS project

**The university has no liability** for faculty members' open source distributions.

### Can we create a campus-specific "VIRENS distribution"?

**Yes.** This is a normal use case.

**Example:**
- "VIRENS for BigStateU" includes:
  - University SSO integration
  - Campus file server paths
  - University branding
  - Local support contacts

**Requirements:**
- Must stay AGPL-3.0
- Must share source if offered as service to external institutions
- Must credit original VIRENS

### What's our liability if VIRENS has bugs?

**AGPL includes standard "no warranty" clauses:**

```
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
```

**This is standard for all open source.** Same as:
- Linux (GPL)
- Python (PSF License)
- Git (GPL)

**Your institution's standard software review process should apply.**

### Can we purchase commercial support?

**Not required, but available.** Developer offers:
- Implementation consulting
- Training workshops
- Custom development
- Priority support contracts

**These are optional commercial services separate from the free license.**

### How does AGPL compare to other licenses we're familiar with?

| License | Copyleft | Network Clause | Institutional Use | Commercial Use |
|---------|----------|---------------|------------------|---------------|
| **AGPL-3.0** | Yes | Yes | ✅ Allowed | ✅ Allowed |
| GPL-3.0 | Yes | No | ✅ Allowed | ✅ Allowed |
| MIT | No | No | ✅ Allowed | ✅ Allowed |
| Apache-2.0 | No | No | ✅ Allowed | ✅ Allowed |
| CC-BY-NC-SA | Yes (content) | No | ⚠️ Risky | ❌ Unclear |

**AGPL is more protective than MIT** (prevents proprietary forks) but **less restrictive than CC-BY-NC** (no commercial ambiguity).

### What if our legal department is concerned about "copyleft"?

**Copyleft affects derivative works, not use.**

**Your institution can:**
- ✅ Use AGPL software without "catching" the license
- ✅ Run AGPL alongside proprietary software
- ✅ Create proprietary research outputs using AGPL tools

**Copyleft only matters if you:**
- Create a modified version AND
- Distribute it or offer it as a service

**For normal institutional use, copyleft is not a concern.**

### Can graduate students contribute improvements back?

**Yes, encouraged.** AGPL explicitly permits contributions.

**Student contributions:**
- Student retains copyright on their code
- Contribution is licensed under AGPL (same as project)
- Student gets credit via Git history
- No additional paperwork required

**Check your institution's IP policy** - some universities claim ownership of student work.

### What happens if VIRENS changes licenses later?

**Existing versions stay AGPL.** You can continue using AGPL versions forever.

**New versions could use different licenses**, but:
- You're not required to upgrade
- AGPL allows forking if you prefer old license

**This is standard open source practice** (see: Oracle MySQL → MariaDB fork).

### Can we recommend VIRENS for grant-funded projects?

**Yes.** Major funders (NIH, NSF, NEH, Mellon) support open source tools.

Many grant programs **prefer or require** open source for reproducibility.

### What about FERPA/HIPAA/export control compliance?

**AGPL is license-neutral on data protection.**

- VIRENS doesn't transmit data externally (no "phone home")
- Data stays on your systems
- Your institution's data policies apply normally

**AGPL doesn't create or remove FERPA/HIPAA obligations.**

### Can we bundle VIRENS with proprietary institutional software?

**Yes, if:**
- They're separate programs that just interact
- You're not creating a derivative work

**Example:**
- ✅ VIRENS + proprietary citation manager (separate programs)
- ⚠️ Modified VIRENS that deeply integrates proprietary code (might be derivative)

**General rule:** If they can be installed separately and just talk via files/APIs, you're fine.

### Do we need board approval?

**Probably not.** AGPL software is typically approved at IT/legal level.

**Same approval process as:**
- Firefox
- Linux
- Git
- Python

**If your institution requires board approval for all software, that's a local policy issue, not an AGPL issue.**

### Can we get indemnification?

**Not from the license itself** - AGPL includes standard liability limitations.

**If you purchase commercial support,** indemnification could be included in that contract (separate from license).

## Comparison: AGPL vs. NC Licenses

| Factor | AGPL-3.0 (VIRENS) | CC-BY-NC-SA (Alternative) |
|--------|------------------|--------------------------|
| Institutional use | ✅ Clearly allowed | ⚠️ Ambiguous (are universities "commercial"?) |
| Legal clarity | ✅ Established case law | ⚠️ Vague "NonCommercial" definition |
| OSI approved | ✅ Yes | ❌ No (not open source) |
| Grant funder acceptance | ✅ High | ⚠️ Mixed |
| IT department comfort | ✅ Standard | ⚠️ Requires legal review |
| Can customize | ✅ Yes | ✅ Yes |
| Can redistribute | ✅ Yes | ⚠️ Only non-commercially |

**Bottom line:** AGPL is safer for institutional adoption than NC licenses.

## Recommended Institutional Path

1. **IT Review:** Treat like any open source software (Firefox, Git, Python)
2. **Legal Sign-off:** Standard AGPL, no special contracts needed
3. **Pilot Program:** Deploy for interested faculty first
4. **Training:** Optional workshops (can hire developer or run internally)
5. **Broader Rollout:** Based on pilot feedback
6. **Optional Support:** Commercial support contract if desired

**Timeline:** Approval typically 2-4 weeks (comparable to other open source).

## For IT Directors

**VIRENS is standard open source:**
- No vendor lock-in or proprietary dependencies
- No licensing server or phone-home requirements
- No per-user costs or true-ups
- Standard AGPL-3.0 license (thousands of precedents)
- Can be forked if project direction changes

**Deployment:**
- macOS focused (matches higher ed preference)
- Shell scripts and Python (standard tools)
- No server infrastructure required (desktop application)
- Optional cloud sync via user's own storage

**Support:**
- Community support via GitHub
- Optional paid support from developer
- Can hire third-party consultants (AGPL allows this)

## For Provosts / Research Officers

**Strategic benefits:**
- ✅ Modern research infrastructure (aligns with digital humanities initiatives)
- ✅ Open source (supports open scholarship values)
- ✅ Zero licensing costs (redirects budget to other priorities)
- ✅ Customizable (can adapt to institutional needs)
- ✅ Supports grant mandates for reproducibility
- ✅ Faculty control their own workflows (not vendor-dependent)

**Risks:**
- ⚠️ Lower (no vendor lock-in, can fork if needed)
- ⚠️ Less hand-holding than commercial software (but more control)
- ⚠️ Requires technical comfort (command line, git)

**Comparable to:**
- R/RStudio adoption (hugely successful in academia)
- Zotero adoption (standard in humanities)
- Git adoption (universal in research)

## Legal Checklist

Use this for your institution's approval process:

- [ ] AGPL-3.0 license reviewed and approved
- [ ] No "NonCommercial" ambiguity concerns
- [ ] Modification rights confirmed
- [ ] No vendor lock-in or proprietary dependencies
- [ ] No per-user licensing costs
- [ ] Data stays on institutional systems (no external transmission)
- [ ] Compatible with grant requirements
- [ ] Standard open source warranty disclaimers noted
- [ ] Optional commercial support available if needed
- [ ] Institutional IP policy reviewed for any conflicts

## Still Have Questions?

- Review [License Explained](license-explained.md)
- See [FAQ](faq.md)
- Contact developer: licensing@virens.io
- Request consultation for large deployments

**We want to help your institution succeed with VIRENS.**

---

*This guide is licensed under [CC-BY-SA-4.0](../../LICENSE-DOCS)*