---
title: "VIRENS Licensing FAQ"
license: "CC-BY-SA-4.0"
copyright: "(c) 2025 Mike Edwards"
---

# VIRENS Licensing FAQ

Quick answers to frequently asked questions about VIRENS licensing.

## Quick Start Questions

### Is VIRENS free?

**Yes.** VIRENS is free and open source under AGPL-3.0. No fees, ever.

### Can I use VIRENS for commercial purposes?

**Yes.** AGPL doesn't restrict commercial *use*, only creating proprietary closed-source versions.

### Do I need permission to use VIRENS?

**No.** The AGPL-3.0 license grants permission. Download and use freely.

### Can I modify VIRENS?

**Yes.** AGPL explicitly grants modification rights.

### Do I have to share my modifications?

**Only if** you offer VIRENS as a network service. Personal/internal modifications stay private.

## For Individual Users

### Can I use VIRENS for my dissertation?

**Yes, absolutely.** Free for all research use.

### Will my research outputs be open source?

**No.** AGPL covers the tool, not what you create with it. Your papers, data, and notes are yours.

### Can I use VIRENS at my job?

**Yes.** Even at for-profit companies. AGPL allows commercial use.

### What if my university requires software approval?

Show them [For Institutions](for-institutions.md). AGPL is standard open source, widely approved.

### Should I cite VIRENS in publications?

**Appreciated but not legally required.** Standard academic citation practices apply.

**Suggested citation:**
```
Edwards, Mike. (2025). VIRENS: Verdant Inquiry REsearch Notes System 
[Computer software]. https://github.com/preterite/virens
```

## For Institutions

### Can universities use VIRENS?

**Yes.** AGPL is institutional-safe. No "NonCommercial" ambiguity.

### Are there licensing fees?

**No.** AGPL is free forever. No per-user or subscription costs.

### Can we customize VIRENS?

**Yes.** Modify freely for your institution's needs.

### Must we share internal customizations?

**No.** Internal use doesn't trigger sharing requirements. Only if you offer it as a service to external users.

### What's our liability?

AGPL includes standard "no warranty" clauses. Treat like any open source software (Linux, Git, Python).

### Can we get commercial support?

**Yes.** Optional paid support available from developer or third parties.

## For Consultants

### Can I charge for VIRENS training?

**Yes.** AGPL permits commercial services. Charge freely.

### Can I offer implementation services?

**Yes.** Consulting is explicitly allowed.

### Can I create a hosted VIRENS service?

**Yes, but** you must share your source code modifications (AGPL network copyleft).

### Can I write a book about VIRENS?

**Yes.** Educational content about VIRENS is unrestricted.

### Do I need permission to consult?

**No.** AGPL grants commercial use rights. No permission or fees required.

### Can I use "VIRENS" in my business name?

**Complicated.** Trademark law (not licensing) applies. Contact developer about trademark usage.

## For Developers

### Can I contribute to VIRENS?

**Yes!** Contributions welcome. No CLA required, just submit PRs.

### What license are contributions under?

Code: AGPL-3.0, Documentation: CC-BY-SA-4.0 (same as project).

### Can I fork VIRENS?

**Yes.** Fork must stay AGPL-3.0 and credit original project.

### Can I create proprietary extensions?

**No, not really.** Extensions that incorporate VIRENS code must be AGPL.

### Can I use VIRENS code in my project?

**Yes, if** your project is AGPL-compatible. Incorporating VIRENS makes your code AGPL.

### What if I disagree with project direction?

**Fork it.** AGPL protects your ability to maintain independent versions.

## About the Licenses

### Why AGPL instead of MIT?

**AGPL ensures improvements stay open.** MIT allows anyone to create closed-source versions. AGPL prevents that.

### Why AGPL instead of GPL?

**Network copyleft.** AGPL closes the "SaaS loophole" - if you offer VIRENS as a web service, you must share code.

### Why not CC-BY-NC (NonCommercial)?

**NC is problematic:**
- Ambiguous (are universities "commercial"?)
- Blocks institutional adoption
- Not actually open source (OSI doesn't recognize it)
- Would prevent consulting/training revenue

### What's the difference between AGPL and GPL?

**AGPL = GPL + network copyleft clause.**

- GPL: Share code when you *distribute* software
- AGPL: Share code when you *distribute* OR *offer as network service*

### Why dual licensing (AGPL + CC-BY-SA)?

**Different content, different licenses:**
- Code/scripts → AGPL-3.0 (software license)
- Documentation → CC-BY-SA-4.0 (content license)

This is standard practice for projects with both code and docs.

### Is AGPL "viral"?

**Kind of, but that's the point.**

- AGPL *is* copyleft - derivatives must stay open
- But it doesn't "infect" everything you do
- Only derivative works become AGPL
- Tools that just *use* VIRENS aren't affected

### Can AGPL be changed later?

**Existing versions stay AGPL forever.** New versions could use different licenses, but:
- Would require copyright holder agreement
- Users can continue using old AGPL versions
- Can fork old version if needed

## Specific Scenarios

### I modified VIRENS for personal use. Must I share?

**No.** Personal modifications stay private. Only network service provision triggers sharing.

### My university deployed VIRENS for faculty. Must we share?

**No.** Internal deployment isn't "offering as a service" to external users.

### I built a web platform using VIRENS. Must I share?

**Yes.** Network copyleft applies. Users must be able to download your source code.

### I wrote scripts that call VIRENS. Are they AGPL?

**Probably not.** Scripts that just *execute* VIRENS commands likely aren't derivatives. But scripts that *import* VIRENS code are.

### Can I sell VIRENS?

**You can charge for services** (installation, training, support).

**You cannot** prevent others from getting VIRENS for free (it's open source).

### Can I include VIRENS in commercial software?

**Only if your software becomes AGPL too.** Incorporating AGPL code makes your project AGPL.

### I teach with VIRENS. Can I charge tuition?

**Yes.** Teaching is completely unrestricted. Charge whatever you want.

### Can I create video courses about VIRENS?

**Yes.** Educational content about VIRENS has no restrictions.

### What if I violate the license accidentally?

**Cure the violation:**
1. Stop distributing/offering service
2. Comply with requirements (share code, etc.)
3. Contact developer if uncertain

License automatically reinstates upon compliance.

### Can I get sued for violating AGPL?

**Theoretically yes, but:**
- Individual users unlikely to be targeted
- Community values collaboration over litigation
- Compliance is straightforward
- Good faith efforts respected

**Main concern:** Commercial entities creating proprietary versions.

## Technical Questions

### What's "SPDX-License-Identifier"?

Machine-readable license tag in code files:
```
SPDX-License-Identifier: AGPL-3.0-or-later
```

Enables automated license compliance checking.

### What does "or-later" mean?

`AGPL-3.0-or-later` means you can use AGPL v3.0 OR any later version.

Alternative: `AGPL-3.0-only` restricts to only version 3.0.

### How do I provide source for network services?

**Minimum compliance:**
- Prominent download link in your interface
- Complete source code
- Build instructions
- Configuration files

### Can I password-protect source downloads?

**No.** Source must be freely available to users of your service.

### What counts as "source code"?

**Everything needed to build and run:**
- All source files
- Build scripts
- Configuration files
- Installation instructions
- Documentation

**Not required:**
- User data
- Service infrastructure
- Proprietary third-party components

### Are configuration files covered by AGPL?

**Grey area.** Arguably:
- Shell scripts with logic → AGPL
- Simple config files (YAML, JSON) → Possibly not

**Safe approach:** License configs as AGPL anyway.

## Comparison Questions

### VIRENS vs. Zotero licensing?

- Zotero: AGPL-3.0 (same as VIRENS)
- Both allow commercial use
- Both require sharing modifications for services
- Both institutional-safe

### VIRENS vs. Obsidian licensing?

- Obsidian: Proprietary (free for personal use)
- VIRENS: Open source (AGPL-3.0)
- Obsidian plugins can be any license
- VIRENS extensions must be AGPL

### VIRENS vs. proprietary tools?

**VIRENS advantages:**
- Free forever
- Can modify and customize
- No vendor lock-in
- Community contributions
- Fork if project ends

**Proprietary advantages:**
- Often more polished UI
- Dedicated support team
- Regular development funding
- May have enterprise features

## Legal Questions

### Do I need a lawyer to use VIRENS?

**No.** AGPL is standard, widely-used open source license.

### What if my employer claims rights to my work?

**Check your employment contract.** AGPL doesn't override employment law.

### Can I use VIRENS in countries with restrictive laws?

**AGPL is internationally recognized.** But check local laws about:
- Encryption (if VIRENS adds encryption features)
- Data privacy (GDPR, etc. - separate from licensing)
- Export controls (unlikely for research tools)

### What's the relationship to copyright?

- **Copyright:** Mike Edwards (and contributors) own the code
- **License (AGPL):** Grants you permission to use/modify/share

You don't own VIRENS, but you have extensive rights.

### Can copyright holder change the license?

**Yes, but:**
- Only for new versions
- Existing AGPL versions stay AGPL
- All contributors must agree (for past contributions)
- Or new license only for new code (complex)

### What if multiple people contribute?

**Each contributor owns copyright on their contribution.** Combined work is "VIRENS Project" with many copyright holders.

**Git history tracks authorship.** File headers say "and contributors" collectively.

### Are there patent concerns?

**AGPL includes patent grant.** Contributors automatically grant patent rights for their contributions.

**Protects against patent trolling.**

## Procedural Questions

### Where do I find the full license text?

- **In repo:** `LICENSE` (AGPL-3.0) and `LICENSE-DOCS` (CC-BY-SA-4.0)
- **Online:** 
  - [AGPL-3.0](https://www.gnu.org/licenses/agpl-3.0.html)
  - [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/)

### How do I report license violations?

1. Document the violation
2. Contact developer: licensing@virens.io
3. Or open GitHub issue (if appropriate)
4. Allow time for compliance

**Community prefers education over enforcement.**

### Can I get written confirmation I can use VIRENS?

**The license IS your confirmation.** AGPL-3.0 grants permission explicitly.

**If your legal department needs reassurance:**
- Point to [For Institutions](for-institutions.md)
- Share [GNU AGPL FAQ](https://www.gnu.org/licenses/gpl-faq.html)
- Contact developer for specific questions

### What if I need different terms?

**Contact developer about:**
- Custom licensing arrangements
- Commercial licensing options
- Specific compliance questions
- Partnership opportunities

Currently no alternative licensing, but theoretically possible.

### How do I stay compliant?

**Checklist:**
- [ ] Keep copyright notices in files
- [ ] Include LICENSE file in distributions
- [ ] Credit original VIRENS project
- [ ] Share modifications if offering as service
- [ ] Provide source download for services
- [ ] Use AGPL for derivatives

## Philosophical Questions

### Why open source instead of proprietary?

**VIRENS values:**
- Academic openness
- Community collaboration
- No vendor lock-in
- Reproducible research
- Knowledge sharing

**Open source aligns with scholarly values.**

### Doesn't free software mean no money?

**No.** "Free" = free speech, not free beer. You may find that VIRENS
also aligns with the "free kitten" model of future caretaking.

**Revenue models that work:**
- Consulting and implementation
- Training and workshops
- Hosted services
- Support contracts
- Institutional partnerships

**Examples:** Red Hat, Automattic (WordPress), GitLab (all profitable).

### What if VIRENS becomes popular and big companies use it?

**Good!** More adoption = better tool.

**Companies must:**
- Follow AGPL requirements
- Share modifications (if offering as service)
- Credit VIRENS project

**They cannot:**
- Create closed-source proprietary versions
- Remove copyright notices
- Violate license terms

### Won't someone steal my work if I open source it?

**AGPL prevents "theft":**
- Derivatives must stay open
- Copyright protects attribution
- Community notices violations
- Forks must credit original

**Your competitive advantage:**
- First-mover benefit
- Community trust
- Deeper knowledge
- Authentic connection

## Edge Cases

### What if VIRENS incorporates proprietary components?

**Currently doesn't.** All dependencies are open source.

**If it did:** Would need separate licensing or removal of proprietary parts.

### What about AI-generated code?

**If AI generates code based on VIRENS:**
- Likely derivative work
- Should be AGPL
- But legal landscape evolving

**Err on side of caution:** Consider AI-generated VIRENS code as AGPL.

### Can I use VIRENS in classified/secret research?

**AGPL doesn't prevent classified use.**

**But consider:**
- Can you comply with sharing requirements?
- Network service provision still requires source sharing
- Local use (no service) = no sharing required

**Check with your security officer.**

### What about VIRENS in books/courses?

**Screenshots, descriptions, tutorials:** ✅ Completely unrestricted

**Copied code examples:** ⚠️ Include AGPL license notice

**Reproduced documentation:** ⚠️ Attribute under CC-BY-SA

### Can I print VIRENS documentation and sell it?

**Yes, but:**
- Documentation is CC-BY-SA
- Must include attribution
- Must license your version CC-BY-SA
- Buyers can redistribute freely

**Not a great business model** (they can get PDFs for $free).

## Still Confused?

### I read everything and I'm still uncertain.

**Next steps:**

1. Read [License Explained](license-explained.md) - Plain English overview
2. Check specific guides:
   - [For Users](for-users.md)
   - [For Institutions](for-institutions.md)
   - [For Consultants](for-consultants.md)
   - [For Developers](for-developers.md)
3. Review [GNU AGPL FAQ](https://www.gnu.org/licenses/gpl-faq.html)
4. Ask on GitHub Discussions
5. Email developer: licensing@virens.io

### My question isn't answered here.

**Ask!** We'll add it to this FAQ.

- Open a GitHub issue
- Post in discussions
- Email licensing@virens.io

### I need legal advice.

**We cannot provide legal advice.**

- These docs explain the license
- For legal questions specific to your situation, consult a lawyer
- Many law firms specialize in open source licensing

### Can you review my use case?

**For straightforward questions:** Email licensing@virens.io

**For complex situations:** 
- Consult legal counsel
- Review AGPL FAQ and docs
- Consider GitHub discussion for community input

## Summary

**Most common questions:**

| Question | Answer |
|----------|--------|
| Is it free? | ✅ Yes |
| Can I use commercially? | ✅ Yes |
| Can I modify? | ✅ Yes |
| Must I share modifications? | ⚠️ Only if offering as service |
| Can I charge for training? | ✅ Yes |
| Can I create proprietary versions? | ❌ No |
| Can institutions use it? | ✅ Yes |
| Are there fees? | ❌ No |

**When in doubt:**
- AGPL = Open source with copyleft
- Use freely, share improvements
- Commercial use allowed
- Proprietary derivatives prohibited

## Resources

**Legal:**
- [AGPL-3.0 Full Text](https://www.gnu.org/licenses/agpl-3.0.html)
- [CC-BY-SA-4.0 Full Text](https://creativecommons.org/licenses/by-sa/4.0/)
- [GNU AGPL FAQ](https://www.gnu.org/licenses/gpl-faq.html)
- [OSI License List](https://opensource.org/licenses/)

**VIRENS-specific:**
- [License Overview](index.md)
- [License Explained](license-explained.md)
- [For Users](for-users.md)
- [For Institutions](for-institutions.md)
- [For Consultants](for-consultants.md)
- [For Developers](for-developers.md)

**Community:**
- [GitHub Repository](https://github.com/preterite/virens)
- [GitHub Discussions](https://github.com/preterite/virens/discussions)
- Developer email: licensing@virens.io

---

*This FAQ is licensed under [CC-BY-SA-4.0](../../LICENSE-DOCS)*

*Last updated: 2025*