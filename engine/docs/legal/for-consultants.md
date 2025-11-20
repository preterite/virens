---
title: "VIRENS License Guide for Consultants"
license: "CC-BY-SA-4.0"
copyright: "(c) 2025 Mike Edwards"
---

# VIRENS Licensing for Consultants

This guide addresses licensing questions for consultants, trainers, and service providers offering VIRENS-related commercial services.

## Executive Summary

**Yes, you can offer commercial VIRENS services.**

AGPL-3.0 explicitly permits commercial use including:
- ✅ Paid training and workshops
- ✅ Implementation consulting
- ✅ Custom configuration services
- ✅ Priority support contracts
- ✅ Content creation (courses, books, videos)

**The only restriction:** If you modify VIRENS and offer it as a hosted service, you must share your source code modifications.

**No permission required. No licensing fees. No restrictions on charging.**

## Common Consultant Questions

### Can I charge for VIRENS training workshops?

**Yes, absolutely.** AGPL permits commercial training services.

**You can:**
- Offer paid workshops ($500-2,000+ per participant)
- Run bootcamps and certification programs
- Create online courses (Udemy, Teachable, etc.)
- Sell video tutorials
- Charge for one-on-one coaching

**You must:**
- Not misrepresent yourself as "official" VIRENS (unless authorized)
- Not remove copyright notices from VIRENS materials
- Attribute documentation if you directly copy/adapt it (CC-BY-SA requirement)

**You don't need to:**
- Ask permission from the developer
- Pay licensing fees or royalties
- Share your training materials (they're yours)

### Can I offer VIRENS implementation services?

**Yes.** Implementation consulting is explicitly permitted.

**Services you can offer:**
- Initial setup and configuration
- Custom workflow design
- Integration with institutional systems
- Data migration from other tools
- Ongoing support and maintenance

**Typical rates:** $125-250/hour for humanities computing consultants with PhDs.

**Project-based pricing:** $5,000-15,000 for full institutional implementations.

### What if I modify VIRENS for a client?

**Depends on how you deliver it:**

**Scenario 1: Local installation for client**
- You modify VIRENS for their specific needs
- You install it on their systems
- They run it locally (not as a service to others)
- **Result:** ✅ No sharing required (internal use)

**Scenario 2: You host modified VIRENS as a service**
- You modify VIRENS and run it on your servers
- Multiple clients access your modified version via web/network
- **Result:** ⚠️ You must share your source code modifications

**The key distinction:** Distribution vs. network service provision.

### Can I create a "VIRENS as a Service" platform?

**Yes, but with requirements.**

**What you can do:**
- Build a hosted/managed VIRENS service
- Charge subscription fees
- Offer it commercially

**What you must do:**
- Share your modified VIRENS source code (AGPL network copyleft)
- Provide download access to users
- Keep modifications under AGPL-3.0

**Business model implications:**
- Your service differentiation comes from hosting, support, and ease-of-use
- Not from proprietary code
- Similar to how GitLab offers hosted Git service (AGPL code, commercial service)

**Example services that work:**
- "VIRENS Cloud" - hosted environment with backups and support
- "VIRENS for Teams" - multi-user collaboration features
- "VIRENS Premium" - priority support and advanced training

### Can I create proprietary add-ons or plugins?

**Generally no, but there are exceptions.**

**If your add-on:**
- Incorporates VIRENS code → Must be AGPL
- Links with VIRENS libraries → Must be AGPL
- Modifies core VIRENS functionality → Must be AGPL

**If your add-on:**
- Is completely independent code that just *interacts* via files/APIs → Can be proprietary
- Example: A separate GUI app that reads VIRENS data files → Potentially proprietary

**Grey area.** The safest approach:
- Make plugins AGPL-3.0 (builds community, reduces legal risk)
- Charge for your services, not the code

### Can I write a book about VIRENS and sell it?

**Yes, absolutely.** Educational content about VIRENS is completely unrestricted.

**You can:**
- Write and sell books
- Create paid video courses
- Publish tutorials and guides
- Sell templates and configurations

**You must:**
- Attribute VIRENS documentation if you directly copy it (CC-BY-SA)
- Not misrepresent yourself as the official VIRENS project

**Your original content:** You own the copyright. License it however you want.

### What about NDA restrictions with clients?

**AGPL creates tension with NDAs.**

**The issue:**
- Client wants NDA on your VIRENS modifications
- AGPL requires you to share modifications (if running as service)

**Solutions:**

**Option 1: Local deployment (no sharing required)**
- Install VIRENS on client's systems
- They run it internally
- Your modifications stay private under NDA
- ✅ This works - no conflict

**Option 2: Open source modifications**
- Explain AGPL requirements to client
- Share modifications publicly (as required)
- NDA covers your business processes, not code
- ⚠️ Requires client education

**Option 3: Commercial licensing**
- Contact VIRENS developer about commercial licensing
- Could enable proprietary modifications
- Would require separate agreement
- Currently not offered, but theoretically possible

**Best practice:** Be upfront about AGPL requirements before signing NDAs.

### Can I compete with the original VIRENS developer?

**Yes.** AGPL doesn't grant monopoly rights.

**You can:**
- Offer better training
- Provide superior support
- Charge lower (or higher) rates
- Target different markets
- Build reputation in your niche

**Competition is healthy.** It:
- Improves service quality
- Expands VIRENS adoption
- Benefits the academic community

**How to compete ethically:**
- Don't misrepresent yourself as "official"
- Don't badmouth the original project
- Consider contributing improvements back
- Build reputation through quality service

### What if I want to create a fork with a different name?

**Allowed under AGPL.**

**Requirements:**
- Fork must stay AGPL-3.0
- Credit original VIRENS project
- Can't remove copyright notices
- Must share your source code

**Example:** "AcademicFlow" (based on VIRENS)
- Clearly state it's a VIRENS fork
- List your modifications
- Keep AGPL license
- Provide source code

**Strategic consideration:** Forking creates maintenance burden. Contributing improvements to main project often better.

### Can I use "VIRENS" in my business name?

**Complicated. Trademark law applies, not licensing.**

**Currently:**
- "VIRENS" may become trademarked
- Using "VIRENS" in business name could require permission
- AGPL covers code, not trademarks

**Safe approaches:**
- "[Your Name] VIRENS Consulting"
- "VIRENS Training by [Company]"
- "Certified VIRENS Services" (if certification program exists)

**Risky:**
- "VIRENS Inc." (implies official entity)
- "VIRENS Pro" (implies endorsed version)

**Best practice:** Contact developer about trademark usage guidelines.

### What about certifications and credentials?

**Currently no official certification program.**

**You can:**
- Describe your VIRENS expertise honestly
- List it as a skill/specialization
- Provide references/testimonials
- Demonstrate knowledge through content

**You cannot:**
- Create fake "VIRENS Certified" credentials
- Imply official endorsement without authorization

**Future possibility:** Developer may create certification program. Respect it if implemented.

### Do I need to contribute improvements back?

**Only if running as a service (network copyleft).**

**Local installations for clients:** No contribution requirement.

**Hosted services:** Must share source, but:
- You choose *when* to share (upon user request)
- No requirement to contribute to main project
- Can maintain separate fork

**Ethical consideration:** Contributing back:
- Builds community goodwill
- Reduces your maintenance burden (upstream maintains it)
- Enhances your reputation
- Improves VIRENS for everyone

**Strategic advantage:** Being known as a contributor helps your consulting business.

### Can I offer proprietary "premium features"?

**Not if they modify VIRENS code.**

**What doesn't work:**
- Closed-source VIRENS extensions
- Proprietary modules that link to VIRENS
- Modified VIRENS with added restrictions

**What does work:**
- Premium *services* (support, hosting, training)
- Proprietary tools that *integrate* with VIRENS (if truly separate)
- Exclusive access to your training materials
- Priority support contracts

**The pattern:** Charge for your time/expertise, not for proprietary code.

### What if my client wants proprietary modifications?

**Educate them on alternatives:**

**Option 1: Private modifications (local use)**
- Install VIRENS locally at client site
- Modifications stay private (no service provision)
- ✅ No AGPL conflict

**Option 2: Public modifications**
- Share modifications as required by AGPL
- Client benefits from community improvements
- Often better long-term strategy

**Option 3: Separate proprietary tools**
- Build proprietary systems that *integrate* with VIRENS
- Keep boundary clear between AGPL and proprietary code
- Legal grey area - get advice if needed

**Education point:** Explain that open source doesn't mean "anyone can see our data" - it means the *tools* are open, not their *content*.

### How do I price my services?

**Market rates for academic consulting:**

**Hourly:**
- Entry-level (MA, new PhD): $75-100/hour
- Experienced (PhD, 3-5 years): $125-150/hour
- Senior (5-10 years): $150-200/hour
- Recognized expert: $200-300+/hour

**Project-based:**
- Small projects: $500-2,000
- Medium implementation: $2,000-10,000
- Large institutional: $10,000-50,000+

**Workshops:**
- Half-day: $1,500-3,000
- Full-day: $3,000-6,000
- Multi-day bootcamp: $10,000-25,000

**Value-based:**
- Calculate client's time savings
- Price at 5-20% of value delivered
- Example: Save institution 100 hours/year → Value $10,000 → Charge $2,000

**Retainers:**
- Ongoing support: $2,000-5,000/month
- 5-10 institutional clients at this rate = $120-300K annual revenue

### Can I subcontract or hire others?

**Yes.** AGPL doesn't restrict business structure.

**You can:**
- Hire employees
- Subcontract to other consultants
- Build a consulting firm
- Create training teams

**Ensure:**
- Subcontractors understand AGPL requirements
- Contributions are properly licensed
- Copyright attribution is correct

### What's my liability if I recommend VIRENS?

**Standard consulting liability applies.**

**AGPL includes warranty disclaimer:**
- VIRENS is provided "as-is"
- No warranty from developer

**Your liability:**
- Based on your consulting contract, not AGPL
- Professional liability insurance recommended
- Standard disclaimer: "Software provided as-is, consulting is professional advice"

**Risk mitigation:**
- Test thoroughly before recommending
- Be honest about limitations
- Document your recommendations
- Carry E&O insurance

### Can I create a SaaS competitor to VIRENS?

**Yes, if you follow AGPL.**

**Example: "ResearchCloud" (VIRENS-based SaaS)**

**Requirements:**
- Source code must be AGPL-3.0
- Users must be able to download code
- Credit VIRENS project
- Share all modifications

**Business model:**
- Compete on service quality, not proprietary code
- Offer hosting, support, integrations
- Charge for convenience and expertise

**Precedents:**
- GitLab (based on Git, AGPL/MIT)
- WordPress.com (based on WordPress, GPL)
- Nextcloud (based on ownCloud, AGPL)

**Success factors:**
- Superior hosting/reliability
- Better user experience
- Excellent support
- Additional integrations

### What about international consulting?

**AGPL is internationally recognized.**

**Considerations:**
- EU: GDPR compliance (separate from AGPL)
- Export controls: Unlikely for academic software
- VAT/tax: Consult accountant for international services
- Currency: Price in client's currency or USD

**AGPL doesn't change across borders.** Same rules apply globally.

### Can I sell VIRENS configurations/templates?

**Yes, but licensing matters.**

**If configurations are:**
- Shell scripts, Python code → Must be AGPL-3.0
- Documentation, tutorials → Should be CC-BY-SA-4.0 (or your choice)

**Business models that work:**
- Free configurations + paid implementation services
- Free basic templates + paid premium consulting
- Sell your time/expertise, not the files

**Example:**
- "VIRENS for Legal Scholars" configuration pack
- Configuration files: AGPL (free/open)
- Detailed setup guide: CC-BY-SA (free) or proprietary (paid)
- Implementation service: $2,000 (your expertise)

### Should I contribute to VIRENS development?

**Strategic benefits of contributing:**

**Reputation:**
- Recognized as expert
- Speaking opportunities
- Consulting referrals

**Technical:**
- Upstream maintains your improvements
- Less maintenance burden
- Early access to new features

**Community:**
- Networking with other consultants
- Collaborative problem-solving
- Shared best practices

**Not required, but often beneficial.**

### What if VIRENS changes licenses?

**Existing AGPL versions stay AGPL forever.**

**Scenarios:**

**New version, different license:**
- You can continue using old AGPL version
- You can fork old version (AGPL allows this)
- New version has new terms (your choice to adopt)

**Dual licensing offered:**
- Developer might offer commercial licensing option
- AGPL version remains free
- Pay for proprietary licensing if needed

**Unlikely to happen,** but AGPL protects your ability to fork if needed.

## Consulting Ethics

### Best Practices

**Be honest:**
- Don't oversell capabilities
- Acknowledge limitations
- Set realistic expectations

**Give credit:**
- Attribute VIRENS project
- Credit community contributors
- Recognize client's existing workflows

**Contribute back (when possible):**
- Share improvements
- Report bugs
- Help newcomers

**Respect licenses:**
- Follow AGPL requirements
- Don't hide obligations from clients
- Educate about open source benefits

### Building Your Consulting Practice

**Positioning:**
- "VIRENS Implementation Specialist"
- "Digital Humanities Workflow Consultant"
- "Academic Research Systems Architect"

**Marketing:**
- Blog posts demonstrating expertise
- Conference presentations
- YouTube tutorials
- GitHub contributions
- Published case studies

**Differentiation:**
- Specialized in specific disciplines (history, literature, etc.)
- Institutional expertise (R1 universities, liberal arts colleges)
- Technical focus (integration, automation, advanced features)
- Regional presence (on-campus availability)

**Pricing strategy:**
- Premium pricing for specialized expertise
- Volume discounts for consortia
- Retainers for ongoing relationships
- Value-based for transformative projects

## Summary Table

| Service | Allowed? | AGPL Requirements |
|---------|----------|------------------|
| Paid training workshops | ✅ Yes | None |
| Implementation consulting | ✅ Yes | None (if local install) |
| Hosted VIRENS service | ✅ Yes | Must share source code |
| Proprietary add-ons | ❌ Generally no | Must be AGPL if derivative |
| Selling books/courses | ✅ Yes | None (original content) |
| Custom configurations | ✅ Yes | Configs must be AGPL |
| Support contracts | ✅ Yes | None |
| Competing services | ✅ Yes | None |
| Forking VIRENS | ✅ Yes | Fork must stay AGPL |

## Resources for Consultants

**Legal:**
- [GNU AGPL FAQ](https://www.gnu.org/licenses/gpl-faq.html)
- [For Developers](for-developers.md) - Contributing guidelines
- [License Explained](license-explained.md) - Plain English

**Technical:**
- [VIRENS Documentation](https://virens.io)
- [GitHub Repository](https://github.com/preterite/virens)
- Community forums and Discord

**Business:**
- Academic consulting rate surveys
- Professional development resources
- Consulting best practices

## Still Have Questions?

- Review [FAQ](faq.md)
- Join community discussions
- Contact developer: licensing@virens.io
- Consult with lawyer for complex situations

**Bottom line:** AGPL enables consulting businesses. Charge for your expertise and services, respect the license, and help grow the VIRENS community.

---

*This guide is licensed under [CC-BY-SA-4.0](../../LICENSE-DOCS)*