import http.cookiejar
import json
from sys import argv, exit
import os

import requests
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
            key_elementId_mapping = {
                "assessment": "automated_scoring-recomendtation-data",
                "description": "description-recomendtation-data",
                "rationale": "rationale_statement-recomendtation-data",
                "impact": "impact_statement-recomendtation-data",
                "audit": "audit_procedure-recomendtation-data",
                "remediation": "remediation_procedure-recomendtation-data",
                "default_value": "default_value-recomendtation-data",
                "artifact_eq": "artifact_equation-recomendtation-data",
                "mitre_mapping": "mitre_mappings-recomendtation-data",
                "references": "references-recomendtation-data"
            }
            for key, element_id in key_elementId_mapping.items():
                element = soup.find(id=element_id)
                if element is not None:
                    parsed_html[key] = element.decode_contents().strip()
                else:
                    raise ValueError(f"Response for {url} missing the element #{element_id}. Make sure session cookies are still valid.")
            return parsed_html


if __name__ == "__main__":
    if len(argv) != 2:
        print("Please provide a file name for the output file e.g. 'python fetch.py azure_150'")
        exit(2)
    else:
        save_path = f"./output/{argv[1]}.json"
        if os.path.exists(save_path):
            print(f"Output path {save_path} already exists. Process terminated to avoid overwriting the file. To continue, Specify a different name, move, or delete the file.")
            exit(1)
    
    # Load JSON data from file
    with open('./navtree.json') as json_file:
        json_data = json.load(json_file)
        
    # Parse JSON and fetch web page data
    parsed_data: "list[dict]" = parse_json(json_data)

    output = []
    for datum in parsed_data:
        output.append(fetch_webpage_data(datum))

    # save results
    with open(save_path, "w") as f:
        json.dump(output, f)