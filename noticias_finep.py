import streamlit.components.v1 as components
import feedparser
from bs4 import BeautifulSoup

def get_finep_news():
    """
    Busca e processa as notícias do RSS da Finep.
    Retorna uma lista de dicionários com título, link, imagem e data.
    """
    try:
        rss_url = "http://www.finep.gov.br/component/ninjarsssyndicator/?feed_id=1&format=raw"
        feed = feedparser.parse(rss_url)
        
        news_items = []
        
        for entry in feed.entries:
            image_url = ""
            # Tenta extrair imagem de 'media_content' ou 'enclosures'
            if 'media_content' in entry:
                image_url = entry.media_content[0]['url']
            elif 'enclosures' in entry and len(entry.enclosures) > 0:
                 image_url = entry.enclosures[0]['href']
            
            # Se falhar, tenta extrair do HTML da descrição
            if not image_url and 'description' in entry:
                soup = BeautifulSoup(entry.description, 'html.parser')
                img_tag = soup.find('img')
                if img_tag and img_tag.get('src'):
                    image_url = img_tag['src']
                    if image_url.startswith('/'):
                        image_url = "http://www.finep.gov.br" + image_url

            # Imagem padrão (Logo)
            if not image_url:
                image_url = "https://www.finep.gov.br/images/logo_finep.png"

            news_items.append({
                "title": entry.title,
                "link": entry.link,
                "published": entry.published,
                "image": image_url
            })
            
        return news_items
    except Exception as e:
        print(f"Erro ao buscar notícias: {e}")
        return []

def render_carousel(items):
    """
    Gera o HTML e CSS para o carrossel e o renderiza no Streamlit.
    """
    css = """
    <style>
        .carousel-container {
            display: flex;
            overflow-x: auto;
            scroll-behavior: smooth;
            padding: 20px 0;
            gap: 20px;
            scrollbar-width: thin;
        }
        .carousel-container::-webkit-scrollbar {
            height: 8px;
        }
        .carousel-container::-webkit-scrollbar-thumb {
            background-color: #ccc;
            border-radius: 4px;
        }
        .news-card {
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            min-width: 300px;
            max-width: 300px;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            transition: transform 0.2s;
            text-decoration: none;
            color: inherit;
            font-family: sans-serif;
            border: 1px solid #e0e0e0;
        }
        .news-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 12px rgba(0,0,0,0.15);
        }
        .card-image {
            height: 150px;
            width: 100%;
            object-fit: cover;
        }
        .card-content {
            padding: 15px;
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .news-title {
            font-size: 15px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #333;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
            line-height: 1.4;
        }
        .news-date {
            font-size: 11px;
            color: #888;
            margin-top: auto;
        }
    </style>
    """

    cards_html = ""
    for item in items:
        cards_html += f"""
        <a href="{item['link']}" target="_blank" class="news-card">
            <img src="{item['image']}" class="card-image" alt="Imagem da notícia">
            <div class="card-content">
                <div class="news-title">{item['title']}</div>
                <div class="news-date">{item['published']}</div>
            </div>
        </a>
        """

    full_html = f"""
    {css}
    <div class="carousel-container">
        {cards_html}
    </div>
    """
    
    components.html(full_html, height=320, scrolling=False)
