# Machine Configurations

Each machine in your workflow gets a subdirectory with:

- `identity.json` - Machine identification (name, role, capabilities)
- `config/` - Machine-specific settings

## Example Structure
```
machines/
├── archive/              # Hub machine
│   ├── identity.json
│   └── config/
├── conservatory/         # Intel Mac workstation
│   ├── identity.json
│   └── config/
└── estuary/              # Laptop
    ├── identity.json
    └── config/
```

## Machine Roles

**Hub:**
- Runs Observatory dashboard
- Primary automation
- Central sync point

**Workstation:**
- Syncs with hub
- Full research capabilities
- May run some automation

## Usage

Machine configurations are typically created during first-time setup on each device. The install script will prompt you for machine details.
