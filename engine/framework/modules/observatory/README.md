# Observatory Module

**License:** [AGPL-3.0](../../../../LICENSE)

Academic metrics tracking and career analytics dashboard.

## Features

- Fetch publication data from Semantic Scholar, OpenAlex, CrossRef
- Track GitHub repository statistics
- Calculate h-index, i10-index, citation counts
- Web dashboard for visualization

## Setup
```bash
cd ~/Local/virens/virens/engine/framework/modules/observatory
pip3 install -r requirements.txt --break-system-packages
```

## Usage

The Observatory module requires configuration in your user instance:
```bash
# Configure API keys and publications
observatory-configure

# Start the web dashboard
observatory-start
```

Dashboard runs at: http://localhost:8080

## Configuration

Observatory looks for:
- **User data:** `$(virens_user)/observatory/data/observatory.db`
- **API keys:** `$(virens_user)/config/observatory.yaml`

See the [Observatory Guide](../../docs/guides/observatory-guide.md) for detailed setup instructions.

## Data Sources

- **Semantic Scholar** - Citation tracking and h-index
- **OpenAlex** - Comprehensive publication metadata
- **CrossRef** - DOI resolution and metadata
- **GitHub** - Repository statistics

## License Notice

This module is part of VIRENS and is licensed under the GNU Affero General Public License v3.0. See the [LICENSE](../../../../LICENSE) file in the repository root for the full license text.
