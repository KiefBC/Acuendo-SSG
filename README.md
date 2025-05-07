# Acuendo - A Python Static Site Generator

<p align="center">
  <img src="Example.gif" alt="Example usage and output of Acuendo" width="600">
</p>

This project is a simple yet powerful Static Site Generator (SSG) written in Python. It takes your content (typically written in Markdown), processes it through templates, and outputs a complete, static HTML website ready for deployment on any web server.

## Features

*   **Markdown-Powered Content:** Write your posts and pages using simple Markdown syntax.
*   **Templating Engine:** Uses Jinja2 for flexible and powerful templating.
*   **Customizable Themes:** Easily change the look and feel by modifying templates and static assets.
*   **Fast Builds:** Generates static files quickly.
*   **No Database Required:** All content is file-based, making it secure and easy to manage.
*   **Simple Deployment:** Deploy the generated `output` (or `dist`, `public`) folder to any static hosting service (like GitHub Pages, Netlify, Vercel, AWS S3, etc.).

## How it Works

This SSG works by:
1.  Reading source content files (e.g., `.md` files from a `content/` directory).
2.  Parsing frontmatter (metadata like title, date, tags) from these files.
3.  Converting Markdown content to HTML.
4.  Applying the HTML content and metadata to a specified template (e.g., `post.html`, `page.html` from a `templates/` directory).
5.  Copying over static assets (CSS, JavaScript, images from a `static/` directory).
6.  Writing the final HTML files and static assets to an output directory (e.g., `output/`).

## Prerequisites

*   Python 3.x (e.g., Python 3.8+ recommended)
*   Pip (Python package installer)

## Installation

1.  **Clone the repository:**
    ```bash
    git https://github.com/KiefBC/Acuendo-SSG.git
    cd Acuendo-SSG
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows
    # venv\Scripts\activate
    # On macOS/Linux
    # source venv/bin/activate
    ```

3.  **Install dependencies:**
    (Not needed yet)
    ```bash
    pip install -r requirements.txt
    ```
    
4. **Generate:**
    ```bash
   ./main.sh
   ```