# Company Profile Researcher

Automated tool to gather comprehensive company information including entity details, principals, business activities, sanctions screening, and adverse media analysis.

## Features

- **Entity Confirmation**: Company registration, legal name, incorporation details
- **Principal Identification**: Directors, executives, and beneficial owners
- **Business Profile**: Operations, financials, products, and services
- **Sanctions Screening**: Automated checks against major sanctions lists
- **Adverse Media Analysis**: Compliance, cyber, and ESG risk assessment
- **Structured JSON Output**: Ready-to-use profile in standardized format

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. (Optional) Set up API keys for enhanced search capabilities:
   - Get a SerpAPI key from https://serpapi.com/
   - Get a NewsAPI key from https://newsapi.org/
   - Set environment variables:
```bash
export SERPAPI_KEY="your_serpapi_key"
export NEWS_API_KEY="your_news_api_key"
```

## Usage

### Command Line Interface

Run the program interactively:
```bash
python company_profile_researcher.py
```

The program will prompt you for:
- Company name
- Country
- Additional location details (optional)

### Programmatic Usage

You can also use the `CompanyProfileResearcher` class in your own Python code:

```python
from company_profile_researcher import CompanyProfileResearcher

# Initialize researcher
researcher = CompanyProfileResearcher()

# Build profile
profile = researcher.build_profile(
    company_name="Air Albania",
    country="Albania"
)

# Save to file
researcher.save_profile(profile, "output.json")

# Access profile data
print(profile['entityConfirmation']['registeredLegalName'])
print(profile['riskAssessmentOutcome']['status'])
```

## Output Format

The program generates a JSON file with the following structure:

```json
{
  "entityConfirmation": {
    "registeredLegalName": "...",
    "countryOfIncorporation": "...",
    "incorporationDate": "...",
    "registeredBusinessAddress": "...",
    "companyIdentifiers": {...}
  },
  "principalIdentification": {
    "directors": [...],
    "beneficialOwners": [...],
    "executives": [...]
  },
  "companyProfileEnrichment": {
    "businessDescription": "...",
    "industries": [...],
    "coreProducts": [...],
    "numberOfEmployees": "...",
    "annualRevenue": "...",
    "websiteURL": "..."
  },
  "watchlistAndSanctionsScreening": {...},
  "adverseMediaScreening": {...},
  "riskAssessmentOutcome": {...},
  "rawResearchData": {...}
}
```

## Limitations

- **Public Data Only**: The tool relies on publicly available information from web searches
- **API Keys Required**: Enhanced features require SerpAPI and NewsAPI keys
- **Manual Verification**: Automated results should be verified against official registries
- **Rate Limiting**: Free APIs have usage limits

## Next Steps for Production Use

For production/enterprise use, consider:

1. **Official Registries**: Integrate with government business registries
2. **Commercial Databases**: Use World-Check, Dow Jones, or similar services
3. **Sanctions APIs**: Integrate with sanctions screening APIs
4. **Enhanced Parsing**: Improve information extraction from web results
5. **Machine Learning**: Use NLP/ML for better data extraction
6. **Multi-language**: Support for local language searches

## License

MIT License - feel free to modify and use as needed.

## Support

For issues or questions, please check the code comments or modify the search queries to better fit your needs.

