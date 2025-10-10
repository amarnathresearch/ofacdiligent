"""
Simple Program to Build DEF 14A URL from CIK
"""

import requests

def get_def14a_url(cik, user_email='amarnath@gmail.com'):
    """
    Get DEF 14A URL from CIK
    
    Args:
        cik: Company CIK (e.g., '0000320193' or '320193')
        user_email: Your email (SEC requirement)
        
    Returns:
        Complete URL to DEF 14A filing
    """
    
    # Step 1: Fetch submissions JSON
    cik_padded = str(cik).zfill(10)
    api_url = f'https://data.sec.gov/submissions/CIK{cik_padded}.json'
    
    headers = {'User-Agent': user_email}
    response = requests.get(api_url, headers=headers)
    data = response.json()
    
    # Step 2: Find DEF 14A in recent filings
    recent = data['filings']['recent']
    
    for i in range(len(recent['form'])):
        if recent['form'][i] == 'DEF 14A':
            # Step 3: Extract components
            cik_clean = str(cik).lstrip('0')
            accession = recent['accessionNumber'][i].replace('-', '')
            primary_doc = recent['primaryDocument'][i]
            
            # Step 4: Build URL
            url = f"https://www.sec.gov/Archives/edgar/data/{cik_clean}/{accession}/{primary_doc}"
            
            return url
    
    return None


# Usage
if __name__ == "__main__":
    # Apple Inc.
    # cik = '0000320193'
    cik = '0001318605'
    
    url = get_def14a_url(cik, 'your-email@example.com')
    
    print(f"DEF 14A URL: {url}")
    
    # Expected output:
    # https://www.sec.gov/Archives/edgar/data/320193/000119312521001987/d767770ddef14a.htm