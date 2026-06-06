---
layout: home
title: Keizan Society · Daily Home Practice
---

<style>
    :root {
        --bg: #fdfcf8;        /* Warm off-white */
        --surface: #f4f1ea;   /* Subtle card background */
        --text: #2d2d2d;      /* Near-black */
        --muted: #6b665f;     /* Muted temple-gray */
        --accent: #4a5d6e;    /* Muted indigo */
        --border: #e0dbd1;
        --focus: #d4af37;     /* Gold focus state */
        --max-width: 70ch;
    }

    /* Global Reset for Home Page */
    body {
        background-color: var(--bg);
        color: var(--text);
        font-family: system-ui, -apple-system, sans-serif;
        line-height: 1.65;
        font-size: 1.2rem;
        margin: 0;
        padding: 2rem 1rem;
    }

    .home-container {
        max-width: var(--max-width);
        margin: 0 auto;
    }

    /* Site Identity Header */
    .site-header {
        text-align: left;
        margin-bottom: 3rem;
        border-bottom: 1px solid var(--border);
        padding-bottom: 2rem;
    }

    .site-header p {
        color: var(--muted);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-size: 0.9rem;
        margin: 0;
    }

    .site-header h1 {
        font-size: 2.5rem;
        margin: 0.5rem 0 0 0;
        font-weight: 600;
        color: var(--text);
    }

    /* Links */
    a {
        color: var(--accent);
        text-decoration: none;
        transition: border-color 0.2s;
        border-bottom: 1px solid transparent;
    }

    a:hover {
        border-bottom: 1px solid var(--accent);
    }

    /* Latest Post Section */
    .latest-practice-meta {
        color: var(--muted);
        font-size: 1rem;
        margin-bottom: 1rem;
        display: block;
    }

    .latest-practice-title {
        font-size: 2rem;
        margin-top: 0;
    }

    /* Archive Section */
    .archive-section {
        margin-top: 5rem;
        padding-top: 2rem;
        border-top: 1px solid var(--border);
    }

    .archive-section h3 {
        color: var(--muted);
        font-size: 1.2rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 1.5rem;
    }

    .archive-list {
        list-style: none;
        padding: 0;
    }

    .archive-list li {
        margin-bottom: 1rem;
    }

    .archive-date {
        color: var(--muted);
        font-size: 0.9rem;
        margin-right: 1rem;
        font-variant-numeric: tabular-nums;
    }

    /* Dyslexia Support: Increase paragraph spacing */
    p { margin-bottom: 1.5rem; }

</style>

<div class="home-container">

    <header class="site-header">
        <p>Keizan Society</p>
        <h1>Daily Home Practice</h1>
    </header>

    <main>
        {% for post in site.posts limit:1 %}
            <article class="latest-post">
                <span class="latest-practice-meta">Today's Practice</span>
                <h2 class="latest-practice-title">
                    <a href="{{ post.url }}">{{ post.title }}</a>
                </h2>
                
                <div class="post-content">
                    {{ post.content }}
                </div>
            </article>
        {% endfor %}
    </main>

    <section class="archive-section">
        <h3>Past Observances</h3>
        <ul class="archive-list">
            {% for post in site.posts offset:1 %}
                <li>
                    <span class="archive-date">{{ post.date | date: "%Y-%m-%d" }}</span>
                    <a href="{{ post.url }}">{{ post.title }}</a>
                </li>
            {% endfor %}
        </ul>
    </section>

    <footer style="margin-top: 5rem; color: var(--muted); font-size: 0.9rem; padding-bottom: 4rem;">
        <p><em>May this practice benefit all beings throughout the triple world.</em></p>
    </footer>

</div>
