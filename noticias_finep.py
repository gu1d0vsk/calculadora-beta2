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
    Gera o HTML/CSS/JS para um carrossel com setas de navegação.
    """
    
    # CSS para esconder a barra de rolagem e estilizar as setas
    css = """
    <style>
        /* Container principal que segura setas e o trilho */
        .slider-wrapper {
            display: flex;
            align-items: center;
            gap: 0px;
            font-family: sans-serif;
            width: 100%;
        }

        /* O trilho onde ficam os cartões (esconde a barra de rolagem) */
        .carousel-track {
            display: flex;
            overflow-x: auto;
            scroll-behavior: smooth;
            gap: 15px;
            padding: 10px 2px;
            width: 100%;
            
            /* Esconder Scrollbar (Chrome/Safari/Opera) */
            -webkit-overflow-scrolling: touch;
        }
        .carousel-track::-webkit-scrollbar {
            display: none;
        }
        /* Esconder Scrollbar (Firefox/IE/Edge) */
        .carousel-track {
            -ms-overflow-style: none;
            scrollbar-width: none;
        }

        /* O Cartão individual */
        .news-card {
            background: rgb(0 80 81);
            border: px solid #eee;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            
            /* Mágica para mostrar 3 por vez: 
               100% / 3 = 33.33% menos o espaço do gap */
            min-width: calc(33.33% - 10px); 
            max-width: calc(33.33% - 10px);
            
            height: 110px;
            
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 10px;
            text-decoration: none;
            color: white;
            transition: transform 0.2s;
        }
        .news-card:hover {
            transform: translateY(-2px);
            border-color: #ccc;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            color: rgb(221, 79, 5);
        }

        /* Título do cartão */
        .news-title {
            font-size: 14px;
            font-weight: 600;
            text-align: center;
            line-height: 1.3;
            
            display: -webkit-box;
            -webkit-line-clamp: 4;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }

        /* Botões de Seta */
        .nav-btn {
            background-color:;
            border: 0px solid #ddd;
            border-radius: 50%;
            width: 32px;
            height: 32px;
            min-width: 32px; /* impede de esmagar */
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 18px;
            color: #555;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            transition: all 0.2s;
            user-select: none;
        }
        .nav-btn:hover {
            background-color:;
            color: #000;
            border-color: ;
        }
        .nav-btn:active {
            transform: scale(0.65);
        }
        
        /* Ajuste para telas muito pequenas (celular): mostra 1 por vez */
        @media (max-width: 600px) {
            .news-card {
                min-width: calc(100% - 5px);
                max-width: calc(100% - 5px);
            }
        }
    </style>
    """

    # JavaScript para mover o carrossel
    javascript = """
    <script>
        function scrollCarousel(direction) {
            const track = document.getElementById('track');
            // Pega a largura visível do container
            const scrollAmount = track.clientWidth;
            
            if (direction === 'left') {
                track.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
            } else {
                track.scrollBy({ left: scrollAmount, behavior: 'smooth' });
            }
        }
    </script>
    """

    # Gera os cartões
    cards_html = ""
    for item in items:
        cards_html += f"""
        <a href="{item['link']}" target="_blank" class="news-card">
            <div class="news-title">{item['title']}</div>
        </a>
        """

    # Monta o HTML final com a estrutura de Wrapper > BotãoEsq > Trilho > BotãoDir
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
    
    # Altura ajustada para caber botões e cartões
    components.html(full_html, height=150, scrolling=False)
