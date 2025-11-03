## Profile Fetcher

Fetches rich profiles for people (politicians, actors, celebrities, company directors, etc.) from Wikidata and Wikipedia, including relatives with their relationship type and short bios.

### Setup

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### Usage

```bash
python profile_fetcher.py "Full Name" [occupation]

# Examples
python profile_fetcher.py "Brad Pitt" actor
python profile_fetcher.py "Elon Musk"
```

If the initial Wikidata search does not find a candidate, the tool automatically:
- searches Wikipedia to resolve the best page and its Wikidata `Q` identifier
- falls back to DuckDuckGo Instant Answer to find a Wikipedia page when needed

### Output

- Pretty-printed profile in the console
- JSON block that includes:
  - identifiers, description
  - birth/death details
  - nationalities
  - family (spouses, children, father, mother, siblings)
  - relatives (with relationship type and shortBio)
  - education
  - career (occupations, employers, parties, positions, memberships, affiliations)
  - links (Wikidata/Wikipedia/Commons)

### Notes

- Source data completeness depends on Wikidata/Wikipedia.
- Relatives’ short bios prefer Wikipedia summaries, with a Wikidata description fallback.

