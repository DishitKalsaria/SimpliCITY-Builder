# Link-first use and fallbacks

Pasting the SimpliCITY Builder repository URL is **not installation**. It works only with an AI app that can retrieve repository source files, read a résumé, execute Python, and return generated files. Other hosts can follow the instructions or write code but cannot automatically deliver a tested website.

## Retrieval order for capable AI assistants

1. Try the repository: `https://github.com/DishitKalsaria/SimpliCITY-Builder` and follow `AI_START_HERE.md`.
2. If GitHub HTML browsing is blocked, try the raw text entry point: `https://raw.githubusercontent.com/DishitKalsaria/SimpliCITY-Builder/main/AI_START_HERE.md`. You still need the **full repo** for execution; the raw instructions alone are insufficient.
3. Where a terminal is available, execute `git clone https://github.com/DishitKalsaria/SimpliCITY-Builder.git` and read files locally.
4. Or download `https://github.com/DishitKalsaria/SimpliCITY-Builder/archive/refs/heads/main.zip` and extract in the execution workspace.
5. If neither retrieval method works, ask the user to upload the [Skill ZIP](https://github.com/DishitKalsaria/SimpliCITY-Builder/releases) or project archive; never guess the generator code or claim to have run it.

## Prompt to copy

```text
Use SimpliCITY Builder from https://github.com/DishitKalsaria/SimpliCITY-Builder.
If the GitHub page cannot be read, use the raw AI_START_HERE.md URL or git clone.
Read the attached résumé and create an interactive downloadable index.html in
my imagined world: [DESCRIBE ANY WORLD]. Preserve facts and private details.
Validate the JSON and SVG, build the HTML, and browser-test it if available.
Tell me what you could not verify.
```

The skill supports **arbitrary** worlds. The output is a 2D/2.5D interactive website, not a unique game engine for every request. With a scanned PDF or résumé tables, extraction may be incomplete; review before publishing. Do not put private résumés in GitHub Issues.
