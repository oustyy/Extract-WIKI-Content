# Extract-WIKI-Content
 extract content from a wiki to generate a pdf with title and content
# Stardew Valley Wiki Scraper

## Descrição
Este script em Python faz o scraping de conteúdo da Stardew Valley Wiki (ou outros sites baseados em MediaWiki) e gera um arquivo PDF com o conteúdo extraído, organizado por seções. Ele extrai títulos e textos de páginas, incluindo subpáginas vinculadas, e formata tudo em um documento PDF usando a biblioteca `reportlab`.

## Funcionalidades
- **Extração de Conteúdo**: Coleta títulos e textos de parágrafos, listas e cabeçalhos de uma página wiki.
- **Suporte a Subpáginas**: Extrai conteúdo de links em tabelas, permitindo capturar informações de seções relacionadas.
- **Geração de PDF**: Cria um PDF estruturado com títulos e conteúdos formatados.
- **Configuração Flexível**: Permite ajustar seletores HTML e URLs para outros sites com estrutura semelhante.

## Requisitos
- Python 3.6+
- Bibliotecas Python:
  - `requests`
  - `beautifulsoup4`
  - `reportlab`

Instale as dependências com:
```bash
pip install requests beautifulsoup4 reportlab
```

## Como Usar
1. **Salve o Script**: Copie o código do script para um arquivo, por exemplo, `web_scraper.py`.
2. **Configure as Variáveis**:
   - `base_url`: URL da página principal (ex.: `https://pt.stardewvalleywiki.com/Stardew_Valley_Wiki`).
   - `domain`: Domínio base para links relativos (ex.: `https://pt.stardewvalleywiki.com`).
   - `content_selector`: Seletor HTML para o conteúdo principal (ex.: `('div', {'class': 'mw-parser-output'})`).
   - `title_selector`: Seletor HTML para o título da página (ex.: `('h1', {'class': 'firstHeading'})`).
   - `output_filename`: Nome do arquivo PDF gerado (ex.: `stardew_valley_guide.pdf`).
3. **Execute o Script**:
   ```bash
   python web_scraper.py
   ```
4. **Verifique o Resultado**:
   - Um arquivo PDF (ex.: `stardew_valley_guide.pdf`) será gerado no mesmo diretório.
   - O console mostrará o conteúdo extraído para depuração.

## Exemplo de Configuração
Para a Stardew Valley Wiki:
```python
base_url = "https://pt.stardewvalleywiki.com/Stardew_Valley_Wiki"
domain = "https://pt.stardewvalleywiki.com"
content_selector = ('div', {'class': 'mw-parser-output'})
title_selector = ('h1', {'class': 'firstHeading'})
output_filename = "stardew_valley_guide.pdf"
```

## Adaptação para Outros Sites
Para usar o script com outros sites baseados em MediaWiki (ex.: Wikipédia):
1. Inspecione o HTML do site alvo usando o "Inspecionar elemento" no navegador.
2. Ajuste `content_selector` e `title_selector` para corresponder às classes ou IDs do site.
3. Atualize `base_url` e `domain` para o site desejado.
4. Modifique `output_filename` para um nome relevante.

Exemplo para a Wikipédia em inglês:
```python
base_url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
domain = "https://en.wikipedia.org"
content_selector = ('div', {'id': 'content'})
title_selector = ('h1', {'id': 'firstHeading'})
output_filename = "python_wiki.pdf"
```

## Cuidados
- **Termos de Uso**: Verifique o `robots.txt` do site (ex.: `https://pt.stardewvalleywiki.com/robots.txt`) para garantir que o scraping é permitido.
- **Sobrecarga do Servidor**: O script inclui um `time.sleep(1)` para evitar muitas requisições rápidas. Ajuste se necessário.
- **Depuração**: Use `print(soup.prettify())` na função `fetch_page` para inspecionar o HTML e confirmar os seletores.

## Limitações
- Funciona melhor com sites baseados em MediaWiki devido aos seletores configurados.
- Não suporta a extração de imagens ou tabelas complexas no PDF (apenas texto).
- Pode exigir ajustes para sites com estruturas HTML muito diferentes.

## Licença
Este projeto é fornecido como está, sem garantias. Use por sua conta e risco, respeitando os termos de uso dos sites-alvo.
