# student-deals-feed

A list of discounts available to students, as one JSON file. A browser extension
fetches it and shows what's new.

Feed URL:

```
https://raw.githubusercontent.com/DuBearte/student-deals-feed/main/deals.json
```

## Format

`deals.json` holds `version`, `updated` (the date of the last edit) and `deals`, a list
of entries:

| Field | Meaning |
|---|---|
| `id` | Short, unique, never changes (`spotify-premium-student`). The extension uses it to remember what you've seen or ignored. |
| `store` | The company's name as shown. |
| `domain` | The site where the deal applies (`spotify.com`, no `www.`). The extension lights up on it. |
| `deal` | What you get, in one line. Leave exact prices out unless they're stable. |
| `how` | How to claim it: where to verify, which email to use. Never a password or a code tied to one person. |
| `url` | The page that explains or starts the deal. |
| `expires` | `YYYY-MM-DD`, or `null` for standing offers. |
| `updated` | `YYYY-MM-DD` when this entry was last checked. |

## Adding or changing a deal

Edit `deals.json` and open a pull request, or push to `main` if it's your repo. Keep the
`id` of an existing deal; change anything else. Set `updated` to today.

`check.py` runs on every push and once a day. It fails on invalid JSON, a missing or
repeated field, an `id` used twice, or an entry whose `expires` has passed, so stale
deals show up as a red run instead of lingering in the feed. It also warns about any
entry not re-checked in 180 days.

GitHub switches the daily run off after 60 days without a commit; any push turns it
back on. The extension checks `expires` itself too, so the feed job is a reminder, not
the safety net.

```sh
python3 check.py
```

## Sources

Deals are added by hand from the stores' own education pages. There is no scraping of
discount aggregators. Automated sources, when added, run in the daily job and write to
this file through a pull request.
