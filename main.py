import requests
from bs4 import BeautifulSoup
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import time

def fetch_page(url):
    try:
        response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except requests.RequestException as e:
        print(f"Erro ao acessar a página {url}: {e}")
        return None

def extract_content_from_section(url, content_selector, title_selector):
    soup = fetch_page(url)
    if not soup:
        return None, None
    main_content = soup.find(*content_selector)
    if main_content:
        title_element = soup.find(*title_selector)
        title = title_element.text.strip() if title_element else url.split('/')[-1]
        section_content = []
        for element in main_content.find_all(['p', 'ul', 'ol', 'h2', 'h3'], recursive=True):
            if element.name in ['h2', 'h3']:
                section_content.append(f"\n### {element.text.strip()}\n")
            elif element.name in ['p', 'ul', 'ol']:
                section_content.append(element.text.strip())
        return title, '\n'.join(section_content)
    return None, None

def extract_all_content(base_url, domain, content_selector, title_selector):
    content = {}
    soup = fetch_page(base_url)
    if not soup:
        return content

    main_content = soup.find(*content_selector)
    if main_content:
        # Captura seções de tabelas
        tables = main_content.find_all('table')
        for table in tables:
            for row in table.find_all('tr'):
                cells = row.find_all(['th', 'td'])
                if cells and len(cells) > 0:
                    section_title = cells[0].text.strip()
                    if section_title:
                        section_links = row.find_all('a', href=True)
                        section_content = []
                        for link in section_links:
                            href = link.get('href')
                            if href and href.startswith('/'):
                                full_url = f"{domain}{href}"
                                sub_title, sub_content = extract_content_from_section(full_url, content_selector, title_selector)
                                if sub_title and sub_content:
                                    section_content.append(f"**{sub_title}**\n{sub_content}")
                        if not section_content:
                            section_content = [cell.text.strip() for cell in cells[1:] if cell.text.strip()]
                        if section_content:
                            content[section_title] = '\n'.join(section_content)

        
        for header in main_content.find_all(['h2', 'h3']):
            section_title = header.text.strip()
            next_element = header.find_next()
            section_content = []
            while next_element and next_element.name not in ['h2', 'h3']:
                if next_element.name in ['p', 'ul', 'ol']:
                    section_content.append(next_element.text.strip())
                next_element = next_element.find_next()
            if section_content:
                content[section_title] = '\n'.join(section_content)
    
    print("Conteúdo extraído:", content)
    return content

def create_pdf(content, filename="output.pdf"):
    if not content:
        print("Nenhum conteúdo para gerar o PDF!")
        return
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    for title, text in content.items():
        story.append(Paragraph(title, styles['Heading1']))
        for section in text.split('\n**'):
            if section.strip():
                if section.startswith('*'):
                    section = section[1:].strip()
                lines = section.split('\n')
                for line in lines:
                    if line.strip():
                        if line.startswith('### '):
                            story.append(Paragraph(line.replace('### ', '', 1), styles['Heading2']))
                        else:
                            story.append(Paragraph(line, styles['BodyText']))
        story.append(Spacer(1, 12))
    doc.build(story)
    print(f"PDF gerado com sucesso: {filename}")

# Configuração para o site alvo
base_url = "https://pt.stardewvalleywiki.com/Stardew_Valley_Wiki"
domain = "https://pt.stardewvalleywiki.com"
content_selector = ('div', {'class': 'mw-parser-output'})
title_selector = ('h1', {'class': 'firstHeading'})
output_filename = "stardew_valley_guide.pdf"

content = extract_all_content(base_url, domain, content_selector, title_selector)
create_pdf(content, output_filename)
time.sleep(1)