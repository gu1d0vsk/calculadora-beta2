import streamlit.components.v1 as components
import feedparser

def get_finep_news():
    """
    Busca as notícias do RSS da Finep (apenas título e link).
    """
    try:
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

def render_footer_carousel(items):
    """
    Renderiza um carrossel de CARDS fixo no rodapé da página.
    """
    
    css = """
    <style>
        body {
            margin: 0;
            padding: 0;
            background: transparent;
        }
        
        /* Container fixo no rodapé */
        .footer-wrapper {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 140px; /* Altura da barra */
            background-color: rgba(20, 20, 20, 0.95); /* Fundo escuro atrás dos cards */
            border-top: 1px solid #333;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 99999; /* Garante que fique por cima de tudo */
            box-shadow: 0 -4px 10px rgba(0,0,0,0.2);
            font-family: 'Source Sans Pro', sans-serif;
        }

        /* Área interna que segura setas e trilho */
        .inner-container {
            display: flex;
            align-items: center;
            width: 100%;
            max-width: 1200px; /* Limita largura em telas gigantes */
            padding: 0 10px;
            gap: 10px;
        }

        /* Trilho de rolagem */
        .carousel-track {
            display: flex;
            overflow-x: auto;
            scroll-behavior: smooth;
            gap: 15px;
            padding: 10px 5px;
            width: 100%;
            
            /* Esconde scrollbar */
            -webkit-overflow-scrolling: touch;
            scrollbar-width: none; 
            -ms-overflow-style: none;
        }
        .carousel-track::-webkit-scrollbar {
            display: none;
        }

        /* O Card Verde */
        .news-card {
            background-color: #004d40; /* Verde Finep */
            border-radius: 8px;
            
            /* Tamanho fixo para o rodapé */
            min-width: 260px;
            max-width: 260px;
            height: 100px;
            
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 15px;
            text-decoration: none;
            color: white;
            font-size: 14px;
            font-weight: 600;
            line-height: 1.3;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.1);
            transition: transform 0.2s, background-color 0.2s;
            flex-shrink: 0; /* Impede que o card encolha */
        }

        .news-card:hover {
            transform: translateY(-3px);
            background-color: #00695c;
            box-shadow: 0 4px 8px rgba(0,0,0,0.4);
        }

        .news-title {
            display: -webkit-box;
            -webkit-line-clamp: 4;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }

        /* Botões de Navegação */
        .nav-btn {
            background-color: rgba(255,255,255,0.1);
            color: white;
            border: none;
            border-radius: 50%;
            width: 32px;
            height: 32px;
            min-width: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 18px;
            transition: all 0.2s;
            user-select: none;
        }
        .nav-btn:hover {
            background-color: rgba(255,255,255,0.3);
        }
    </style>
    """

    javascript = """
    <script>
        function scrollCarousel(direction) {
            const track = document.getElementById('track');
            const scrollAmount = 280; // Tamanho do card + gap
            
            if (direction === 'left') {
                track.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
            } else {
                track.scrollBy({ left: scrollAmount, behavior: 'smooth' });
            }
        }
    </script>
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
    <div class="footer-wrapper">
        <div class="inner-container">
            <div class="nav-btn" onclick="scrollCarousel('left')">&#10094;</div>
            <div class="carousel-track" id="track">
                {cards_html}
            </div>
            <div class="nav-btn" onclick="scrollCarousel('right')">&#10095;</div>
        </div>
    </div>
    {javascript}
    """
    
    # Altura fixa do componente iframe
    components.html(full_html, height=140, scrolling=False)
