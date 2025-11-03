"""
Quick test script for the Company Profile Researcher
Run this to test the basic functionality
"""

from company_profile_researcher import CompanyProfileResearcher
import json

def test_researcher():
    """Test the researcher with a sample company"""
    
    print("\n" + "="*70)
    print("Testing Company Profile Researcher")
    print("="*70 + "\n")
    
    # Initialize researcher
    print("Initializing researcher...")
    researcher = CompanyProfileResearcher()
    print("✓ Researcher initialized\n")
    
    # Test parameters
    test_company = "Air Albania"
    test_country = "Albania"
    
    print(f"Test Company: {test_company}")
    print(f"Test Country: {test_country}")
    print("\n" + "-"*70)
    print("Starting research (this may take a few moments)...")
    print("-"*70 + "\n")
    
    try:
        # Build profile
        profile = researcher.build_profile(
            company_name=test_company,
            country=test_country
        )
        
        print("\n" + "-"*70)
        print("Research completed successfully!")
        print("-"*70 + "\n")
        
        # Display results
        print("Profile Summary:")
        print(f"  Company Name: {profile['entityConfirmation']['registeredLegalName']}")
        print(f"  Country: {profile['entityConfirmation']['countryOfIncorporation']}")
        print(f"  Website: {profile['companyProfileEnrichment']['websiteURL'] or 'Not found'}")
        print(f"  Risk Status: {profile['riskAssessmentOutcome']['status']}")
        
        # Count raw results
        entity_results = len(profile['rawResearchData']['entityDetails']['results'])
        principal_results = len(profile['rawResearchData']['principals']['results'])
        business_results = len(profile['rawResearchData']['businessActivities']['results'])
        adverse_results = len(profile['rawResearchData']['adverseMedia']['results'])
        
        print(f"\nRaw Search Results:")
        print(f"  Entity Details: {entity_results} results")
        print(f"  Principals: {principal_results} results")
        print(f"  Business Activities: {business_results} results")
        print(f"  Adverse Media: {adverse_results} results")
        
        # Save profile
        filename = researcher.save_profile(profile, "test_output.json")
        
        print("\n" + "="*70)
        print(f"✓ Test completed successfully!")
        print(f"✓ Profile saved to: {filename}")
        print("="*70 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error during research: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_researcher()
    
    if success:
        print("All tests passed! ✓")
    else:
        print("Tests failed. Please check the error messages above.")

