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

def render_carousel(items):
    """
    Gera o HTML/CSS/JS para um carrossel full-width.
    """
    
    css = """
    <style>
        body {
            margin: 0;
            padding: 0;
            background-color: transparent;
        }
        
        .slider-wrapper {
            display: flex;
            align-items: center;
            gap: 15px;
            font-family: 'Source Sans Pro', sans-serif;
            width: 100%;
            padding: 0 20px; /* Margem lateral de segurança */
            box-sizing: border-box;
        }

        .carousel-track {
            display: flex;
            overflow-x: auto;
            scroll-behavior: smooth;
            gap: 20px;
            padding: 10px 5px;
            width: 100%;
            -webkit-overflow-scrolling: touch;
        }
        .carousel-track::-webkit-scrollbar {
            display: none;
        }
        .carousel-track {
            -ms-overflow-style: none;
            scrollbar-width: none;
        }

        .news-card {
            /* Cor do fundo igual ao print (Verde Petróleo/Finep) */
            background-color: #004d40; 
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            
            /* Lógica para 3 cards ocuparem a tela inteira */
            min-width: 300px; /* Tamanho mínimo para não esmagar */
            width: 32%;       /* Tenta ocupar um terço da tela */
            
            height: 140px;
            
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
            text-decoration: none;
            color: white; /* Texto branco */
            transition: transform 0.2s, background-color 0.2s;
            border: 1px solid rgba(255,255,255,0.1);
        }

        .news-card:hover {
            transform: translateY(-4px);
            background-color: #00695c; /* Um pouco mais claro no hover */
            box-shadow: 0 8px 12px rgba(0,0,0,0.4);
        }

        .news-title {
            font-size: 16px;
            font-weight: 600;
            text-align: center;
            line-height: 1.4;
            color: #ffffff;
            
            display: -webkit-box;
            -webkit-line-clamp: 5;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }

        /* Botões de Navegação */
        .nav-btn {
            background-color: rgba(0,0,0,0.4);
            color: white;
            border: none;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            min-width: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 20px;
            transition: all 0.2s;
            user-select: none;
        }
        .nav-btn:hover {
            background-color: rgba(0,0,0,0.8);
            transform: scale(1.1);
        }
        
        /* Responsividade para celular */
        @media (max-width: 768px) {
            .news-card {
                min-width: 85vw; /* No celular ocupa quase tudo */
            }
        }
    </style>
    """

    javascript = """
    <script>
        function scrollCarousel(direction) {
            const track = document.getElementById('track');
            // Rola o equivalente a largura de um card + gap (aprox 320px)
            const scrollAmount = track.clientWidth / 2;
            
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
    <div class="slider-wrapper">
        <div class="nav-btn" onclick="scrollCarousel('left')">&#10094;</div>
        <div class="carousel-track" id="track">
            {cards_html}
        </div>
        <div class="nav-btn" onclick="scrollCarousel('right')">&#10095;</div>
    </div>
    {javascript}
    """
    
    # Altura um pouco maior para caber sombra e hover
    components.html(full_html, height=180, scrolling=False)
