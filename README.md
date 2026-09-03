# Beyond the Leash with Sandra

The site at [beyondtheleashwithsandra.com](https://beyondtheleashwithsandra.com),
served straight from this repository by GitHub Pages.

Plain static HTML — there is no framework and no install step. Open a `.html`
file, edit it, commit. The one exception is the shared header and footer, below.

## Editing the header or footer

Those two appear on all nine pages, so they live in one place instead of being
copy-pasted nine times:

    _partials/header.html
    _partials/footer.html

After changing either one, run:

```bash
python build.py
```

That stamps the partials into every page and writes finished HTML to disk, which
is the point: the pages stay complete for search engines and for visitors whose
JavaScript does not run. Commit the regenerated pages along with the partial.

To check whether the pages have drifted from the partials without changing
anything (exits non-zero if they have):

```bash
python build.py --check
```

### How it works

Each page marks the region the build owns:

```html
<!-- BUILD:header -->   ...generated, do not hand-edit...   <!-- /BUILD:header -->
```

Anything between those markers is overwritten on the next build. Everything
outside them is yours.

Nav links in the header partial carry `data-nav="home"`, `data-nav="about"` and
so on. `build.py` adds `nav-active` and `aria-current="page"` to whichever one
matches the page being built; the `PAGES` map at the top of the script says
which key each page uses. Blog posts point at `blog`, so the Blog tab stays lit
while reading a post.

**Adding a page:** give it the four marker comments and add it to `PAGES` in
`build.py`, then run the build.

## Previewing locally

```bash
python -m http.server 8000
```

Then open <http://localhost:8000>. A plain file:// open mostly works, but the
homepage pulls the newest post from `blog.html` with `fetch()`, which browsers
block on local files — so use the server if you are checking that card.

## Layout

    index.html, about.html, blog.html, resources.html,
    interviews.html, contact.html, post-*.html   the live pages
    _partials/                shared header and footer (see above)
    build.py                  stamps the partials into the pages
    styles.css, script.js     shared styles and behaviour
    images/                   photographs and the logo
    files/                    superseded drafts, excluded in robots.txt
    CNAME, robots.txt, sitemap.xml
