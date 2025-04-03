import streamlit as st
import streamlit.components.v1 as components
import requests
from utils.style_loader import load_bare_css

# Get data items from API
@st.cache_data(ttl=6400)  
def fetch_tech_news():
    api_key = st.secrets["NEWS_KEY"]
    url = ('https://newsapi.org/v2/top-headlines?'
       'category=technology&'
       'language=en&'
       'apiKey=' + api_key)
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("articles", [])
    else:
        st.error("Failed to fetch news")
        return []

# Dynamically display carousel items
def display_carousel():
    articles = fetch_tech_news()
    if not articles:
        st.write("No news available at the moment 😔")
        return

    carousel_items = ""
    for i, article in enumerate(articles):
        active_class = "active" if i == 0 else ""
        image_url = article.get("urlToImage") or "https://via.placeholder.com/800x400?text=No+Image"
        title = article.get("title", "No Title")
        description = article.get("description", "")
        article_url = article.get("url", "#")

        carousel_items += f"""
        <div class="carousel-item {active_class}">
          <div class="img-container">
            <a href="{article_url}" target="_blank">
              <img src="{image_url}" class="d-block w-100 carousel-img" alt="{title}">
            </a>
          </div>
          <div class="carousel-caption">
            <h5>{title}</h5>
            <p>{description}</p>
          </div>
        </div>
        """

    css_content = load_bare_css()

    carousel_html = f"""
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>{css_content}</style>
    <div id="carouselComponent" class="carousel slide" data-ride="carousel">
      <div class="carousel-inner">{carousel_items}</div>
      <a class="carousel-control-prev" href="#carouselComponent" role="button" data-slide="prev">
        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
        <span class="sr-only">Previous</span>
      </a>
      <a class="carousel-control-next" href="#carouselComponent" role="button" data-slide="next">
        <span class="carousel-control-next-icon" aria-hidden="true"></span>
        <span class="sr-only">Next</span>
      </a>
    </div>
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.2/dist/js/bootstrap.bundle.min.js"></script>
    """
    components.html(carousel_html, height=510)