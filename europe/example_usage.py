"""
Example usage of Company Profile Researcher
Demonstrates different ways to use the researcher
"""

from company_profile_researcher import CompanyProfileResearcher
import json

def example_basic_usage():
    """Basic example of using the researcher"""
    print("="*60)
    print("Example 1: Basic Usage")
    print("="*60)
    
    # Create researcher instance
    researcher = CompanyProfileResearcher()
    
    # Research a company
    profile = researcher.build_profile(
        company_name="Air Albania",
        country="Albania"
    )
    
    # Display summary
    print(f"\nCompany: {profile['entityConfirmation']['registeredLegalName']}")
    print(f"Country: {profile['entityConfirmation']['countryOfIncorporation']}")
    print(f"Status: {profile['riskAssessmentOutcome']['status']}")
    
    # Save to file
    researcher.save_profile(profile, "example_output.json")
    

def example_multiple_companies():
    """Example of researching multiple companies"""
    print("\n" + "="*60)
    print("Example 2: Multiple Companies")
    print("="*60)
    
    companies = [
        {"name": "Air Albania", "country": "Albania"},
        {"name": "IKEA", "country": "Sweden"},
        {"name": "BMW", "country": "Germany"},
    ]
    
    researcher = CompanyProfileResearcher()
    profiles = []
    
    for company in companies:
        print(f"\nResearching {company['name']}...")
        profile = researcher.build_profile(
            company_name=company['name'],
            country=company['country']
        )
        profiles.append(profile)
    
    # Save all profiles
    with open("multiple_companies.json", "w") as f:
        json.dump(profiles, f, indent=2)
    
    print(f"\nSaved {len(profiles)} profiles to multiple_companies.json")


def example_with_api_keys():
    """Example using API keys for enhanced search"""
    print("\n" + "="*60)
    print("Example 3: With API Keys")
    print("="*60)
    
    # You can get these from environment variables or pass directly
    researcher = CompanyProfileResearcher(
        serpapi_key="your_serpapi_key_here",
        news_api_key="your_news_api_key_here"
    )
    
    profile = researcher.build_profile(
        company_name="Tesla Inc",
        country="United States",
        location="Austin, Texas"
    )
    
    # Access raw research data
    print("\nRaw search results:")
    for i, result in enumerate(profile['rawResearchData']['entityDetails']['results'][:3]):
        print(f"{i+1}. {result.get('title', 'No title')}")
        print(f"   URL: {result.get('url', 'No URL')}")
    
    researcher.save_profile(profile, "tesla_profile.json")


def example_custom_queries():
    """Example of using individual research methods"""
    print("\n" + "="*60)
    print("Example 4: Custom Queries")
    print("="*60)
    
    researcher = CompanyProfileResearcher()
    company_name = "Apple Inc"
    country = "United States"
    
    # Research specific aspects
    print("\nResearching entity details...")
    entity_data = researcher.research_entity_details(company_name, country)
    print(f"Found {len(entity_data['results'])} entity results")
    
    print("\nResearching principals...")
    principals_data = researcher.research_principals(company_name, country)
    print(f"Found {len(principals_data['results'])} principal results")
    
    print("\nResearching business activities...")
    business_data = researcher.research_business_activities(company_name)
    print(f"Found {len(business_data['results'])} business results")
    
    # Build full profile
    profile = researcher.build_profile(company_name, country)
    researcher.save_profile(profile, "apple_profile.json")


def example_batch_processing():
    """Example for processing a list of companies from a file"""
    print("\n" + "="*60)
    print("Example 5: Batch Processing")
    print("="*60)
    
    # Example companies file (JSON format)
    companies_data = {
        "companies": [
            {"name": "SAP", "country": "Germany", "location": "Walldorf"},
            {"name": "ASML", "country": "Netherlands", "location": "Veldhoven"},
            {"name": "Novo Nordisk", "country": "Denmark", "location": "Copenhagen"}
        ]
    }
    
    # Save companies list
    with open("companies_list.json", "w") as f:
        json.dump(companies_data, f, indent=2)
    
    # Process companies
    researcher = CompanyProfileResearcher()
    results = []
    
    with open("companies_list.json", "r") as f:
        data = json.load(f)
    
    for company in data['companies']:
        print(f"\nProcessing: {company['name']}")
        try:
            profile = researcher.build_profile(
                company_name=company['name'],
                country=company['country'],
                location=company.get('location', '')
            )
            results.append(profile)
        except Exception as e:
            print(f"Error processing {company['name']}: {e}")
    
    # Save batch results
    with open("batch_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nProcessed {len(results)} companies successfully")


def example_extract_specific_info():
    """Example of extracting specific information from profile"""
    print("\n" + "="*60)
    print("Example 6: Extract Specific Information")
    print("="*60)
    
    researcher = CompanyProfileResearcher()
    profile = researcher.build_profile("Microsoft", "United States")
    
    # Extract specific fields
    info = {
        "name": profile['entityConfirmation']['registeredLegalName'],
        "country": profile['entityConfirmation']['countryOfIncorporation'],
        "website": profile['companyProfileEnrichment']['websiteURL'],
        "risk_status": profile['riskAssessmentOutcome']['status'],
        "risk_reasoning": profile['riskAssessmentOutcome']['reasoning'],
        "num_search_results": len(profile['rawResearchData']['entityDetails']['results'])
    }
    
    print("\nExtracted Information:")
    for key, value in info.items():
        print(f"{key}: {value}")
    
    # Save extracted info
    with open("extracted_info.json", "w") as f:
        json.dump(info, f, indent=2)


if __name__ == "__main__":
    print("\nCompany Profile Researcher - Examples")
    print("="*60)
    
    # Run examples
    try:
        example_basic_usage()
    except Exception as e:
        print(f"Error in example 1: {e}")
    
    # Uncomment to run other examples
    # example_multiple_companies()
    # example_with_api_keys()
    # example_custom_queries()
    # example_batch_processing()
    # example_extract_specific_info()
    
    print("\n" + "="*60)
    print("Examples completed!")
    print("="*60)

