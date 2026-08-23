# Contributing to Frontage

Thanks for taking a look. Frontage has a lot of headroom for new business/portfolio/
dashboard types, palettes, and AI providers, so contributions of any size are
welcome.

## Getting set up

Follow the [README's setup steps](README.md#-quick-start) to get the backend and
frontend running locally. Run `python selftest.py` in `backend/` before you start
changing things, and again before opening a PR - it works without any API key
set and exercises every type across all three site kinds.

## Ways to contribute

- **Add a type.** Add an entry to `BUSINESS_TYPES`, `PORTFOLIO_TYPES`, or
  `DASHBOARD_TYPES` (in `backend/business_types.py`, `portfolio_types.py`, or
  `dashboard_types.py`): a label, an inline SVG icon, and fallback copy. Business
  types also need a layout (`grid`/`list`) and a schema.org `schema_type`. No
  template changes required.
- **Add a palette.** Add an entry to `PALETTES` in `backend/palettes.py` with six
  CSS variables, described in the README.
- **Add an AI provider.** Add a `_call_<provider>` function to
  `backend/services/ai_provider.py` following the existing Anthropic/OpenAI/Gemini
  pattern, then register it in `_CALLERS`, `PROVIDER_ORDER`, `DEFAULT_MODELS`, and
  `PROVIDER_DISPLAY_NAMES`.
- **Improve a template.** `backend/templates_data/` has one shared template per
  kind. Changes there affect every site of that kind, so check the result across a
  few types and palettes before opening a PR.
- **Fix a bug or improve the UI.** Issues tagged `good first issue` are a
  reasonable place to start if one exists; otherwise open an issue first for
  anything non-trivial so we're aligned before you put in the work.

## Before opening a PR

- Run `python selftest.py` in `backend/`.
- Run `npm run build` in `frontend/`.
- Test against at least one real type + palette combination per kind you touched.
- Keep PRs focused. Small, single-purpose changes are much easier to review than a
  bundle of unrelated fixes.
- Describe what changed and why. A screenshot or short clip is appreciated for
  anything UI-facing.

## Reporting bugs / requesting features

Use the issue templates under **New Issue**. The more specific the repro steps, the
faster it gets fixed.

## Code style

- Python: standard library style, minimal dependencies. If you're adding a new one,
  explain why in the PR.
- JavaScript: plain React with hooks, no extra state management library. Keep
  components focused; if a component is doing three unrelated things, it's probably
  three components.
- Comments should explain *why*, not narrate *what* the next line obviously does.

## License

By contributing, you agree your contributions will be licensed under the project's
[MIT License](LICENSE).
