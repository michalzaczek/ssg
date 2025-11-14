# Static Site Generator

A custom-built static site generator written in Python that converts Markdown files into a fully functional static website.

## Features

- 📝 Converts Markdown to HTML with full support for:
  - Headings (h1-h6)
  - Bold and italic text
  - Links and images
  - Code blocks and inline code
  - Ordered and unordered lists
  - Blockquotes
- 🎨 Template-based page generation
- 🔄 Recursive directory processing
- 🌐 Configurable base path for flexible deployment
- 🚀 GitHub Pages ready

## Project Structure

```
ssg/
├── content/           # Markdown source files
│   ├── index.md      # Main page
│   ├── blog/         # Blog posts
│   └── contact/      # Contact page
├── static/           # Static assets (CSS, images)
├── docs/             # Generated HTML output (for GitHub Pages)
├── src/              # Python source code
│   ├── main.py       # Entry point
│   ├── utilities.py  # Core generation functions
│   ├── textnode.py   # Markdown parsing
│   └── htmlnode.py   # HTML generation
├── template.html     # HTML template
├── build.sh          # Production build script
└── main.sh           # Local development script
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/michalzaczek/ssg.git
cd ssg
```

2. Ensure you have Python 3 installed:
```bash
python3 --version
```

## Usage

### Local Development

Run the site locally with the default basepath (`/`):

```bash
./main.sh
```

This will:
1. Generate the site into the `docs/` directory
2. Start a local server at `http://localhost:8888`

### Production Build

Build the site for GitHub Pages deployment:

```bash
./build.sh
```

This generates the site with the `/ssg/` basepath for GitHub Pages.

### Custom Base Path

You can specify a custom base path for deployment:

```bash
python3 src/main.py /custom-path/
```

## Writing Content

### Creating a New Page

1. Create a new Markdown file in the `content/` directory:
```bash
touch content/my-page.md
```

2. Add content with a required h1 header:
```markdown
# My Page Title

Your content here...
```

3. Rebuild the site to see your changes.

### Markdown Support

The generator supports standard Markdown syntax:

```markdown
# Heading 1
## Heading 2

**Bold text** and *italic text*

[Link text](https://example.com)

![Alt text](/images/photo.jpg)

- Unordered list
- Item 2

1. Ordered list
2. Item 2

> Blockquote

`inline code`

\```
code block
\```
```

## Deployment

### GitHub Pages

1. Push your changes to GitHub:
```bash
git push origin main
```

2. In your GitHub repository settings:
   - Go to Settings → Pages
   - Set Source to "Deploy from a branch"
   - Select branch: `main`
   - Select folder: `/docs`
   - Click Save

3. Your site will be available at: `https://yourusername.github.io/ssg/`

## Testing

Run the test suite:

```bash
cd src
python3 -m unittest discover -s . -p "test_*.py"
```

## How It Works

1. **Markdown Parsing**: The generator reads Markdown files and converts them into an abstract syntax tree (AST) of HTML nodes.

2. **HTML Generation**: Each node type (text, bold, italic, link, etc.) is converted to its HTML equivalent.

3. **Template Injection**: The generated HTML content and extracted title are injected into the template file.

4. **Path Resolution**: All URL paths (`href` and `src` attributes) are prefixed with the configured basepath.

5. **File Output**: The final HTML is written to the `docs/` directory, preserving the original directory structure.

## License

This project was built as part of the [Boot.dev](https://www.boot.dev) "Build a Static Site Generator" course.

## Contributing

This is a learning project, but feel free to fork and experiment with it!

