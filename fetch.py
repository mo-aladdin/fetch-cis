import requests
import json
import http.cookiejar
from bs4 import BeautifulSoup

def fetch_data(url, session):
    response = session.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

def parse_json(json_data):
    parsed_data = []
    navtree = json_data['navtree']
    for section in navtree:
        recommendations = section.get('recommendations_for_nav_tree', [])
        for recommendation in recommendations:
            recommendation_id = recommendation['id']
            recommendation_title = recommendation['title']
            recommendation_ref = recommendation['view_level']
            url = f"https://workbench.cisecurity.org/sections/{section['id']}/recommendations/{recommendation_id}"
            parsed_data.append({
                'url': url,
                'title': recommendation_title,
                'ref': recommendation_ref
            })
    return parsed_data

def fetch_webpage_data(data: "dict"):
    with requests.Session() as session:
        # Load cookies from a cookies.txt file
        cookie_jar = http.cookiejar.MozillaCookieJar()
        cookie_jar.load("cookies.txt")
        session.cookies = cookie_jar  
        url = data['url']
        html = fetch_data(url, session)
        if html:
            # Parse HTML and extract inner HTML of specific elements
            parsed_html = data.copy()
            soup = BeautifulSoup(html, 'html.parser')
            element_ids = [
                "automated_scoring-recomendtation-data",
                "description-recomendtation-data",
                "rationale_statement-recomendtation-data",
                "impact_statement-recomendtation-data",
                "audit_procedure-recomendtation-data",
                "remediation_procedure-recomendtation-data",
                "default_value-recomendtation-data",
                "artifact_equation-recomendtation-data",
                "mitre_mappings-recomendtation-data",
                "references-recomendtation-data"
            ]
            for element_id in element_ids:
                element = soup.find(id=element_id)
                if element is not None:
                    parsed_html[element_id] = element.decode_contents().strip()
                else:
                    raise ValueError(f"None element {element_id} for {url}")
            
            return parsed_html

# Load JSON data from file
with open('./navtree.json') as json_file:
    json_data = json.load(json_file)
    
# Parse JSON and fetch web page data
parsed_data: "list[dict]" = parse_json(json_data)

output = fetch_webpage_data(parsed_data[0])

# Print the final dictionary
with open("output.py", "w") as f:
    f.write(str(output))