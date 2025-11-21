import streamlit.components.v1 as components
import feedparser

def get_finep_news():
    """
    Busca as notícias do RSS da Finep (apenas título e link).
    """
    try:
        # URL do RSS
        rss_url = "https://www.finep.gov.br/component/ninjarsssyndicator/?feed_id=1&format=raw"
        feed = feedparser.parse(rss_url)
        
        news_items = []
        
        for entry in feed.entries:
            news_items.append({
                "title": entry.title,
                "link": entry.link
            })
            
        return news_items
    except Exception as e:
        print(f"Erro ao buscar notícias: {e}")
        return []

def render_carousel(items):
    """
    Gera o HTML e CSS para o carrossel de texto e o renderiza.
    """
    css = """
    <style>
        .carousel-container {
            display: flex;
            overflow-x: auto;
            scroll-behavior: smooth;
            padding: 15px 5px;
            gap: 15px;
            scrollbar-width: thin;
        }
        .carousel-container::-webkit-scrollbar {
            height: 6px;
        }
        .carousel-container::-webkit-scrollbar-thumb {
            background-color: #ddd;
            border-radius: 3px;
        }
        .news-card {
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.08);
            border: 1px solid #eee;
            
            /* Tamanho do cartão */
            min-width: 280px;
            max-width: 280px;
            height: 140px; /* Altura fixa para alinhar */
            
            display: flex;
            align-items: center; /* Centraliza verticalmente */
            justify-content: center; /* Centraliza horizontalmente */
            
            padding: 20px;
            text-decoration: none;
            color: #333;
            font-family: sans-serif;
            transition: all 0.2s ease;
        }
        .news-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 10px rgba(0,0,0,0.1);
            border-color: #ddd;
            color: #005051; /* Muda a cor do texto ao passar o mouse (verde escuro) */
        }
        .news-title {
            font-size: 15px;
            font-weight: 600;
            line-height: 1.4;
            text-align: center;
            
            /* Lógica para cortar apenas se for MUITO grande (8 linhas) */
            display: -webkit-box;
            -webkit-line-clamp: 8; 
            -webkit-box-orient: vertical;
            overflow: hidden;
        }
    </style>
    """

    cards_html = ""
    for item in items:
        cards_html += f"""
        <a href="{item['link']}" target="_blank" class="news-card">
            <div class="news-title">{item['title']}</div>
        </a>
        """

    full_html = f"""
    {css}
    <div class="carousel-container">
        {cards_html}
    </div>
    """
    
    # Altura do componente ajustada para caber o cartão + scrollbar
    components.html(full_html, height=180, scrolling=False)
