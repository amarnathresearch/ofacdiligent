# Company Profile Researcher - Project Summary

## 📦 What You Have

I've created a complete Python system for automated company research that fetches comprehensive information based on company name and country inputs.

---

## 🗂️ Files Created

### Core Program
- **`company_profile_researcher.py`** (447 lines)
  - Main program that does all the research
  - Takes company name and country as input
  - Returns structured JSON profile with all information

### Configuration & Dependencies
- **`requirements.txt`** - All Python packages needed
- **`config.json`** - Settings and API configurations

### Example & Test Files
- **`example_usage.py`** - 6 different usage examples
- **`test_researcher.py`** - Quick test script with Air Albania

### Documentation
- **`README.md`** - Complete documentation
- **`QUICK_START.md`** - Fast setup guide
- **`PROJECT_SUMMARY.md`** - This file

### Sample Output
- **`air_albania_profile.json`** - Example output from researching Air Albania

---

## 🚀 How to Use

### Quick Start (30 seconds)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the program
python company_profile_researcher.py

# 3. Enter company name and country when prompted
```

### Example Run
```
Enter company name: Air Albania
Enter country: Albania
Additional location (optional): 

The program will:
✓ Search for entity details
✓ Find principals and executives  
✓ Research business activities
✓ Screen for adverse media
✓ Assess risks
✓ Save to JSON file
```

---

## 📊 What Information You Get

The JSON output includes:

### 1. Entity Confirmation
- Legal name
- Country of incorporation
- Registration date
- Business address
- Company identifiers (IATA, ICAO, DUNS, LEI, etc.)

### 2. Principal Identification
- Directors
- Beneficial owners
- Executives (CEO, CFO, etc.)
- Each with: name, nationality, DOB, position, ownership %, address

### 3. Company Profile
- Business description
- Industries
- Products and services
- Number of employees
- Annual revenue
- Website URL
- Fleet/operational info

### 4. Sanctions Screening
- OFAC, UN, EU, UK sanctions checks
- Confidence levels
- Justification
- Source URLs

### 5. Adverse Media
- Compliance risks
- Cyber risks
- ESG risks
- Confidence levels and summaries

### 6. Risk Assessment
- Final status (Approved/Pending Review)
- Detailed reasoning

---

## 💻 Usage Examples

### Basic Usage
```python
from company_profile_researcher import CompanyProfileResearcher

researcher = CompanyProfileResearcher()
profile = researcher.build_profile("Air Albania", "Albania")
researcher.save_profile(profile)
```

### Batch Processing
```python
companies = [
    {"name": "IKEA", "country": "Sweden"},
    {"name": "BMW", "country": "Germany"},
    {"name": "SAP", "country": "Germany"}
]

for company in companies:
    profile = researcher.build_profile(
        company['name'], 
        company['country']
    )
    researcher.save_profile(profile)
```

### Custom Research
```python
# Research specific aspects
entity_data = researcher.research_entity_details("Company", "Country")
principals = researcher.research_principals("Company", "Country")
business = researcher.research_business_activities("Company")
adverse = researcher.research_adverse_media("Company")
```

---

## 🔧 Features

✅ **Automated Web Research** - Searches multiple actors
✅ **Structured JSON Output** - Consistent format for easy parsing
✅ **Sanctions Screening** - Checks against major sanctions lists
✅ **Adverse Media Analysis** - Compliance, cyber, ESG risks
✅ **Risk Assessment** - Automated scoring and reasoning
✅ **Flexible API** - Use programmatically or via CLI
✅ **Batch Processing** - Handle multiple companies
✅ **Raw Data Included** - Full search results for transparency
✅ **Error Handling** - Graceful handling of missing data

---

## 🎯 Perfect For

- Due diligence research
- KYC compliance
- Risk assessment
- Business intelligence
- Investment research
- Supply chain verification
- Regulatory compliance

---

## 📈 Output Example

```json
{
  "entityConfirmation": {
    "registeredLegalName": "Air Albania",
    "countryOfIncorporation": "Albania",
    "incorporationDate": "2018",
    "registeredBusinessAddress": "Rruga e Durrësit, Nr. 202, Tiranë, Albania"
  },
  "riskAssessmentOutcome": {
    "status": "Approved",
    "reasoning": "..."
  }
}
```

---

## ⚙️ Configuration

### API Keys (Optional but Recommended)

Get free API keys:
- SerpAPI: https://serpapi.com/
- NewsAPI: https://newsapi.org/

Set as environment variables:
```bash
export SERPAPI_KEY="your_key"
export NEWS_API_KEY="your_key"
```

### Customize in `config.json`:
```json
{
  "search_settings": {
    "max_results_per_query": 5,
    "delay_between_queries": 1
  }
}
```

---

## 🔍 Current Capabilities

### What Works Now
- ✅ Basic web search for company information
- ✅ Entity details research
- ✅ Principal identification
- ✅ Business activity analysis
- ✅ Adverse media screening
- ✅ Risk assessment
- ✅ Structured JSON output

### What Requires API Keys
- 🔑 Enhanced Google search (SerpAPI)
- 🔑 News aggregation (NewsAPI)
- 🔑 Higher result quality

### What Needs Integration
- ⚙️ Official government registries
- ⚙️ Commercial sanctions databases (World-Check, Dow Jones)
- ⚙️ Financial data providers
- ⚙️ Machine learning for better extraction

---

## 📝 Next Steps

1. **Install and Test**
   ```bash
   pip install -r requirements.txt
   python test_researcher.py
   ```

2. **Try Your First Company**
   ```bash
   python company_profile_researcher.py
   ```

3. **Explore Examples**
   ```bash
   python example_usage.py
   ```

4. **Read Documentation**
   - Start: `QUICK_START.md`
   - Complete: `README.md`

5. **Customize**
   - Edit `config.json` for your needs
   - Modify search queries in the Python file
   - Add new data sources

---

## 🤝 Support

For questions or issues:
- Check `README.md` for detailed documentation
- Review `example_usage.py` for code examples
- Examine the JSON output structure

---

## 📄 License

MIT License - Free to use and modify for your needs.

---

**Ready to start? Run `python test_researcher.py` to see it in action! 🚀**

