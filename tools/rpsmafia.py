#!/usr/bin/env python3
"""Author the RPS Mafia legal documents.

    python3 tools/rpsmafia.py

Writes rpsmafia/index.html, rpsmafia/{privacy,terms}/index.html, their archive pages, and the
dated version file for each. The rest of this site is hand-maintained HTML; this app is generated
for one reason — the "current" page and its `versions/<date>.html` snapshot must be byte-identical
in substance, and keeping two 30 KB documents in step by hand is how they drift apart.

To publish a revision: add a new entry at the top of VERSIONS, set CURRENT to its date, edit the
section bodies, and rerun. The previous version file is left untouched, which is the point of it.

Everything stated here is checked against what the software actually does. If the app changes what
it collects, this file changes in the same commit.
"""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APP = "rpsmafia"
APP_NAME = "RPS Mafia"
SITE = "https://legal.neuera.app"

CURRENT = "2026-09-08"
EFFECTIVE = "September 8, 2026"

VERSIONS = {
    "privacy": [
        {
            "version": "2026-09-08",
            "effective_date": "September 8, 2026",
            "summary": "Documents the age check the app now shows before anything else. A new "
                       "\"How we check your age\" section describes what is asked, what happens "
                       "to the answer, and what happens if it is below the minimum age. The "
                       "important detail is what is NOT done: the date of birth is used once to "
                       "work out an age and is then discarded, is never stored, and never leaves "
                       "the device — only the outcome is kept, and only locally. The Children "
                       "section is rewritten to describe the check rather than only the "
                       "prohibition, and the do-not-collect list now says explicitly that a date "
                       "of birth is not among the things we hold. No other practice changed, and "
                       "nothing new is collected by this release.",
            "file": "2026-09-08.html",
            "highlights": [
                "New section: how the age check works and what happens to the answer",
                "The date of birth is discarded after the check — not stored, never transmitted",
                "Only the outcome is remembered, on the device, and a refusal is permanent",
                "Children section rewritten around the check rather than the prohibition alone",
                "Do-not-collect list now names date of birth explicitly",
                "No new collection of any kind in this release",
            ],
        },
        {
            "version": "2026-09-07",
            "effective_date": EFFECTIVE,
            "summary": "Initial Privacy Policy for RPS Mafia, published before the game leaves "
                       "early access. Documents the account system (anonymous by default, with "
                       "optional Google or Apple sign-in), the scheduling records that game "
                       "nights require, the reliability counters derived from them, optional "
                       "push reminders, and the player reports and blocks that moderation "
                       "depends on. States plainly that voice is relayed live through a server "
                       "we operate ourselves and is never recorded, stored or transcribed, and "
                       "that game state exists only in memory and is destroyed when the game "
                       "ends. Lists every sub-processor by name. Confirms the app carries no "
                       "analytics SDK, no advertising SDK, no crash reporter and no advertising "
                       "identifier.",
            "file": "2026-09-07.html",
            "highlights": [
                "Accounts are anonymous by default; Google or Apple sign-in is optional and "
                "exists only to carry progress between devices",
                "Voice is relayed live through our own server and is never recorded, stored or "
                "transcribed",
                "Game state lives in memory only and is destroyed when the game ends",
                "Game-night attendance and reliability counters disclosed as Tier B under the "
                "NeuEra Data Practices Charter, with the reason each field exists",
                "Player reports store the report text and both player identifiers, because "
                "moderation cannot work without them",
                "Push reminder tokens are stored only while reminders are on and deleted when "
                "they are turned off",
                "No analytics SDK, no advertising SDK, no advertising identifier, no crash "
                "reporting",
                "Sub-processors named: Google (Firebase Authentication and Cloud Messaging) and "
                "Fly.io (application, database and voice hosting)",
                "Account deletion available on request today; in-app deletion is being built",
            ],
        },
    ],
    "terms": [
        {
            "version": "2026-09-08",
            "effective_date": "September 8, 2026",
            "summary": "The age section now describes the check rather than only stating the "
                       "requirement. It sets out that the app asks for a date of birth before "
                       "anything else, that an answer below the minimum age ends access on that "
                       "device and is not asked again, and that misstating your age is a breach "
                       "of these terms. No other term changed.",
            "file": "2026-09-08.html",
            "highlights": [
                "Age section describes the check, not just the requirement",
                "An answer below the minimum age is final on that device",
                "Misstating your age is stated as a breach",
                "No other term changed",
            ],
        },
        {
            "version": "2026-09-07",
            "effective_date": EFFECTIVE,
            "summary": "Initial Terms of Use for RPS Mafia. Sets a minimum age of 13, describes "
                       "what the service is and what it is not, and sets out the conduct rules "
                       "for a game played by live voice between people who may be strangers. "
                       "Covers accounts, game nights and the fact that a night can be cancelled "
                       "when too few players arrive, the reporting and blocking system and how "
                       "enforcement works, and states that the service is free with nothing to "
                       "buy and no advertising. Notes that the game is in early access and is "
                       "offered as-is.",
            "file": "2026-09-07.html",
            "highlights": [
                "Minimum age 13, and higher where local law requires it",
                "Conduct rules written for live voice between strangers, not generic boilerplate",
                "Reporting, blocking and enforcement described, including what a report contains",
                "Game nights may be cancelled when too few players arrive; replacements offered",
                "Free with no purchases, no advertising and nothing that can be paid for",
                "Early access stated plainly: games may end, data may be reset, features may change",
                "Deliberate disruption of other players' games is grounds for removal",
            ],
        },
    ],
}


# ==================================================================================================
# Shared chrome — matches the hand-written pages elsewhere on this site.
# ==================================================================================================

def head(title: str, description: str, canonical: str | None) -> str:
    canon = f'\n    <link rel="canonical" href="{canonical}">' if canonical else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{html.escape(description, quote=True)}">
    <meta property="og:title" content="{html.escape(title, quote=True)}">
    <meta property="og:description" content="{html.escape(description, quote=True)}">
    <title>{html.escape(title)}</title>
    <link rel="stylesheet" href="/assets/css/style.css?v=3">
    <link rel="stylesheet" href="/assets/css/print.css?v=3" media="print">{canon}
</head>
<body>
    <a href="#main" class="skip-link">Skip to content</a>

    <header class="site-header">
        <div class="container">
            <a href="/" class="brand" aria-label="NeuEra Apps home">
                <span class="brand-mark"><img src="/assets/img/neuera-icon.png" alt=""></span>
                <span>NeuEra Apps</span>
            </a>
            <nav class="main-nav" aria-label="Main">
                <a href="/apps/">Apps</a>
                <a href="/about/">About</a>
                <a href="/legal/" class="active">Legal</a>
                <a href="/contact/" class="btn btn--outline btn--sm">Contact</a>
            </nav>
        </div>
    </header>
"""


def breadcrumb(last: str) -> str:
    return f"""
    <nav class="breadcrumb" aria-label="Breadcrumb">
        <div class="container">
            <a href="/">Home</a>
            <span class="breadcrumb-sep">/</span>
            <a href="/legal/">Legal</a>
            <span class="breadcrumb-sep">/</span>
            <a href="/legal/#{APP}">{APP_NAME}</a>
            <span class="breadcrumb-sep">/</span>
            <span aria-current="page">{last}</span>
        </div>
    </nav>
"""


FOOTER = """
    <footer class="site-footer">
        <div class="container">
            <div class="footer-grid">
                <div class="footer-col footer-brand">
                    <a href="/" class="brand" style="margin-bottom: var(--space-3);">
                        <span class="brand-mark"><img src="/assets/img/neuera-icon.png" alt=""></span>
                        <span>NeuEra Apps</span>
                    </a>
                    <p>An independent app studio based in the United States.</p>
                </div>
                <div class="footer-col">
                    <h4>Apps</h4>
                    <ul>
                        <li><a href="/netcloak/">NetCloak VPN</a></li>
                        <li><a href="/playlounge/">Play Lounge</a></li>
                        <li><a href="/rpsmafia/">RPS Mafia</a></li>
                        <li><a href="/odometer/">Odo</a></li>
                        <li><a href="/kalum/">Kalum</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h4>Studio</h4>
                    <ul>
                        <li><a href="/about/">About</a></li>
                        <li><a href="/contact/">Contact</a></li>
                        <li><a href="/legal/">Legal</a></li>
                        <li><a href="/data/">Data Practices</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h4>Elsewhere</h4>
                    <ul>
                        <li><a href="https://apps.apple.com/us/developer/neuera-apps/id1895216844" rel="noopener" target="_blank">App Store</a></li>
                        <li><a href="https://play.google.com/store/apps/developer?id=NeuEra+Apps" rel="noopener" target="_blank">Google Play</a></li>
                        <li><a href="mailto:hello@neuera.app">hello@neuera.app</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <span>&copy; 2026 NeuEra Apps LLC. All rights reserved.</span>
                <span>Built independently in the United States.</span>
            </div>
        </div>
    </footer>

    <script src="/assets/js/toc.js?v=2" defer></script>
</body>
</html>
"""


def toc(sections: list[tuple[str, str, str]]) -> str:
    items = "\n".join(
        f'                        <li><a href="#{sid}">{html.escape(title)}</a></li>'
        for sid, title, _ in sections
    )
    return f"""                <nav class="table-of-contents" id="toc" aria-label="Table of Contents">
                    <h3>Table of Contents</h3>
                    <ol>
{items}
                    </ol>
                </nav>
"""


def article(kind: str, sections: list[tuple[str, str, str]], version: str) -> str:
    doc_title = f"{APP_NAME} {'Privacy Policy' if kind == 'privacy' else 'Terms of Use'}"
    # House style on this site: numbered <h3> section headings, <h2> reserved for the document
    # title. The privacy sections carry no numbers of their own, so they are numbered here.
    numbered = kind == "privacy"
    body = "\n".join(
        f"""                <section id="{sid}">
                    <h3>{str(i) + ". " if numbered else ""}{html.escape(title)}</h3>
{content}
                </section>
"""
        for i, (sid, title, content) in enumerate(sections, start=1)
    )
    return f"""            <article class="legal-document current-document" data-version="{version}" data-product="{APP}">
                <header class="document-header">
                    <h2>{doc_title}</h2>
                    <div class="document-meta">
                        <span class="version-badge">Version: <time datetime="{version}">{version}</time></span>
                        <span class="effective-date">Effective Date: <time datetime="{version}">{EFFECTIVE}</time></span>
                    </div>
                </header>

{toc(sections)}
{body}            </article>
"""


def current_page(kind: str, sections, title, description) -> str:
    label = "Privacy Policy" if kind == "privacy" else "Terms of Use"
    return (
        head(title, description, f"{SITE}/{APP}/{kind}/")
        + breadcrumb(label)
        + f"""
    <main class="main-content" id="main">
        <div class="container">
            <div class="policy-header">
                <div class="policy-meta">
                    <span class="current-badge">Current Version</span>
                    <div class="version-info">
                        <span class="version-number">Version {CURRENT}</span>
                        <span class="effective-date">Effective: {EFFECTIVE}</span>
                    </div>
                </div>
                <div class="policy-actions">
                    <a href="./archive.html" class="btn btn-secondary">View Version History</a>
                    <button onclick="window.print()" class="btn btn-outline">Print {label}</button>
                </div>
            </div>

"""
        + article(kind, sections, CURRENT)
        + """        </div>
    </main>
"""
        + FOOTER
    )


def version_page(kind: str, sections, title, description, version: str) -> str:
    label = "Privacy Policy" if kind == "privacy" else "Terms of Use"
    return (
        head(f"{title} - Version {version}", description, None)
        + breadcrumb(f"{label} {version}")
        + f"""
    <main class="main-content" id="main">
        <div class="container">
            <div class="policy-header">
                <div class="policy-meta">
                    <span class="version-number">Version {version}</span>
                    <span class="effective-date">Effective: {EFFECTIVE}</span>
                </div>
                <div class="policy-actions">
                    <a href="../" class="btn btn-secondary">Current Version</a>
                    <a href="../archive.html" class="btn btn-outline">All Versions</a>
                </div>
            </div>

"""
        + article(kind, sections, version)
        # A version file sits one level deeper than the current page, so the in-body
        # "./archive.html" cross-reference would resolve inside versions/ and 404.
        .replace('href="./archive.html"', 'href="../archive.html"')
        + """        </div>
    </main>
"""
        + FOOTER
    )


def archive_page(kind: str) -> str:
    label = "Privacy Policy" if kind == "privacy" else "Terms of Use"
    entries = ""
    for i, v in enumerate(VERSIONS[kind]):
        badge = '<span class="current-badge">Current</span>' if v["version"] == CURRENT else ""
        highs = "\n".join(
            f"                            <li>{html.escape(h)}</li>" for h in v["highlights"]
        )
        entries += f"""                <li class="version-entry">
                    <div class="version-entry__header">
                        <h3><a href="./versions/{v['file']}">Version {v['version']}</a></h3>
                        {badge}
                    </div>
                    <p class="effective-date">Effective: {v['effective_date']}</p>
                    <p>{html.escape(v['summary'])}</p>
                    <ul>
{highs}
                    </ul>
                </li>
"""
    return (
        head(f"{APP_NAME} {label} — Version History",
             f"Every published version of the {APP_NAME} {label}, with a summary of what changed "
             f"in each and why.", f"{SITE}/{APP}/{kind}/archive.html")
        + breadcrumb(f"{label} History")
        + f"""
    <main class="main-content" id="main">
        <div class="container">
            <h1>{APP_NAME} {label} — Version History</h1>
            <p>Every version we have published, newest first. Superseded versions stay online at a
            permanent address so that a policy you agreed to can always be read back exactly as it
            stood.</p>
            <ol class="version-list">
{entries}            </ol>
            <p><a href="./" class="btn btn-secondary">Read the current {label}</a></p>
        </div>
    </main>
"""
        + FOOTER
    )


def app_index() -> str:
    return (
        head(f"{APP_NAME} — Legal Documents",
             f"Privacy Policy and Terms of Use for {APP_NAME}, the free browser Mafia game with "
             f"voice built in.", f"{SITE}/{APP}/")
        + f"""
    <nav class="breadcrumb" aria-label="Breadcrumb">
        <div class="container">
            <a href="/">Home</a>
            <span class="breadcrumb-sep">/</span>
            <span aria-current="page">{APP_NAME}</span>
        </div>
    </nav>

    <main class="main-content" id="main">
        <div class="container">
            <h1>{APP_NAME}</h1>
            <p>A free social deduction game played by voice in the browser, for five to twelve
            players. Reserve a seat at a scheduled game night or start a private table with a code.
            Available at <a href="https://rpsociety.app" rel="noopener">rpsociety.app</a>.</p>

            <div class="policy-cards">
                <article class="policy-card">
                    <h2><a href="./privacy/">Privacy Policy</a></h2>
                    <p class="effective-date">Version {CURRENT} &middot; Effective {EFFECTIVE}</p>
                    <p>What the game records, what it does not, and why. Voice is relayed live and
                    never recorded. Game state is destroyed when the game ends.</p>
                    <p><a href="./privacy/">Read</a> &middot;
                       <a href="./privacy/archive.html">Version history</a></p>
                </article>
                <article class="policy-card">
                    <h2><a href="./terms/">Terms of Use</a></h2>
                    <p class="effective-date">Version {CURRENT} &middot; Effective {EFFECTIVE}</p>
                    <p>The rules for playing, the conduct expected in a game played out loud with
                    strangers, and how reports and blocks work.</p>
                    <p><a href="./terms/">Read</a> &middot;
                       <a href="./terms/archive.html">Version history</a></p>
                </article>
            </div>

            <p>{APP_NAME} is covered by the studio-wide
            <a href="/data/">NeuEra Data Practices Charter</a>, which explains the test we apply
            before any measurement is built. Where the Charter and this app's Privacy Policy
            differ, the Privacy Policy governs.</p>
        </div>
    </main>
"""
        + FOOTER
    )


# ==================================================================================================
# Privacy Policy
# ==================================================================================================

P = lambda *ps: "\n".join(f"                    <p>{p}</p>" for p in ps)
UL = lambda *ls: ("                    <ul>\n"
                  + "\n".join(f"                        <li>{l}</li>" for l in ls)
                  + "\n                    </ul>")

PRIVACY = [
    ("introduction", "Introduction", P(
        "RPS Mafia is a social deduction game you play in a web browser with five to twelve other "
        "people, talking to each other by voice. It is made by NeuEra Apps LLC and is available at "
        "<a href=\"https://rpsociety.app\" rel=\"noopener\">rpsociety.app</a>.",
        "This policy describes what the game records about you, what it deliberately does not "
        "record, who else is involved, and what you can ask us to do. It covers the game itself "
        "and the website around it.",
        "The game is in early access. Where something is still being built, this policy says so "
        "rather than describing an intention as though it were already true.",
    )),

    ("what-we-collect", "Information We Collect", P(
        "<strong>Your account.</strong> You are signed in anonymously the first time you open the "
        "game, which creates an identifier for you and nothing else — no email address, no name, "
        "nothing you typed. You may optionally sign in with Google or Apple so that your progress "
        "follows you between devices. If you do, we receive the account identifier that Google or "
        "Apple issues for you. We never receive or store your password.",
        "<strong>The name you choose.</strong> You pick a nickname, which other players at your "
        "table can see. Choose one you are comfortable being known by; there is no requirement "
        "that it be your real name, and we would gently suggest it should not be.",
        "<strong>Game nights.</strong> If you reserve a seat at a scheduled game, we record which "
        "slot you reserved, whether you were present when it opened, and whether you were seated "
        "at a table. From those we keep two running counts — games you were seated in, and times "
        "you showed up — and a reliability standing derived from them.",
        "<strong>Reminders.</strong> If you ask to be reminded before a game night starts, we "
        "store the notification token your device issues and which platform it came from. That is "
        "what a reminder is delivered to. Turn reminders off and the token is deleted.",
        "<strong>Reports and blocks.</strong> If you report another player, we store who reported, "
        "who was reported, and the reason you wrote. If you block someone, we store that pair so "
        "the two of you are not seated together again.",
        "<strong>Voice.</strong> While you are in a game your microphone audio is relayed live "
        "through a server we operate. It is not recorded, not stored, not transcribed and not "
        "listened to. See <a href=\"#voice\">Voice</a> below.",
        "<strong>Server logs.</strong> Our servers keep ordinary operational logs, which include "
        "network-level information such as IP addresses. They exist to keep the service running "
        "and to investigate faults and abuse.",
    )),

    ("what-we-do-not-collect", "What We Do Not Collect", P(
        "This list is specific on purpose, because a general assurance is worth very little.",
    ) + "\n" + UL(
        "<strong>No analytics.</strong> The game contains no analytics SDK. We do not measure "
        "screens viewed, sessions, funnels or engagement.",
        "<strong>No advertising.</strong> There is no advertising SDK, no ad network, and no "
        "advertising identifier is read. There are no ads in the game.",
        "<strong>No crash reporting SDK.</strong>",
        "<strong>No voice recordings.</strong> Audio is relayed and discarded, never written down.",
        "<strong>No contacts, location, photos, or files.</strong> The game never asks for them.",
        "<strong>No payment information.</strong> The game is free and there is nothing to buy, so "
        "there is no card, no billing address and no transaction history.",
        "<strong>No marketing list.</strong> We do not collect email addresses and will not send "
        "you marketing.",
        "<strong>No chat transcripts.</strong> The game is played by voice; there is no text chat "
        "to keep.",
        "<strong>No date of birth.</strong> You are asked for one once, to check your age. It is "
        "used for that and discarded — see below.",
    )),

    ("charter", "How This Fits Our Data Charter", P(
        "The <a href=\"/data/\">NeuEra Data Practices Charter</a> commits us to attempting every "
        "product question with counted totals that carry no identifier and no timestamp, and to "
        "moving to per-person records only when we can say plainly why a total will not do. It "
        "calls those two categories Tier A and Tier B.",
        "RPS Mafia holds Tier B data, and we should say exactly which and why, because the Charter "
        "is worth nothing if the app quietly ignores it.",
    ) + "\n" + UL(
        "<strong>Your account identifier</strong> is Tier B because a game that seats you at a "
        "table with the same people, remembers a block you made, and lets your progress follow you "
        "to another device cannot do any of that against an anonymous total.",
        "<strong>Game-night attendance</strong> is Tier B because the whole feature is a promise "
        "that a table will be full when you arrive. Reserving a seat you do not take costs seven "
        "other people their game, so the system has to know whether you came.",
        "<strong>Reports and blocks</strong> are Tier B because a report that cannot name who was "
        "reported is not a report, and a block that does not know who you blocked cannot keep you "
        "apart.",
        "<strong>Reminder tokens</strong> are Tier B for the plainest reason there is: a "
        "notification has to be delivered to a particular device.",
    ) + "\n" + P(
        "We do not keep per-event behavioural records beyond these. There is no log of which "
        "screens you visited, how long you looked at them, or what you did inside a game.",
    )),

    ("how-we-use", "How We Use It", P(
        "Every use below is one of the four things named above doing the job it exists for.",
    ) + "\n" + UL(
        "To sign you in and keep you signed in.",
        "To seat you at a table, show your nickname to the other players, and run the game.",
        "To hold your reservation for a game night, and to build full tables from the players who "
        "actually arrived.",
        "To send the reminder you asked for, and to tell you when your table is ready.",
        "To act on reports, to keep blocked players apart, and to remove people who make the game "
        "unpleasant for everyone else.",
        "To keep the service running, diagnose faults, and prevent abuse.",
    ) + "\n" + P(
        "We do not use any of it to profile you for advertising, to score you for anything outside "
        "the game, or to train machine-learning models.",
    )),

    ("legal-bases", "Legal Bases", P(
        "For people in the United Kingdom, the European Economic Area and other places with "
        "comparable law, we rely on the following bases.",
    ) + "\n" + UL(
        "<strong>Performance of a contract</strong> for your account, your nickname, seating you "
        "at a table and running your game night reservation. Without these the service you asked "
        "for cannot be delivered.",
        "<strong>Consent</strong> for push reminders and for the microphone. Both are optional, "
        "both are asked for, and both can be withdrawn at any time.",
        "<strong>Legitimate interests</strong> for reports, blocks, reliability standing, server "
        "logs and abuse prevention — our interest, and every other player's, in a game that is not "
        "ruined by a few people. You may object to processing on this basis; see "
        "<a href=\"#your-rights\">Your Rights</a>.",
    )),

    ("voice", "Voice", P(
        "Voice is the whole point of the game, so it deserves to be described precisely.",
        "Your microphone audio travels to a voice server that we run ourselves, on our own "
        "infrastructure, and is relayed from there to the other players at your table. It is "
        "<strong>never recorded, stored, transcribed, analysed or listened to by us</strong>. When "
        "the game ends, the audio has already ceased to exist — there is nothing kept to delete.",
        "The software we run for this is LiveKit. We operate our own instance of it, which means "
        "your audio is not sent to LiveKit the company.",
        "The game decides who is able to speak and when, because that is a rule of Mafia: during a "
        "night, the table is silent. That control is about gameplay, not about listening. Your "
        "browser will ask for microphone permission before any of this happens, and you can refuse "
        "or revoke it at any time in your browser or device settings.",
        "One thing we cannot control, and you should know it: other players hear your voice live, "
        "and nothing prevents a person from recording their own screen or audio. Treat a voice "
        "game with strangers the way you would treat any live call with people you do not know.",
    )),

    ("retention", "How Long We Keep It", P(
        "Different things live for very different lengths of time.",
    ) + "\n" + UL(
        "<strong>Voice audio</strong> — never stored at all.",
        "<strong>Game state</strong> — held in memory while the game runs and destroyed when it "
        "ends. It is never written to a database.",
        "<strong>Reminder tokens</strong> — until you turn reminders off, sign out, or the device "
        "token stops working, whichever comes first.",
        "<strong>Game-night reservations and attendance</strong> — kept while your account exists, "
        "because your reliability standing is derived from them.",
        "<strong>Reports and blocks</strong> — kept while your account exists. A block that expired "
        "would defeat its purpose, and a report we deleted could not inform a decision later.",
        "<strong>Server logs</strong> — short-lived operational retention.",
    ) + "\n" + P(
        "We should be straightforward about a gap: the game does not yet delete old records "
        "automatically on a schedule. Deletion happens when you ask for it. We are building a "
        "retention routine and will update this section, with a version entry, when it ships.",
    )),

    ("sharing", "Who Else Is Involved", P(
        "We do not sell your information, and we do not share it for anyone else's advertising. "
        "There are no advertising or analytics companies in this list because there are none in "
        "the product.",
        "These are the companies that process data on our behalf so the service can work:",
    ) + "\n" + UL(
        "<strong>Google</strong> — Firebase Authentication issues and verifies your sign-in, and "
        "Firebase Cloud Messaging delivers reminders if you turn them on. If you choose to sign in "
        "with Google, Google necessarily knows you did.",
        "<strong>Apple</strong> — if, and only if, you choose Sign in with Apple.",
        "<strong>Fly.io</strong> — hosts the game server, the database and the voice server.",
    ) + "\n" + P(
        "We may also disclose information where the law requires it, or where it is necessary to "
        "investigate a credible threat to someone's safety. We have no interest in doing so beyond "
        "those cases.",
        "In line with the Data Charter, we do not join this data with any other NeuEra Apps "
        "product. RPS Mafia does not share an account system or an identifier with Play Lounge, "
        "Kalum, Odo or NetCloak, and we have not built the means to connect them.",
    )),

    ("age-check", "How We Check Your Age", P(
        "The first time you open the game it asks for your date of birth, before anything else "
        "happens.",
        "<strong>The answer is used once and then discarded.</strong> The game works out how old "
        "you are, keeps the answer to that question — old enough, or not — and forgets the date. "
        "The date of birth is never written to storage, never sent to our servers, and never seen "
        "by us. What is remembered is a single word on your own device, and nothing else.",
        "If the date puts you below the minimum age, the game says so and stops there. That "
        "outcome is remembered on that device and you are not asked again, because a check you can "
        "retry until it passes is not a check.",
        "We should be plain about what this is and is not. It is a declared-age check: it asks, and "
        "it believes you. Anyone determined to type a different year will get through, and no "
        "self-declared check has ever prevented that. What it does is keep the game closed to a "
        "child who answered honestly, which is the case that actually happens, and it means we are "
        "not quietly relying on never having asked.",
    )),

    ("children", "Children", P(
        "RPS Mafia is not for children under 13, and you must be at least 13 to use it. In parts "
        "of the European Economic Area the minimum age for consent to online services is higher, "
        "and where that is the case, that higher age applies to you.",
        "The reason is specific rather than legalistic: this is a live voice game played with "
        "people you have not met, in which lying convincingly is the object. That is not a "
        "suitable environment for a child.",
        "This is enforced by the age check described above, which every player passes before "
        "reaching the game. We do not knowingly collect information from anyone under 13, and a "
        "player whose answer puts them below that age never gets as far as an account. If you "
        "believe a child is using the game anyway, write to "
        "<a href=\"mailto:hello@neuera.app\">hello@neuera.app</a> and we will delete the account.",
    )),

    ("security", "Security", P(
        "Connections to the game and the website are encrypted in transit. Sign-in is handled by "
        "Firebase Authentication rather than by us, so there is no password of yours for us to "
        "store or to lose. Access to the production database is restricted to the people who "
        "operate the service.",
        "No service can promise perfect security, and we will not pretend otherwise. What we can "
        "say is that the most sensitive thing in a voice game — the audio — is never written down "
        "anywhere, so it cannot be taken from us.",
    )),

    ("your-choices", "Your Choices", P() + UL(
        "<strong>Stay anonymous.</strong> Signing in with Google or Apple is optional. The game is "
        "fully playable without it.",
        "<strong>Choose your nickname.</strong> It does not have to be your name.",
        "<strong>Refuse the microphone.</strong> Your browser will ask, and you can say no or "
        "change your mind later in browser or device settings.",
        "<strong>Turn reminders off.</strong> The stored token is deleted when you do.",
        "<strong>Block someone.</strong> You will not be seated with them again.",
        "<strong>Delete your account.</strong> See below.",
    )),

    ("your-rights", "Your Rights", P(
        "Depending on where you live you may have the right to access the information we hold "
        "about you, to correct it, to delete it, to object to or restrict how we use it, to "
        "receive a copy in a portable form, and to complain to your data protection authority. "
        "Residents of California and other US states with comparable law have similar rights, "
        "including the right not to be discriminated against for exercising them. We do not sell "
        "personal information, so there is nothing to opt out of on that front.",
        "To exercise any of these, write to "
        "<a href=\"mailto:hello@neuera.app\">hello@neuera.app</a>. We will respond within 30 days.",
        "<strong>Account deletion.</strong> Today this is done by asking us, and we will delete "
        "your account and the records tied to it. An in-app delete button is being built and this "
        "section will be updated when it ships. One limit worth stating in advance: if you have "
        "been reported by another player, we may keep the minimum record needed to enforce a ban, "
        "because a system where deleting your account erases the complaints against you is a "
        "system that protects the wrong person.",
    )),

    ("international", "Where Your Information Goes", P(
        "We are based in the United States and our servers are operated there. If you use the game "
        "from outside the United States, your information is transferred there and processed under "
        "US law. Where transfers out of the United Kingdom or European Economic Area require a "
        "safeguard, we rely on the Standard Contractual Clauses that our providers offer.",
    )),

    ("store-disclosures", "App Store Disclosures", P(
        "For the Google Play Data Safety form and Apple's privacy labels, the data types "
        "associated with you are: an account identifier, the nickname you choose, your game-night "
        "attendance records, the reports and blocks you create, and a notification token if you "
        "enable reminders. Audio is collected in the sense that it passes through our server, and "
        "is <strong>not stored</strong>. No data is used for advertising or for tracking across "
        "other companies' apps and websites.",
    )),

    ("changes", "Changes to This Policy", P(
        "When this policy changes we publish a new version at a new dated address, leave the old "
        "one online permanently, and write a summary of what changed and why in the "
        "<a href=\"./archive.html\">version history</a>. A superseded policy stays readable so "
        "that the terms you agreed to can always be checked.",
        "For a change that materially affects you, we will give notice in the app before it takes "
        "effect.",
    )),

    ("contact", "Contact", P(
        "NeuEra Apps LLC<br>"
        "Email: <a href=\"mailto:hello@neuera.app\">hello@neuera.app</a><br>"
        "Legal documents: <a href=\"https://legal.neuera.app\">legal.neuera.app</a><br>"
        "The game: <a href=\"https://rpsociety.app\" rel=\"noopener\">rpsociety.app</a>",
        "If something in this document does not match what the software actually does, that is a "
        "defect and we want to hear about it.",
    )),
]


# ==================================================================================================
# Terms of Use
# ==================================================================================================

TERMS = [
    ("acceptance", "1. Accepting These Terms", P(
        "These Terms of Use are an agreement between you and NeuEra Apps LLC covering RPS Mafia, "
        "the game at <a href=\"https://rpsociety.app\" rel=\"noopener\">rpsociety.app</a>, and the "
        "website around it. By playing, you accept them.",
        "If you do not accept them, the remedy is simple: do not play. There is no account to "
        "cancel and nothing to pay.",
        "Our <a href=\"/rpsmafia/privacy/\">Privacy Policy</a> explains what the game records and "
        "forms part of this agreement.",
    )),

    ("age", "2. Age", P(
        "You must be at least 13 years old. Where the law in your country sets a higher minimum "
        "age for consenting to online services, that higher age applies to you instead.",
        "This is a live voice game played with people you have not met, in which convincing "
        "deception is the object. We would rather state a real reason than a legal formula: it is "
        "not a suitable place for a child.",
        "<strong>The game asks for your date of birth before anything else.</strong> If your answer "
        "puts you below the minimum age, that is the end of it on that device — the game says so, "
        "remembers it, and does not ask again. The date itself is not kept; see the "
        "<a href=\"/rpsmafia/privacy/#age-check\">Privacy Policy</a>.",
        "Giving a false date of birth to get past that check is a breach of these terms.",
    )),

    ("service", "3. What the Service Is", P(
        "RPS Mafia is a free social deduction game for five to twelve players, played in a browser "
        "with live voice. A server runs the game: it deals the roles, runs the night, resolves "
        "every action and decides who may speak and when. There is no human narrator and no "
        "moderator sitting out of the game.",
        "You can play in two ways. Start a private table and share its code with people you "
        "already know, or reserve a seat at a scheduled game night and be matched with other "
        "players who did the same.",
        "<strong>The service is free.</strong> There is nothing to buy, no subscription, no "
        "currency, no cosmetics and no advantage of any kind that can be paid for. There is no "
        "advertising.",
    )),

    ("early-access", "4. Early Access", P(
        "The game is in early access, and we would rather say so here than let you discover it.",
        "That means features may change or be removed, games may end unexpectedly, scheduled "
        "nights may not run, and we may reset data during development. Availability is not "
        "guaranteed and there is no service level promised. The service is provided as it is.",
    )),

    ("accounts", "5. Your Account", P(
        "You are signed in anonymously when you first play. You may optionally link a Google or "
        "Apple account so your progress follows you to another device.",
        "You are responsible for what happens under your account. Do not share it, and do not use "
        "someone else's. Do not attempt to impersonate another player, and do not choose a "
        "nickname designed to make people believe you are someone you are not.",
        "You may stop at any time. To have your account and its records deleted, write to "
        "<a href=\"mailto:hello@neuera.app\">hello@neuera.app</a>.",
    )),

    ("conduct", "6. How to Behave", P(
        "Mafia is a game about lying. That is the point, and nothing below is meant to interfere "
        "with it. Bluffing, misleading, accusing and betraying other players inside the game are "
        "the game.",
        "What follows is about the difference between playing a character and treating a person "
        "badly. While you are connected to a table you must not:",
    ) + "\n" + UL(
        "Harass, threaten or intimidate anyone.",
        "Use slurs, or abuse anyone on the basis of race, ethnicity, nationality, religion, "
        "gender, sexual orientation, disability or age.",
        "Say anything sexual to or about a player, or anything sexual involving minors under any "
        "circumstances.",
        "Share another person's private information, or your own contact details with strangers.",
        "Broadcast noise, music or audio designed to make the table unusable, or hold the "
        "microphone open to stop other people being heard.",
        "Record or republish another player's voice without their agreement.",
        "Deliberately ruin games — reserving seats you do not intend to take, leaving repeatedly "
        "part-way through, or throwing games to spite other players.",
        "Use software to automate play, interfere with the game, or gain any advantage.",
        "Attempt to break, overload or gain unauthorised access to the service.",
    ) + "\n" + P(
        "The short version: argue with the character, not the person.",
    )),

    ("voice-rules", "7. Voice", P(
        "Voice is live and is not recorded by us. Other players hear you as you speak.",
        "Two things follow from that, and both are your decision to make. Anything you say can be "
        "heard by strangers, so do not say things you would not want a stranger to hear. And "
        "although recording another player without their agreement is against these terms, we "
        "cannot prevent someone from doing it on their own device. Treat a table of strangers the "
        "way you would treat any live call with people you do not know.",
        "Your browser will ask before your microphone is used, and you can refuse or withdraw that "
        "permission at any time.",
    )),

    ("reports", "8. Reports, Blocks and Enforcement", P(
        "If a player behaves badly you can report them. A report records who was reported, who "
        "reported them, and the reason you wrote. Reports are read by a person.",
        "You can also block a player, which is separate from reporting and needs no justification. "
        "Blocked players are not seated at the same table as you again.",
        "Do not file false reports. A report is a call on somebody else's time and standing, and "
        "using it to punish a player for beating you is itself a breach of these terms.",
        "Where a breach is established we may warn, suspend or permanently remove an account, and "
        "may do so without notice where the behaviour is serious. If your account is removed for "
        "abuse, we may keep the minimum record needed to enforce that removal, as explained in the "
        "<a href=\"/rpsmafia/privacy/#your-rights\">Privacy Policy</a>.",
    )),

    ("game-nights", "9. Game Nights", P(
        "A game night is a scheduled table you reserve a seat at. Reserving is a commitment to "
        "turn up, because seven other people are relying on it.",
        "You are seated only if you are present when the table opens. A night that too few players "
        "attend is cancelled rather than run badly, and you will be offered the next slots with "
        "room in them. We do not guarantee that any particular night will run, or that you will be "
        "seated at a particular table.",
        "The game keeps a record of the nights you reserved and attended, and a reliability "
        "standing derived from it. Repeatedly reserving seats you do not take may affect how you "
        "are matched.",
    )),

    ("content", "10. What You Contribute", P(
        "You keep whatever rights you have in the things you supply — your nickname, your voice, "
        "and the text of any report you file. You give us permission to use them for the purpose "
        "they were given for: showing your nickname to your table, relaying your voice to the "
        "other players, and reading your report in order to act on it.",
        "You are responsible for what you say and write. Do not supply anything you do not have "
        "the right to supply.",
    )),

    ("ip", "11. Our Rights", P(
        "The game, the website, the software, the name RPS Mafia, the crest and the written "
        "material on rpsociety.app belong to NeuEra Apps LLC.",
        "You may play the game and read the site. You may not copy, resell, decompile or "
        "redistribute the software, or present the game as your own.",
        "Mafia as a parlour game is a folk tradition that belongs to nobody, and the rules of "
        "social deduction are not ours to own. What is ours is this implementation of it, and the "
        "specific rules, roles and balance that RPS Mafia plays by.",
    )),

    ("disclaimers", "12. Disclaimers", P(
        "The service is provided \"as is\" and \"as available\", without warranties of any kind, "
        "whether express or implied, including any implied warranty of merchantability, fitness "
        "for a particular purpose, or non-infringement.",
        "We do not promise that the service will be uninterrupted, that games will always start, "
        "that voice will always work, or that it will be free of errors.",
        "<strong>We do not control other players.</strong> The game puts you in a voice "
        "conversation with people we have not vetted. We remove people who behave badly when we "
        "learn of it, and we give you tools to report and block, but we cannot promise that "
        "everyone you meet will behave well.",
        "Nothing in these terms excludes any liability that cannot lawfully be excluded, including "
        "for death or personal injury caused by negligence, or for fraud. Some jurisdictions do "
        "not allow certain exclusions, and where that is the case those exclusions do not apply to "
        "you.",
    )),

    ("liability", "13. Limitation of Liability", P(
        "To the fullest extent the law allows, NeuEra Apps LLC is not liable for indirect, "
        "incidental, special or consequential losses arising from your use of the service, nor for "
        "lost data, lost games, or the conduct of other players.",
        "The service is free, so there are no fees to refund. Where liability cannot be excluded "
        "and a monetary cap is permitted, our total liability is limited to one hundred US "
        "dollars.",
    )),

    ("termination", "14. Ending This Agreement", P(
        "You may stop playing at any time, and you may ask us to delete your account.",
        "We may suspend or end your access if you breach these terms, or if we discontinue the "
        "service. Because the service is free, we do not owe compensation for doing so.",
        "The sections on what you contribute, our rights, disclaimers and limitation of liability "
        "survive the end of this agreement.",
    )),

    ("changes", "15. Changes to These Terms", P(
        "When these terms change we publish a new version at a new dated address, leave the old "
        "one online permanently, and summarise what changed in the "
        "<a href=\"./archive.html\">version history</a>. For a change that materially affects you, "
        "we will give notice in the app before it takes effect. Continuing to play after that "
        "means you accept the new version.",
    )),

    ("law", "16. Governing Law", P(
        "These terms are governed by the laws of the State of California, United States, without "
        "regard to its conflict of law principles. If you are a consumer resident elsewhere, you "
        "keep the benefit of any mandatory protections of your own country's law, and nothing here "
        "removes them.",
    )),

    ("contact", "17. Contact", P(
        "NeuEra Apps LLC<br>"
        "Email: <a href=\"mailto:hello@neuera.app\">hello@neuera.app</a><br>"
        "Legal documents: <a href=\"https://legal.neuera.app\">legal.neuera.app</a><br>"
        "The game: <a href=\"https://rpsociety.app\" rel=\"noopener\">rpsociety.app</a>",
    )),
]


# ==================================================================================================

PRIVACY_TITLE = f"{APP_NAME} Privacy Policy - NeuEra Apps"
PRIVACY_DESC = ("RPS Mafia Privacy Policy — anonymous accounts by default, voice relayed live and "
                "never recorded, game state destroyed when the game ends, and no analytics or "
                "advertising SDK of any kind.")
TERMS_TITLE = f"{APP_NAME} Terms of Use - NeuEra Apps"
TERMS_DESC = ("RPS Mafia Terms of Use — who may play, how to behave in a voice game with "
              "strangers, how reports and blocks work, and what early access means.")


def w(rel: str, text: str) -> None:
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    print(f"  wrote {rel}")


def main() -> None:
    w(f"{APP}/index.html", app_index())

    w(f"{APP}/privacy/index.html",
      current_page("privacy", PRIVACY, PRIVACY_TITLE, PRIVACY_DESC))
    w(f"{APP}/privacy/versions/{CURRENT}.html",
      version_page("privacy", PRIVACY, PRIVACY_TITLE, PRIVACY_DESC, CURRENT))
    w(f"{APP}/privacy/archive.html", archive_page("privacy"))

    w(f"{APP}/terms/index.html", current_page("terms", TERMS, TERMS_TITLE, TERMS_DESC))
    w(f"{APP}/terms/versions/{CURRENT}.html",
      version_page("terms", TERMS, TERMS_TITLE, TERMS_DESC, CURRENT))
    w(f"{APP}/terms/archive.html", archive_page("terms"))

    # Register the app in the shared metadata file.
    meta_path = ROOT / "_data" / "policies.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    meta[APP] = {
        "name": APP_NAME,
        "description": "Free browser social deduction game with voice, for 5 to 12 players",
        "privacy": {"current_version": CURRENT, "versions": VERSIONS["privacy"]},
        "terms": {"current_version": CURRENT, "versions": VERSIONS["terms"]},
    }
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("  updated _data/policies.json")


if __name__ == "__main__":
    main()
