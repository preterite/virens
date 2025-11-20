# VIRENS

**Verdant Inquiry REsearch Notes System**

An open-source academic research workflow system for humanities scholars.

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](LICENSE)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](LICENSE-DOCS)

---

## Quick Start
```bash
# Clone VIRENS framework
git clone https://github.com/preterite/virens ~/Local/virens/virens

# Run installation
cd ~/Local/virens/virens
./engine/install.sh
```

See [Installation Guide](engine/docs/getting-started/installation.md) for details.

---

## What is VIRENS?

VIRENS is a modular framework that integrates macOS applications into a unified scholarly workflow:

- **Research**: Obsidian, Bookends, DEVONthink, Scrivener, Pandoc
- **Tasks**: Things 3
- **Automation**: Hazel, Keyboard Maestro, Shortcuts, Typinator
- **Capture**: Drafts, Highlights, Readwise, Just Press Record
- **Discovery**: Alfred, Hookmark
- **Communication**: Apple Mail/Calendar/Contacts
- **Observatory**: Academic metrics tracking and analytics
- **Health**: System monitoring and maintenance

---

## Directory Structure

After installation, you'll have:
```
~/Local/virens/
├── virens/                      # VIRENS framework (this repository)
│   ├── .git/                    # Framework repository
│   └── engine/                  # Infrastructure + Framework + Template
│       ├── infrastructure/      # Kernel layer
│       ├── framework/           # Modular tools
│       ├── template/            # User scaffold (User0)
│       ├── docs/                # Documentation
│       └── install.sh           # Installation script
│
└── user1/                       # Your research environment (created by install.sh)
    ├── .git/                    # Your private repository
    ├── config/                  # Your configurations
    ├── dotfiles/                # Your shell configs
    ├── obsidian-vault/          # Your research notes
    └── observatory/             # Your academic metrics
```

**Important:** The `user1/` directory is your private research data with its own separate Git repository. It is **NOT** part of the VIRENS framework repository. Keep them separate!

---

## Two Repositories, Two Purposes

### 1. VIRENS Framework (~/Local/virens/virens/)
- **Purpose:** The shared framework that runs VIRENS
- **Repository:** https://github.com/preterite/virens (public)
- **Updates:** Run `virens-update` to get new features
- **You contribute:** Via pull requests to improve VIRENS

### 2. Your User Instance (~/Local/virens/user1/)
- **Purpose:** Your personal research data and configurations
- **Repository:** Your own private Git repository (optional)
- **Updates:** You control this completely
- **You manage:** Push to your own private GitHub/GitLab remote

These are **completely separate Git repositories**. Your private data in `user1/` will never be committed to the public VIRENS repository.

---

## License

VIRENS is dual-licensed to maximize freedom while protecting the open-source nature of the project:

### Code License: AGPL-3.0

All executable code, scripts, automation, and modules are licensed under the [GNU Affero General Public License v3.0](LICENSE).

**This means you can:**
- ✅ Use VIRENS for personal research (free forever)
- ✅ Use VIRENS at your institution (no fees)
- ✅ Modify and customize for your needs
- ✅ Share improvements with the community
- ✅ Offer consulting/training services

**You must:**
- 📋 Keep the license notices intact
- 🔓 Share modifications if you offer VIRENS as a network service
- 🔄 Use the same license (AGPL-3.0) for derivative works

**You cannot:**
- ❌ Make proprietary closed-source versions
- ❌ Remove attribution or license information

### Documentation License: CC-BY-SA 4.0

All written documentation, tutorials, guides, and explanations are licensed under the [Creative Commons Attribution-ShareAlike 4.0 International License](LICENSE-DOCS).

**This means you can:**
- ✅ Share and adapt the documentation
- ✅ Use it for teaching and training
- ✅ Translate it to other languages

**You must:**
- 📖 Provide attribution to VIRENS
- 🔄 Share adaptations under the same license

---

## Understanding the Licenses

**New to open-source licensing?** We've created comprehensive guides:

- **[License Overview](engine/docs/legal/index.md)** - Start here
- **[Plain English Explanation](engine/docs/legal/license-explained.md)** - What AGPL means in practice
- **[For Individual Users](engine/docs/legal/for-users.md)** - Can I use this for free?
- **[For Institutions](engine/docs/legal/for-institutions.md)** - Can my university adopt this?
- **[For Consultants](engine/docs/legal/for-consultants.md)** - Can I offer VIRENS training?
- **[For Developers](engine/docs/legal/for-developers.md)** - Can I contribute? Can I fork?
- **[FAQ](engine/docs/legal/faq.md)** - Common questions answered

**Quick answer for most people:** Yes, you can use VIRENS freely for academic research. The AGPL license protects the open-source nature of the project—it doesn't restrict personal or institutional use.

---

## Documentation

- [Getting Started](engine/docs/getting-started/)
- [Module Reference](engine/docs/reference/)
- [User Guides](engine/docs/guides/)
- [Development](engine/docs/development/)

---

## Community

- **Issues & Bug Reports**: [GitHub Issues](https://github.com/preterite/virens/issues)
- **Discussions**: [GitHub Discussions](https://github.com/preterite/virens/discussions)
- **Website**: [virens.io](https://virens.io)
- **Philosophy**: [verdantinquiry.org](https://verdantinquiry.org)

---

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for:

- Code of Conduct
- How to submit issues and pull requests
- Development setup instructions
- Coding standards

By contributing, you agree that your contributions will be licensed under:
- **Code contributions**: AGPL-3.0
- **Documentation contributions**: CC-BY-SA 4.0

---

## Citation

If you use VIRENS in your research, please cite:
```bibtex
@software{virens2025,
  author = {Mike Edwards},
  title = {VIRENS: Verdant Inquiry REsearch Notes System},
  year = {2025},
  url = {https://github.com/preterite/virens},
  version = {1.0.0}
}
```

---

## Support

VIRENS is free and open-source software maintained by scholars, for scholars.

If you find VIRENS valuable, consider:
- ⭐ Starring the repository
- 📢 Sharing with colleagues
- 📝 Contributing documentation or code
- 💬 Participating in discussions

---

**Built with ❤️ by the academic community**
