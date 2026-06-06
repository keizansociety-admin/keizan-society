---
layout: home
title: Daily Practice
---

Welcome to the Keizan Society. Below is the practice schedule for today.

{% for post in site.posts limit:1 %}
  ## [{{ post.title }}]({{ post.url }})
  {{ post.content }}
{% endfor %}

---
### Past Observances
{% for post in site.posts offset:1 %}
* [{{ post.title }}]({{ post.url }})
{% endfor %}
