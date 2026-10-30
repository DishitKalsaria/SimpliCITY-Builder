# Security and privacy

SimpliCITY Builder processes potentially sensitive career information. Do not post private résumés, personal phone numbers, addresses, access tokens or secrets in GitHub Issues.

To report a security vulnerability, use the GitHub repository's private vulnerability reporting feature if enabled or contact the maintainer using the public contact methods on [Dishit Kalsaria's GitHub profile](https://github.com/dishitkalsaria). Do not publish exploit details before a fix can be evaluated.

Generated portfolios are standalone offline HTML, without tracking or outgoing network calls. Public link fields are validated to http(s) URLs; user-provided text is HTML escaped. Optional original SVG artwork is restricted to a safe subset. These defenses do not replace careful review before publishing. Uploaded résumé handling is governed by the chosen AI host, not by this script.


SVG gradients in v0.2.0 accept only `url(#localGradientId)` references to definitions inside the same SVG. Remote URLs, script, external href, filters and event handlers remain disallowed. The résumé extractor writes private text to a gitignored directory by default and does not upload files. Never commit generated portfolios based on a real résumé without explicit authorization.
