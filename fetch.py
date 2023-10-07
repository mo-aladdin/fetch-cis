import http.cookiejar
import json
import re
from sys import exit
import os

import requests
from bs4 import BeautifulSoup

def fetch_data(url, session):
    response: requests.Response = session.get(url)
    if response.status_code == 200:
        return response
    else:
        response.raise_for_status()

def parse_json(json_data):
    def generate_urls(recommendations: "list[dict]"):
        output = []
        for recommendation in recommendations:
            recommendation_id = recommendation['id']
            section_id = recommendation['section_id']
            recommendation_title = recommendation['title']
            recommendation_ref = recommendation['view_level']
            url = f"https://workbench.cisecurity.org/sections/{section_id}/recommendations/{recommendation_id}"
            output.append({
                'url': url,
                'title': recommendation_title,
                'ref': recommendation_ref
            })
        return output

    def parse_subsections(subsections):
        for section in subsections:
            subsections = section.get('subsections_for_nav_tree')
            if subsections:
                parse_subsections(subsections)
            else:
                recommendations = section.get('recommendations_for_nav_tree')
                parsed_data.extend(generate_urls(recommendations))

    parsed_data = []
    navtree = json_data['navtree']
    parse_subsections(navtree)
    return parsed_data

def fetch_webpage_data(data: "dict", session: requests.Session):
    global progress
    with session:
        url = data['url']
        print(f"{progress}Fetching {url}")
        html = fetch_data(url, session).text
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
    # Create session and load cookies from a cookies.txt file
    cookie_jar = http.cookiejar.MozillaCookieJar()
    cookie_jar.load("cookies.txt")
    session = requests.Session()
    session.cookies = cookie_jar

    # retrieve benchmark name and navtree
    with open("urls.txt") as f:
        urls =  f.read().split('\n')
        while urls[-1] is None:
            urls = urls[:-1] # in case of extra line breaks
    for idx, url in enumerate(urls):
        progress = f"[{idx+1}/{len(urls)}] "
        benchmark_id = re.search(r'\d+/*$', url).group().replace("/", "")
        print(f"{progress}Fetching benchmark title for {url}")
        html = fetch_data(url, session).text
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find(name='wb-benchmark-title').get("title")
        safename = "".join([c for c in title.replace(" ", "_") if re.match(r'\w', c)]).lower()
        save_path = f"./output/{safename}.json"
        if os.path.exists(save_path):
            print(f"{progress}Output path {save_path} already exists. Process terminated to avoid overwriting the file. To continue, Specify a different name, move, or delete the file.")
            exit(1)

        # Load JSON navtree data
        print(f"{progress}Fetching navtree data for {title}")
        url = f"https://workbench.cisecurity.org/api/v1/benchmarks/{benchmark_id}/navtree"
        json_data = fetch_data(url, session).json()
        # Parse JSON and fetch web page data
        parsed_data: "list[dict]" = parse_json(json_data)
        output = []
        for datum in parsed_data:
            output.append(fetch_webpage_data(datum, session))

        # save results
        print(f"{progress}Saving results to {save_path}")
        with open(save_path, "w") as f:
            json.dump(output, f)