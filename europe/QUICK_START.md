# Quick Start Guide - Company Profile Researcher

## 🚀 Getting Started in 3 Steps

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Run the Program

**Option A: Interactive Mode**
```bash
python company_profile_researcher.py
```

Then enter:
- Company name (e.g., "Air Albania")
- Country (e.g., "Albania")

**Option B: Test Mode**
```bash
python test_researcher.py
```

This will automatically test with Air Albania as an example.

**Option C: Use in Your Code**
```python
from company_profile_researcher import CompanyProfileResearcher

researcher = CompanyProfileResearcher()
profile = researcher.build_profile("Air Albania", "Albania")
researcher.save_profile(profile)
```

### Step 3: Check the Output

The program creates a JSON file with the company profile:
- `[company_name]_profile.json` - Main profile
- `test_output.json` - Output from test script

---

## 📋 Example Input/Output

### Input
```
Company: Air Albania
Country: Albania
```

### Output
File: `air_albania_profile.json`

Contains:
- ✅ Entity confirmation (legal name, registration)
- ✅ Principal identification (directors, executives)
- ✅ Business activities (products, services, revenue)
- ✅ Sanctions screening results
- ✅ Adverse media analysis
- ✅ Risk assessment

---

## 🎯 Common Use Cases

### Use Case 1: Research a Single Company
```bash
python company_profile_researcher.py
# Enter company name and country when prompted
```

### Use Case 2: Batch Process Multiple Companies
See `example_usage.py` - Example 5

### Use Case 3: Integrate into Your System
```python
from company_profile_researcher import CompanyProfileResearcher

researcher = CompanyProfileResearcher()
profile = researcher.build_profile("Company Name", "Country")

# Access specific data
status = profile['riskAssessmentOutcome']['status']
executives = profile['principalIdentification']['executives']
```

---

## 🔑 Optional: API Keys for Enhanced Search

To get better search results, you can add API keys:

1. Get SerpAPI key: https://serpapi.com/ (free tier available)
2. Get NewsAPI key: https://newsapi.org/ (free tier available)
3. Set environment variables:
```bash
export SERPAPI_KEY="your_key_here"
export NEWS_API_KEY="your_key_here"
```

Or edit `config.json`:
```json
{
  "api_keys": {
    "serpapi_key": "your_key_here",
    "news_api_key": "your_key_here"
  }
}
```

---

## 📁 Files in This Package

| File | Description |
|------|-------------|
| `company_profile_researcher.py` | Main program |
| `test_researcher.py` | Quick test script |
| `example_usage.py` | Multiple usage examples |
| `requirements.txt` | Python dependencies |
| `config.json` | Configuration file |
| `README.md` | Full documentation |
| `QUICK_START.md` | This file |

---

## ⚠️ Important Notes

1. **Free Tier Limits**: Without API keys, the program uses basic search which may be slower and less comprehensive
2. **Rate Limiting**: The program includes delays between searches to respect API limits
3. **Manual Verification**: Results should be verified against official sources for critical business decisions
4. **Data Limitations**: Some information (like full executive rosters, financials) may not be publicly available

---

## 🐛 Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### No results found
- Check your internet connection
- Verify the company name spelling
- Try adding more location details
- Consider adding API keys for better search

### Slow performance
- This is normal - the program searches multiple sources
- Consider adding API keys to speed up searches

---

## 📞 Next Steps

1. ✅ Run the test script to verify everything works
2. ✅ Try your first company research
3. ✅ Read `example_usage.py` for advanced usage
4. ✅ Check `README.md` for complete documentation

Happy researching! 🎉

