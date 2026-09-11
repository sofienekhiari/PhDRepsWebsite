"""Generate the Claude Artifact copy of the website from the published page.

The website in docs/ is a complete HTML document. A Claude Artifact is not: the
file is injected into a wrapper that already supplies the doctype, the html
element, the head and the body, and its content security policy refuses scripts
from unpkg.com, which is where the Claude Design runtime fetches React from.

This script bridges both gaps. It strips the document wrapper, and it prepends a
small map that redirects the runtime's React loads to a CDN the sandbox allows.
Nothing else about the page changes, so the artifact and the live site stay the
same page.

Run it after any edit to docs/index.html, before republishing the artifact:

    python3 build-artifact.py
"""

# only the standard library, so this runs anywhere the repository is checked out
import os
import re

# the page that GitHub Pages publishes, and the single source of truth
SOURCE = "docs/index.html"

# where the artifact copy is written; kept out of docs/ so Pages never serves it
TARGET = "artifact/index.html"

# the runtime's own CDN URLs, and the ones the artifact sandbox will actually load.
# support.js looks each original up in window.__resources by its exact string and
# uses the replacement without a subresource integrity hash when it finds one.
CDN_REDIRECTS = {
    "https://unpkg.com/react@18.3.1/umd/react.production.min.js":
        "https://cdnjs.cloudflare.com/ajax/libs/react/18.3.1/umd/react.production.min.js",
    "https://unpkg.com/react-dom@18.3.1/umd/react-dom.production.min.js":
        "https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.3.1/umd/react-dom.production.min.js",
}

# the name the artifact carries in the browser tab and the gallery. The page's own
# longer title is set at runtime by its helmet block, so this only names the file.
ARTIFACT_TITLE = "PhD Reps Pharmazentrum"


def body_of(document):
    """Pull the page's own markup out of the full HTML document.

    Args:
        document: The complete contents of docs/index.html.

    Returns:
        Everything from the opening <x-dc> tag to the end of the file, with the
        closing </body> and </html> tags removed. That is the part an artifact
        supplies itself; the doctype, html, head and body tags come from the
        wrapper instead.

    Raises:
        ValueError: If the source does not contain an <x-dc> element, which would
            mean the page is no longer a Claude Design component.
    """
    # find where the component markup starts
    start = document.find("<x-dc>")
    # refuse to guess if the page is not shaped the way this script expects
    if start == -1:
        raise ValueError(SOURCE + " has no <x-dc> element")
    # take everything from there to the end, then drop the closing wrapper tags
    return re.sub(r"\s*</body>\s*</html>\s*$", "\n", document[start:])


def shim():
    """Build the script that redirects the runtime's React loads.

    Returns:
        An inline <script> element, as text. It must run before support.js,
        because support.js reads window.__resources the moment it starts loading
        React. Setting this map also stops the runtime re-fetching its own source
        over the network, which in an artifact would return the wrapper page
        rather than this file.
    """
    # one line per redirect, written as a JavaScript object literal
    pairs = ",\n".join('  "%s":\n    "%s"' % (k, v) for k, v in CDN_REDIRECTS.items())
    # wrap it in the script tag the page needs
    return "<script>\nwindow.__resources = {\n" + pairs + "\n};\n</script>"


def build():
    """Write the artifact copy of the page.

    Returns:
        The number of bytes written, so the caller can report something useful.
    """
    # read the published page
    document = open(SOURCE).read()
    # assemble the artifact: its name, the CDN redirect, the runtime, then the page
    parts = [
        "<title>" + ARTIFACT_TITLE + "</title>",
        shim(),
        '<script src="support.js"></script>',
        body_of(document),
    ]
    # make sure the output folder exists before writing into it
    os.makedirs(os.path.dirname(TARGET), exist_ok=True)
    # write the file
    out = "\n".join(parts)
    open(TARGET, "w").write(out)
    # hand the size back
    return len(out)


# run the build when the script is executed directly
if __name__ == "__main__":
    # do the work and say where it went
    print("wrote", TARGET, build(), "bytes")
