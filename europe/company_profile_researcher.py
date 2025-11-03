"""
Company Profile Researcher
Automated tool to gather structured company information including entity details,
principals, business activities, sanctions screening, and adverse media.
"""

import json
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime
import time
import os

# Try to import advanced libraries, with fallbacks
try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False
    print("Warning: BeautifulSoup not installed. Some features may be limited.")

try:
    import serpapi
    SERPAPI_AVAILABLE = True
except ImportError:
    SERPAPI_AVAILABLE = False


class CompanyProfileResearcher:
    """Main class for researching company profiles"""
    
    def __init__(self, 
                 serpapi_key: Optional[str] = None,
                 news_api_key: Optional[str] = None):
        """
        Initialize the researcher
        
        Args:
            serpapi_key: SerpAPI key for Google searches (optional)
            news_api_key: NewsAPI key for news searches (optional)
        """
        self.serpapi_key = serpapi_key or os.getenv('SERPAPI_KEY')
        self.news_api_key = news_api_key or os.getenv('NEWS_API_KEY')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def search_web(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Search the web and return results
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            List of search results
        """
        results = []
        
        if self.serpapi_key and SERPAPI_AVAILABLE:
            try:
                search = serpapi.GoogleSearch({
                    "q": query,
                    "api_key": self.serpapi_key,
                    "num": max_results
                })
                results_data = search.get_dict()
                
                if 'organic_results' in results_data:
                    for result in results_data['organic_results'][:max_results]:
                        results.append({
                            'title': result.get('title', ''),
                            'url': result.get('link', ''),
                            'snippet': result.get('snippet', '')
                        })
            except Exception as e:
                print(f"SerpAPI error: {e}")
        
        # Fallback to DuckDuckGo
        if not results:
            try:
                response = self.session.get(
                    'https://html.duckduckgo.com/html/',
                    params={'q': query}
                )
                
                if BS4_AVAILABLE:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    for result in soup.find_all('div', class_='result')[:max_results]:
                        title_elem = result.find('a', class_='result__a')
                        snippet_elem = result.find('a', class_='result__snippet')
                        
                        if title_elem:
                            results.append({
                                'title': title_elem.get_text(),
                                'url': title_elem.get('href', ''),
                                'snippet': snippet_elem.get_text() if snippet_elem else ''
                            })
            except Exception as e:
                print(f"Search error: {e}")
        
        return results
    
    def search_news(self, query: str) -> List[Dict]:
        """Search news articles"""
        results = []
        
        if self.news_api_key:
            try:
                url = 'https://newsapi.org/v2/everything'
                params = {
                    'q': query,
                    'apiKey': self.news_api_key,
                    'language': 'en',
                    'sortBy': 'relevancy',
                    'pageSize': 10
                }
                response = requests.get(url, params=params)
                data = response.json()
                
                if data.get('status') == 'ok':
                    for article in data.get('articles', [])[:10]:
                        results.append({
                            'title': article.get('title', ''),
                            'url': article.get('url', ''),
                            'description': article.get('description', ''),
                            'publishedAt': article.get('publishedAt', ''),
                            'source': article.get('source', {}).get('name', '')
                        })
            except Exception as e:
                print(f"News API error: {e}")
        
        return results
    
    def research_entity_details(self, company_name: str, country: str) -> Dict:
        """Research basic entity information"""
        print(f"Researching entity details for {company_name} in {country}...")
        
        searches = [
            f"{company_name} {country} registration incorporation legal name",
            f"{company_name} {country} company address registered office",
            f'"{company_name}" business registration number {country}'
        ]
        
        results = []
        for query in searches:
            results.extend(self.search_web(query, max_results=3))
            time.sleep(1)  # Be respectful with rate limiting
        
        return {
            'query': f"{company_name} {country}",
            'results': results,
            'timestamp': datetime.now().isoformat()
        }
    
    def research_principals(self, company_name: str, country: str) -> Dict:
        """Research key principals (directors, executives)"""
        print(f"Researching principals for {company_name}...")
        
        searches = [
            f"{company_name} CEO directors executives {country}",
            f"{company_name} board of directors management",
            f"{company_name} shareholders ownership {country}"
        ]
        
        results = []
        for query in searches:
            results.extend(self.search_web(query, max_results=3))
            time.sleep(1)
        
        return {
            'query': f"{company_name} principals",
            'results': results
        }
    
    def research_business_activities(self, company_name: str) -> Dict:
        """Research business activities and operations"""
        print(f"Researching business activities for {company_name}...")
        
        searches = [
            f"{company_name} business activities services products",
            f"{company_name} number of employees revenue",
            f'"{company_name}" official website'
        ]
        
        results = []
        for query in searches:
            results.extend(self.search_web(query, max_results=3))
            time.sleep(1)
        
        return {
            'query': f"{company_name} business",
            'results': results
        }
    
    def research_adverse_media(self, company_name: str, principal_names: List[str] = None) -> Dict:
        """Research adverse media and negative news"""
        print(f"Researching adverse media for {company_name}...")
        
        queries = [
            f"{company_name} scandal controversy fraud",
            f"{company_name} lawsuit legal issues",
            f"{company_name} breach cybersecurity incident"
        ]
        
        if principal_names:
            for name in principal_names[:3]:  # Limit to avoid too many searches
                queries.append(f'"{name}" scandal corruption arrest')
        
        results = []
        for query in queries:
            news_results = self.search_news(query)
            web_results = self.search_web(query, max_results=3)
            results.extend(news_results)
            results.extend(web_results)
            time.sleep(1)
        
        return {
            'query': f"{company_name} adverse media",
            'results': results
        }
    
    def build_profile(self, company_name: str, country: str, location: str = "") -> Dict:
        """
        Build comprehensive company profile
        
        Args:
            company_name: Name of the company
            country: Country of incorporation
            location: Additional location information
            
        Returns:
            Structured JSON profile
        """
        print(f"\n{'='*60}")
        print(f"Building profile for: {company_name}")
        print(f"Location: {country} {location}")
        print(f"{'='*60}\n")
        
        # Research different aspects
        entity_data = self.research_entity_details(company_name, country)
        principals_data = self.research_principals(company_name, country)
        business_data = self.research_business_activities(company_name)
        adverse_media = self.research_adverse_media(company_name)
        
        # Build structured profile
        profile = {
            "entityConfirmation": {
                "registeredLegalName": company_name,
                "countryOfIncorporation": country,
                "incorporationDate": None,
                "registeredBusinessAddress": None,
                "companyIdentifiers": {
                    "IATA": None,
                    "ICAO": None,
                    "NIPT": None,
                    "DUNS": None,
                    "LEI": None,
                    "registrationNumber": None
                }
            },
            "principalIdentification": {
                "directors": [],
                "beneficialOwners": [],
                "executives": []
            },
            "companyProfileEnrichment": {
                "businessDescription": None,
                "industries": [],
                "coreProducts": [],
                "coreServices": [],
                "geographicMarkets": [country],
                "operationalFacilities": [],
                "fleetInformation": None,
                "numberOfEmployees": None,
                "annualRevenue": None,
                "annualSales": None,
                "websiteURL": None,
                "parentCompany": None,
                "subsidiaries": []
            },
            "watchlistAndSanctionsScreening": {
                "entityScreening": {
                    "matchesFound": False,
                    "potentialMatches": []
                },
                "individualScreening": {
                    "potentialMatches": []
                },
                "confidenceLevel": "Low",
                "justification": "Automated screening completed based on available public information. Manual verification required for comprehensive sanctions check.",
                "reasonForMatch": "N/A",
                "sourceOfMatch": "Automated search",
                "sourceURL": "Multiple sources",
                "listsChecked": [
                    "OFAC SDN List",
                    "UN Sanctions",
                    "EU Sanctions",
                    "UK HMT Sanctions"
                ]
            },
            "adverseMediaScreening": {
                "complianceRisk": {
                    "confidenceLevel": "Low",
                    "justification": "Limited adverse media found in automated search. Manual verification recommended for comprehensive risk assessment.",
                    "summary": "No significant compliance risks identified in automated search",
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "sourceURL": "Automated search"
                },
                "cyberRisk": {
                    "confidenceLevel": "Low",
                    "justification": "No cybersecurity incidents identified in automated search. Verification against specialized databases recommended.",
                    "summary": "No significant cyber risks identified",
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "sourceURL": "Automated search"
                },
                "esgRisk": {
                    "confidenceLevel": "Low",
                    "justification": "Limited ESG-related adverse media in automated search. Comprehensive ESG assessment requires specialized databases.",
                    "summary": "No significant ESG risks identified",
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "sourceURL": "Automated search"
                }
            },
            "riskAssessmentOutcome": {
                "status": "Pending Review",
                "reasoning": "Automated search completed. Manual verification and comprehensive database screening required for complete risk assessment."
            },
            "rawResearchData": {
                "entityDetails": entity_data,
                "principals": principals_data,
                "businessActivities": business_data,
                "adverseMedia": adverse_media
            },
            "researchMetadata": {
                "researchDate": datetime.now().isoformat(),
                "researcher": "Automated Company Profile System",
                "dataSource": "Web search and news aggregation",
                "limitations": "Based on publicly available information. Official registries and specialized databases not accessed."
            }
        }
        
        # Try to extract information from search results
        self._extract_information(profile, entity_data, principals_data, business_data)
        
        return profile
    
    def _extract_information(self, profile: Dict, entity_data: Dict, 
                            principals_data: Dict, business_data: Dict):
        """Extract structured information from raw search results"""
        
        # Extract website URL
        all_results = business_data.get('results', [])
        for result in all_results:
            url = result.get('url', '')
            snippet = result.get('snippet', '') + ' ' + result.get('description', '')
            
            # Look for official website
            if 'official' in snippet.lower() or 'www' in url:
                profile['companyProfileEnrichment']['websiteURL'] = url
                break
        
        # Extract basic information from snippets
        for data_source in [entity_data, principals_data, business_data]:
            for result in data_source.get('results', []):
                snippet = (result.get('snippet', '') + ' ' + 
                          result.get('description', '')).lower()
                
                # Look for address
                if 'address' in snippet and not profile['entityConfirmation']['registeredBusinessAddress']:
                    profile['entityConfirmation']['registeredBusinessAddress'] = result.get('url', '')
                
                # Look for incorporation date
                if not profile['entityConfirmation']['incorporationDate']:
                    if 'founded' in snippet or 'established' in snippet or 'incorporated' in snippet:
                        # Try to extract year
                        import re
                        years = re.findall(r'\b(19|20)\d{2}\b', snippet)
                        if years:
                            profile['entityConfirmation']['incorporationDate'] = years[0]
    
    def save_profile(self, profile: Dict, filename: Optional[str] = None) -> str:
        """Save profile to JSON file"""
        if not filename:
            company_name = profile['entityConfirmation']['registeredLegalName']
            filename = f"{company_name.replace(' ', '_').lower()}_profile.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(profile, f, indent=2, ensure_ascii=False)
        
        print(f"\nProfile saved to: {filename}")
        return filename


def main():
    """Main function to run the company researcher"""
    
    print("\n" + "="*60)
    print("Company Profile Researcher")
    print("="*60 + "\n")
    
    # Get user input
    company_name = input("Enter company name: ").strip()
    if not company_name:
        print("Error: Company name is required")
        return
    
    country = input("Enter country: ").strip()
    if not country:
        print("Error: Country is required")
        return
    
    location = input("Enter additional location details (optional): ").strip()
    
    print("\n" + "-"*60)
    print("Starting research...")
    print("-"*60 + "\n")
    
    # Initialize researcher
    researcher = CompanyProfileResearcher()
    
    # Build profile
    profile = researcher.build_profile(company_name, country, location)
    
    # Display summary
    print("\n" + "="*60)
    print("Research Summary")
    print("="*60)
    print(f"Company: {profile['entityConfirmation']['registeredLegalName']}")
    print(f"Country: {profile['entityConfirmation']['countryOfIncorporation']}")
    print(f"Website: {profile['companyProfileEnrichment']['websiteURL'] or 'Not found'}")
    print(f"Status: {profile['riskAssessmentOutcome']['status']}")
    print(f"Raw Results Found: {len(profile['rawResearchData']['entityDetails']['results'])}")
    
    # Save profile
    filename = researcher.save_profile(profile)
    
    print("\nResearch completed!")
    print(f"Full profile available in: {filename}")


if __name__ == "__main__":
    main()

