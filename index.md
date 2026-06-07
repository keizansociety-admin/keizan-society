---
layout: home
title: Keizan Society · Daily Home Practice
---

<style>
    :root {
        --bg: #fdfcf8; --surface: #f4f1ea; --text: #2d2d2d; --muted: #6b665f;
        --accent: #4a5d6e; --border: #e0dbd1; --max-width: 70ch;
    }
    body { background-color: var(--bg); color: var(--text); font-family: system-ui, sans-serif; line-height: 1.7; font-size: 20px; margin: 0; padding: 0; }
    .home-container { max-width: var(--max-width); margin: 0 auto; padding: 2rem 1.5rem; }
    
    .site-header { text-align: left; margin-bottom: 3rem; border-bottom: 4px solid var(--accent); padding-bottom: 1rem; }
    .site-header h1 { font-size: 2.2rem; margin: 0; font-weight: 800; color: var(--text); }

    .latest-card { background: var(--surface); padding: 2rem; border-radius: 16px; margin-bottom: 4rem; border: 1px solid var(--border); }
    .latest-label { color: var(--accent); font-weight: 700; font-size: 0.9rem; text-transform: uppercase; display: block; margin-bottom: 0.5rem; }
    .latest-title { font-size: 1.8rem; margin: 0 0 1.5rem 0; }
    
    .start-button { display: inline-block; background: var(--accent); color: #fff !important; padding: 0.8rem 1.5rem; border-radius: 8px; font-weight: 700; text-decoration: none; }
    
    .archive-section h2 { font-size: 1.1rem; text-transform: uppercase; color: var(--muted); letter-spacing: 0.1em; margin-bottom: 1.5rem; }
    .archive-item { padding: 1rem 0; border-bottom: 1px solid var(--border); display: flex; flex-direction: column; }
    .archive-date { font-size: 0.8rem; color: var(--muted); }
    .archive-link { color: var(--text); font-weight: 600; text-decoration: none; }

    footer { margin-top: 6rem; padding-bottom: 4rem; font-style: italic; color: var(--muted); border-left: 3px solid var(--border); padding-left: 1rem; }
</style>

<div class="home-container">

    <header class="site-header">
        <h1>Daily Home Practice</h1>
    </header>

    <main>
        {% for post in site.posts limit:1 %}
            <section class="latest-card">
                <span class="latest-label">Today's Observances</span>
                <h2 class="latest-title">{{ post.title }}</h2>
                <a href="{{ post.url }}" class="start-button">Begin Daily Practice</a>
            </section>
        {% endfor %}
    </main>

    <section class="archive-section">
        <h2>Past Observances</h2>
        <ul class="archive-list">
            {% for post in site.posts offset:1 %}
                <li class="archive-item">
                    <span class="archive-date">{{ post.date | date: "%Y-%m-%d" }}</span>
                    <a href="{{ post.url }}" class="archive-link">{{ post.title }}</a>
                </li>
            {% endfor %}
        </ul>
    </section>

</div>
