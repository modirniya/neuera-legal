#!/usr/bin/env python3
"""Author the Salon Ledger legal documents.

    python3 tools/salonledger.py

Writes salonledger/index.html, salonledger/{privacy,terms}/index.html, their archive pages, and the
dated version file for each, and registers the app in _data/policies.json. Modelled on
tools/rpsmafia.py, and generated for the same reason: the "current" page and its
`versions/<date>.html` snapshot must say exactly the same thing, and keeping two long documents in
step by hand is how they drift apart.

The page chrome matches the site as it stands after the visual redesign (favicon, style.css?v=6,
and `noindex` on dated version files), which is newer than the chrome in tools/rpsmafia.py.

To publish a revision: add a new entry at the top of VERSIONS, set CURRENT and EFFECTIVE to its
date, edit the section bodies, and rerun. The previous version file is left untouched, which is
the point of it.

Everything stated here is checked against what the software actually does. If the app changes what
it collects, this file changes in the same commit.
"""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APP = "salonledger"
APP_NAME = "Salon Ledger"
SITE = "https://legal.neuera.app"

CURRENT = "2026-09-28"
EFFECTIVE = "September 28, 2026"

VERSIONS = {
    "privacy": [
        {
            "version": "2026-09-28",
            "effective_date": EFFECTIVE,
            "summary": "Initial Privacy Policy for Salon Ledger, published during its closed "
                       "pilot. Salon Ledger replaces the paper service-ticket pad in a nail salon: "
                       "the salon owner signs in with an email address, adds techs by name, links "
                       "each tech's phone with a one-time QR code, and techs log their tickets on "
                       "those phones. The policy lists every field the service holds about the "
                       "owner, the techs, the linked phones and the tickets, including the full "
                       "change history kept on every ticket and a per-ticket entry-time "
                       "measurement that exists only for the pilot. It states that nothing is "
                       "collected about the salon's own customers, that no payments are processed, "
                       "and that the app carries no analytics, advertising or crash-reporting SDK. "
                       "It discloses that on Android the QR code is read by Google's ML Kit, which "
                       "processes the camera image on the phone but sends Google its own usage and "
                       "performance metrics. It says plainly that deletion is by email request and "
                       "that pilot sign-in is not yet the production authentication system.",
            "file": f"{CURRENT}.html",
            "highlights": [
                "Business tool: the salon owner is the customer; techs use it at the owner's "
                "invitation and need no account",
                "Every field listed for the owner, techs, linked phones and tickets",
                "Nothing collected about the salon's customers — a ticket has no customer name or "
                "contact",
                "No payments processed; tips are recorded, not handled",
                "Tickets are never deleted by design, and every change is kept with who made it "
                "and when",
                "Per-ticket entry time disclosed as a pilot-only measurement, Tier B under the "
                "NeuEra Data Practices Charter",
                "Camera used only to scan the linking QR code; frames are not stored or sent by us",
                "Google ML Kit on Android disclosed, including the metrics it sends to Google",
                "No analytics SDK, no advertising SDK, no crash reporting, no advertising "
                "identifier",
                "Hosting named: Fly.io, United States (Chicago)",
                "Deletion by email request today; pilot sign-in stated as not yet production "
                "authentication",
            ],
        },
    ],
    "terms": [
        {
            "version": "2026-09-28",
            "effective_date": EFFECTIVE,
            "summary": "Initial Terms of Use for Salon Ledger, covering its closed pilot. The "
                       "agreement is with the salon owner, who invites techs to use it. The "
                       "service is provided as-is during the pilot, features may change, and "
                       "there is no fee. The owner is responsible for the accuracy of tickets and "
                       "totals, for how techs are paid, and for having the right to enter techs' "
                       "names and work records. Totals are a record-keeping aid, not payroll, tax "
                       "or legal advice, and no payments or tips are processed. Owner corrections "
                       "take precedence over tech edits, and every change is kept in the ticket's "
                       "history.",
            "file": f"{CURRENT}.html",
            "highlights": [
                "Agreement is with the salon owner; techs use the app at the owner's invitation",
                "Closed pilot, provided as-is, features may change, no fee during the pilot",
                "Owner responsible for ticket accuracy, totals, and how techs are paid",
                "Owner must have the right to enter techs' names and work records",
                "Totals are a record-keeping aid — not payroll, tax or legal advice",
                "No payments or tips are processed",
                "Owner edits take precedence over tech edits; every change stays in the history",
                "California law, as in the studio's other terms",
            ],
        },
    ],
}


# ==================================================================================================
# Shared chrome — matches the hand-written pages elsewhere on this site.
# ==================================================================================================

def head(title: str, description: str, canonical: str | None, noindex: bool = False,
         body_class: str | None = None) -> str:
    canon = f'\n    <link rel="canonical" href="{canonical}">' if canonical else ""
    robots = '\n    <meta name="robots" content="noindex">' if noindex else ""
    body = f'<body class="{body_class}">' if body_class else "<body>"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">{robots}
    <meta name="description" content="{html.escape(description, quote=True)}">
    <meta property="og:title" content="{html.escape(title, quote=True)}">
    <meta property="og:description" content="{html.escape(description, quote=True)}">
    <title>{html.escape(title)}</title>
    <link rel="icon" href="/assets/img/neuera-icon.png" type="image/png">
    <link rel="apple-touch-icon" href="/assets/img/neuera-icon.png">
    <link rel="stylesheet" href="/assets/css/style.css?v=6">
    <link rel="stylesheet" href="/assets/css/print.css?v=5" media="print">{canon}
</head>
{body}
    <a href="#main" class="skip-link">Skip to content</a>

    <header class="site-header">
        <div class="container">
            <a href="/" class="brand" aria-label="NeuEra Apps home">
                <span class="brand-mark"><img src="/assets/img/neuera-icon.png" alt=""></span>
                <span>NeuEra Apps</span>
            </a>
            <nav class="main-nav" aria-label="Main">
                <a href="/apps/" class="nav-hide-sm">Apps</a>
                <a href="/about/" class="nav-hide-sm">About</a>
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
                        <li><a href="/salonledger/">Salon Ledger</a></li>
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


def effective_of(kind: str, version: str) -> str:
    for v in VERSIONS[kind]:
        if v["version"] == version:
            return v["effective_date"]
    raise KeyError(f"{kind} {version} is not in VERSIONS")


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
    # The document title is <h1>, so its sections are <h2>. The privacy sections carry no numbers
    # of their own, so they are numbered here; the terms sections are numbered in their titles.
    numbered = kind == "privacy"
    body = "\n".join(
        f"""                <section id="{sid}">
                    <h2>{str(i) + ". " if numbered else ""}{html.escape(title)}</h2>
{content}
                </section>
"""
        for i, (sid, title, content) in enumerate(sections, start=1)
    )
    return f"""            <article class="legal-document current-document" data-version="{version}" data-product="{APP}">
                <header class="document-header">
                    <h1>{doc_title}</h1>
                    <div class="document-meta">
                        <span class="version-badge">Version: <time datetime="{version}">{version}</time></span>
                        <span class="effective-date">Effective Date: <time datetime="{version}">{effective_of(kind, version)}</time></span>
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
        head(f"{title} - Version {version}", description,
             f"{SITE}/{APP}/{kind}/versions/{version}.html", noindex=True)
        + breadcrumb(f"{label} {version}")
        + f"""
    <main class="main-content" id="main">
        <div class="container">
            <div class="policy-header">
                <div class="policy-meta">
                    <span class="version-number">Version {version}</span>
                    <span class="effective-date">Effective: {effective_of(kind, version)}</span>
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
    for v in VERSIONS[kind]:
        badge = '<span class="current-badge">Current</span>' if v["version"] == CURRENT else ""
        highs = "\n".join(
            f"                            <li>{html.escape(h)}</li>" for h in v["highlights"]
        )
        entries += f"""                <li class="version-entry">
                    <div class="version-entry__header">
                        <h2><a href="./versions/{v['file']}">Version {v['version']}</a></h2>
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
    """The app's landing page on the legal site, in the product-hero / legal-callout markup every
    other app page uses. There is no "open the app" button: ledger.salon is not live yet, and the
    app is in a closed pilot rather than on either store."""
    return (
        head(f"{APP_NAME} — Legal Documents",
             f"Privacy Policy and Terms of Use for {APP_NAME}, service tickets for nail salons.",
             f"{SITE}/{APP}/", body_class=f"product--{APP}")
        + f"""
    <nav class="breadcrumb" aria-label="Breadcrumb">
        <div class="container">
            <a href="/">Home</a>
            <span class="breadcrumb-sep">/</span>
            <span aria-current="page">{APP_NAME}</span>
        </div>
    </nav>

    <main class="main-content" id="main">
        <section class="product-hero">
            <div class="container">
                <div class="product-hero__head">
                    <span class="product-hero__icon" aria-hidden="true"><img src="/assets/img/salonledger-icon.svg" alt=""></span>
                    <div>
                        <h1>{APP_NAME}</h1>
                        <p class="product-hero__tagline">The service-ticket pad, on the techs' own phones.</p>
                    </div>
                </div>
                <div class="product-hero__body">
                    <p>Service tickets for nail salons. Techs log each ticket on their own phone
                    &mdash; services, prices and an optional tip &mdash; even when the phone is
                    offline. The owner sees every ticket, corrects what needs correcting, closes the
                    pay period and exports each tech's totals. No payments are processed and nothing
                    is recorded about the salon's customers. Currently in a closed pilot.</p>
                    <div>
                        <span class="feature-tag">iOS</span>
                        <span class="feature-tag">Android</span>
                        <span class="feature-tag">Business</span>
                        <span class="feature-tag">Closed pilot</span>
                    </div>
                </div>
                <div class="product-hero__actions">
                    <a href="/data/" class="btn btn--outline">Data Practices Charter</a>
                </div>
            </div>
        </section>

        <section class="section section--alt">
            <div class="container container--narrow">
                <div class="legal-callout">
                    <div>
                        <h2>Legal documents</h2>
                        <p>Current Privacy Policy and Terms of Use, version {CURRENT}, effective
                        {EFFECTIVE} — with the full version history of both.</p>
                    </div>
                    <div class="legal-callout__links">
                        <a href="/{APP}/privacy/" class="btn btn--outline btn--sm">Privacy policy</a>
                        <a href="/{APP}/terms/" class="btn btn--outline btn--sm">Terms of use</a>
                        <a href="/{APP}/privacy/archive.html" class="btn btn--ghost btn--sm">Version history &rarr;</a>
                    </div>
                </div>
            </div>
        </section>
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

MAIL = "<a href=\"mailto:hello@neuera.app\">hello@neuera.app</a>"

PRIVACY = [
    ("introduction", "Introduction", P(
        "Salon Ledger replaces the paper service-ticket pad in a nail salon. Techs log each ticket "
        "on their own phone, and the salon owner sees every ticket, corrects what needs "
        "correcting, and gets each tech's totals for payday. It is made by NeuEra Apps LLC and "
        "runs on iOS and Android.",
        "This policy describes what Salon Ledger records, what it deliberately does not record, "
        "who else is involved, how long things are kept, and what you can ask us to do.",
        "Salon Ledger is in a closed pilot with a small number of salons. Where something is not "
        "finished yet, this policy says so rather than describing an intention as though it were "
        "already true.",
    )),

    ("who-this-covers", "Who This Policy Is About", P(
        "Salon Ledger is a business tool, and three groups of people are involved in different "
        "ways.",
    ) + "\n" + UL(
        "<strong>The salon owner</strong> is our customer. The owner signs in, sets up the salon, "
        "decides which techs use it, and can see and correct every ticket.",
        "<strong>Techs</strong> — employees or contractors of the salon — use Salon Ledger at the "
        "owner's invitation. A tech has no account of their own: the owner adds them by name and "
        "links their phone, and the phone logs their tickets.",
        "<strong>The salon's customers</strong> are not part of it at all. A ticket has no "
        "customer name, phone number, email address or any other customer detail, and has no "
        "field in which to enter one.",
    )),

    ("what-we-collect", "Information We Collect", P(
        "<strong>About the owner.</strong> The email address you sign in with, an identifier for "
        "signing in that is derived from that address, the name of your salon and its time zone. "
        "Each owner account has one salon.",
        "<strong>The salon's setup.</strong> The service menu you create, and the pay periods you "
        "close.",
        "<strong>About techs.</strong> The name and short code (for example, <em>OP3</em>) that "
        "the owner enters for each tech. That is all we hold about a tech as a person.",
        "<strong>About linked phones.</strong> When a phone is linked by QR code we create a "
        "random identifier for it, and record when it was linked, when it last connected, and "
        "whether it has been unlinked. We do not collect the phone's number, its contacts, its "
        "location, or its advertising identifier.",
        "<strong>Tickets.</strong> For each ticket: the services and their prices; a tip amount "
        "if one was entered, marked cash or card; whether the ticket was voided; the time of the "
        "work, as recorded by the phone; the time our server received it; its ticket number; and "
        "how long it took to enter (see <a href=\"#pilot-measurement\">below</a>).",
        "<strong>Ticket history.</strong> Every version of every ticket is kept, together with who "
        "made each change — the owner, or which tech — and when. If a phone sends a change that "
        "the server does not accept, that change is kept too, so the owner can review it.",
        "<strong>Server logs.</strong> Our server's request logs record the method, path, status "
        "and duration of each request. Our hosting provider necessarily processes IP addresses to "
        "deliver traffic to and from the server.",
    )),

    ("on-the-phone", "What Stays on a Tech's Phone", P(
        "Salon Ledger works without a connection, so a linked phone keeps a local database of that "
        "tech's own tickets from the last 45 days, and sends new tickets and changes to our server "
        "when it next connects. A phone holds only the tickets of the tech it is linked to.",
        "The token that lets a linked phone talk to our server is stored in the iOS Keychain or "
        "the Android Keystore, the places each system provides for credentials.",
        "Deleting the app from a phone removes its local database of tickets.",
    )),

    ("what-we-do-not-collect", "What We Do Not Collect", P(
        "This list is specific on purpose, because a general assurance is worth very little.",
    ) + "\n" + UL(
        "<strong>No customer information.</strong> Nothing about the people whose nails were "
        "done: no name, no phone number, no email address, no appointment details.",
        "<strong>No payments.</strong> Salon Ledger does not take or process payments of any "
        "kind, including tips. A tip on a ticket is a record that a tip was given, not a "
        "transaction. There is no card number, bank account or payment processor involved.",
        "<strong>No payroll or tax information.</strong> Salon Ledger adds up tickets. It does not "
        "calculate wages, commission splits, withholding or tax, and does not hold anyone's tax "
        "or bank details.",
        "<strong>No analytics.</strong> The app contains no analytics SDK. We do not measure "
        "screens viewed, sessions or engagement.",
        "<strong>No advertising.</strong> There is no advertising SDK, no ad network, no "
        "advertising identifier and no ads.",
        "<strong>No crash-reporting SDK.</strong>",
        "<strong>No tracking</strong> across other companies' apps or websites.",
        "<strong>No phone number, contacts, location or photos</strong> from a tech's phone. The "
        "camera is used for one thing only — see the next section.",
    )),

    ("camera", "The Camera and QR Code Scanning", P(
        "The camera is used for one purpose: to scan the one-time QR code that links a tech's "
        "phone to the salon. The camera frames are read on the phone to find the code, and are "
        "not stored and not sent to us.",
        "<strong>On iOS</strong>, the code is read by Apple's Vision framework, which is part of "
        "iOS and runs on the phone.",
        "<strong>On Android</strong>, the code is read by Google's ML Kit barcode scanner, which is "
        "built into the app and also runs on the phone. Google states that ML Kit processes the "
        "image on the device and does not send the image, or what it read from it, to Google. "
        "Google also states that ML Kit sends Google metrics about how the scanner performs and "
        "how it is used, together with information about the device and the app, and may contact "
        "Google's servers from time to time for things like fixes and updated models. Google uses "
        "those metrics to measure performance, maintain and improve ML Kit, and detect misuse. "
        "That data goes to Google, not to us, and is handled under Google's own practices rather "
        "than ours.",
        "Your phone will ask for camera permission before the first scan. You can refuse it or "
        "withdraw it in your phone's settings; you would then need another way to link the phone, "
        "and during the pilot the QR code is the only one.",
    )),

    ("charter", "How This Fits Our Data Charter", P(
        "The <a href=\"/data/\">NeuEra Data Practices Charter</a> commits us to attempting every "
        "product question with counted totals that carry no identifier and no timestamp, and to "
        "moving to per-person records only when we can say plainly why a total will not do. It "
        "calls those two categories Tier A and Tier B.",
        "Most of what Salon Ledger holds is Tier B by its nature, and we should say which and why.",
    ) + "\n" + UL(
        "<strong>Tickets and their history</strong> are Tier B because a service ticket is a work "
        "record. A payday total is only worth something if it can be checked against the tickets "
        "behind it, which means each ticket has to say who did the work, what was charged and "
        "when — and a correction has to show what it changed.",
        "<strong>Techs' names and codes</strong> are Tier B because the owner needs to know whose "
        "tickets are whose.",
        "<strong>Linked-phone records</strong> are Tier B because a ticket can only be credited to "
        "the right tech if the server knows which phone sent it, and an owner can only unlink a "
        "lost phone if the server knows it exists.",
        "<strong>The owner's email address</strong> is Tier B because it is how the owner signs "
        "in.",
    ) + "\n" + P(
        "<a id=\"pilot-measurement\"></a><strong>One field exists only for the pilot:</strong> the "
        "time it took to enter each ticket. The pilot is testing whether logging a ticket on a "
        "phone is fast enough to replace the paper pad, and this is how that is measured. It is "
        "stored on the ticket, so it is tied to a tech and a time, and it is Tier B. We are "
        "disclosing it here rather than leaving it to be found.",
        "On Android, ML Kit's own metrics, described in the previous section, are Google's rather "
        "than ours. They are not a bare total, so by the Charter's test they would not qualify as "
        "Tier A.",
    )),

    ("how-we-use", "How We Use It", UL(
        "To sign the owner in, and to link and recognise techs' phones.",
        "To store tickets, keep them in step between a tech's phone and the owner's view, and keep "
        "the history of every change.",
        "To show the owner every ticket, let the owner correct them, close pay periods, and export "
        "each tech's totals.",
        "To measure, during the pilot, how long a ticket takes to enter.",
        "To keep the service running, diagnose faults and prevent abuse.",
        "To reply when you write to us.",
    ) + "\n" + P(
        "We do not use any of it for advertising, we do not sell it, and we do not use it to "
        "train machine-learning models.",
    )),

    ("who-sees-what", "Who Can See What", UL(
        "<strong>The owner</strong> can see and correct every ticket in the salon, and its full "
        "history.",
        "<strong>A tech's phone</strong> holds only that tech's own tickets.",
        "<strong>A CSV export</strong> is a file the owner downloads. Once it is exported, it is "
        "the owner's file, and where it goes after that is outside Salon Ledger.",
        "<strong>We</strong> can access the salon's data to operate the service, investigate a "
        "fault, or act on a request the owner makes of us.",
    )),

    ("legal-bases", "Legal Bases", P(
        "For people in places whose law asks us to name one, we rely on the following.",
    ) + "\n" + UL(
        "<strong>Performance of a contract</strong> for the owner's account, the salon's setup, "
        "and storing and showing the salon's tickets. Without these the service the owner asked "
        "for cannot be delivered.",
        "<strong>Legitimate interests</strong> — the salon's, in keeping accurate work records, "
        "and ours, in running a reliable service — for techs' names and codes, linked-phone "
        "records, ticket history, the pilot entry-time measurement, and server logs.",
        "<strong>Consent</strong> for the camera, which the phone asks for and which can be "
        "withdrawn at any time.",
    ) + "\n" + P(
        "The salon owner decides which techs to add and what is recorded about the salon's work, "
        "and is responsible for having the right to record it. We hold and process those records "
        "to provide the service to the salon.",
    )),

    ("retention", "How Long We Keep It", UL(
        "<strong>Tickets</strong> are never deleted in normal use, by design. Voiding a ticket "
        "marks it void and keeps it, so that a total can always be traced back to what changed "
        "it.",
        "<strong>Ticket history, techs, linked-phone records, and changes the server refused</strong> "
        "— kept for as long as the salon uses the service.",
        "<strong>The owner's account</strong> — kept for as long as the salon uses the service.",
        "<strong>On a tech's phone</strong> — that tech's tickets from the last 45 days.",
    ) + "\n" + P(
        "We should be straightforward about a gap: <strong>there is no in-app way to delete an "
        "account or a salon's data yet.</strong> Deletion is done by asking us at " + MAIL + ". "
        "When a salon owner asks us to close their salon's data, we delete its tickets, its techs "
        "and its linked phones. Otherwise, business records are kept for as long as the salon "
        "uses the service. We will update this section, with a version entry, when in-app "
        "deletion exists.",
    )),

    ("sharing", "Who Else Is Involved", P(
        "We do not sell information, and we do not share it for anyone's advertising. There are no "
        "advertising or analytics companies in this list because there are none in the product.",
    ) + "\n" + UL(
        "<strong>Fly.io</strong> — hosts our server and its Postgres database, in the United "
        "States (Chicago region).",
        "<strong>Google</strong> — on Android only, ML Kit reads the linking QR code on the phone "
        "and sends Google its own metrics, as described in "
        "<a href=\"#camera\">The Camera and QR Code Scanning</a>.",
    ) + "\n" + P(
        "We may also disclose information where the law requires it. In line with the Data "
        "Charter, we do not join Salon Ledger's data with any other NeuEra Apps product; it does "
        "not share an account system or an identifier with any of them.",
    )),

    ("security", "Pilot Status and Security", P(
        "<strong>Sign-in during the pilot is a simplified mechanism built for the pilot. It is not "
        "yet the authentication system Salon Ledger will use in production</strong>, and it should "
        "not be relied on as though it were. We are telling you this so that you can decide what "
        "to record while the pilot lasts. We will update this section, with a version entry, when "
        "that changes.",
        "Connections between the app and our server are encrypted in transit: the server accepts "
        "HTTPS connections only.",
        "On a linked phone, the token that connects it to our server is kept in the iOS Keychain "
        "or Android Keystore. An owner can unlink a phone at any time, for example if it is lost "
        "or a tech leaves. Access to the production database is limited to the people who operate "
        "the service.",
        "No service can promise perfect security, and a pilot less than most.",
    )),

    ("children", "Children", P(
        "Salon Ledger is a business tool for salon owners and the people who work for them. It is "
        "not directed at children, and we do not knowingly collect information about anyone under "
        "13. If you believe we hold such information, write to " + MAIL + " and we will delete it.",
    )),

    ("your-rights", "Your Rights", P(
        "Depending on where you live you may have the right to access the information we hold "
        "about you, to correct it, to delete it, to object to or restrict how we use it, to "
        "receive a copy in a portable form, and to complain to your data protection authority. "
        "Residents of California and other US states with comparable law have similar rights, "
        "including the right not to be discriminated against for exercising them. We do not sell "
        "personal information, so there is nothing to opt out of on that front.",
        "To exercise any of these, write to " + MAIL + ". We will respond within 30 days.",
        "<strong>If you are the owner</strong>, you can already see, correct and export your "
        "salon's records in the app. Deleting your account or your salon's data is done by "
        "asking us.",
        "<strong>If you are a tech</strong>, the records of your work are part of your salon's "
        "business records, which the owner can see and correct. You can write to us to ask what "
        "we hold about you. Where a request would change or remove the salon's records, we will "
        "involve the salon owner, because those records are theirs to keep.",
    )),

    ("international", "Where Information Is Stored", P(
        "We are based in the United States, and Salon Ledger's server and database are hosted "
        "there, in Fly.io's Chicago region. If you use Salon Ledger from outside the United "
        "States, your information is transferred to and processed in the United States.",
    )),

    ("store-disclosures", "App Store Disclosures", P(
        "For Apple's privacy labels and the Google Play Data safety form, the data collected is: "
        "the owner's email address, the names of techs, an identifier for each linked phone, the "
        "ticket records and their history, and the time each ticket took to enter. None of it is "
        "used for advertising or for tracking across other companies' apps and websites. On "
        "Google Play, the form also declares the diagnostics and device information that ML Kit "
        "sends to Google.",
    )),

    ("changes", "Changes to This Policy", P(
        "When this policy changes we publish a new version at a new dated address, leave the old "
        "one online permanently, and write a summary of what changed and why in the "
        "<a href=\"./archive.html\">version history</a>.",
        "For a change that materially affects you, we will tell salon owners before it takes "
        "effect.",
    )),

    ("contact", "Contact", P(
        "NeuEra Apps LLC<br>"
        "Email: " + MAIL + "<br>"
        "Legal documents: <a href=\"https://legal.neuera.app\">legal.neuera.app</a><br>"
        "Salon Ledger's website, www.ledger.salon, is not live yet.",
        "If something in this document does not match what the software actually does, that is a "
        "defect and we want to hear about it.",
    )),
]


# ==================================================================================================
# Terms of Use
# ==================================================================================================

TERMS = [
    ("acceptance", "1. Accepting These Terms", P(
        "These Terms of Use are an agreement between NeuEra Apps LLC and the salon owner who uses "
        "Salon Ledger — and, where the owner signs up on behalf of a business, that business. In "
        "these terms, <strong>\"you\"</strong> means the owner, and <strong>\"techs\"</strong> "
        "means the people the owner invites to log tickets.",
        "By signing in and setting up a salon, you accept these terms. If you do not accept them, "
        "do not use Salon Ledger.",
        "Techs use Salon Ledger at the owner's invitation and do not enter into a separate "
        "agreement with us, but anyone who uses a linked phone must follow "
        "<a href=\"#acceptable-use\">Acceptable Use</a>.",
        "Our <a href=\"/salonledger/privacy/\">Privacy Policy</a> explains what Salon Ledger "
        "records and forms part of this agreement.",
    )),

    ("eligibility", "2. Who May Use It", P(
        "To set up a salon you must be at least 18 years old and able to enter into this agreement "
        "— and, if you are acting for a business, authorised to accept these terms on its behalf.",
        "Salon Ledger is a business tool. It is for recording the work done in a salon, not for "
        "personal use.",
    )),

    ("pilot", "3. The Closed Pilot", P(
        "Salon Ledger is in a closed pilot, open only to salons we have invited. We would rather "
        "say so here than let you discover it.",
        "That means the service is provided as it is. Features may change or be removed, "
        "availability is not guaranteed, and no service level is promised. We may end the pilot, "
        "or your participation in it; when we do, we will try to give you reasonable notice so "
        "that you can export your totals first.",
        "<strong>There is no fee during the pilot.</strong> If Salon Ledger is offered for a fee "
        "later, we will tell you what it costs before anything is charged, and nothing will be "
        "charged without your agreement.",
    )),

    ("service", "4. What Salon Ledger Is, and What It Is Not", P(
        "Salon Ledger replaces the paper service-ticket pad. Techs log tickets on their phones — "
        "the services, their prices, and an optional tip marked cash or card — and you see every "
        "ticket, correct them, close pay periods, and export each tech's totals as a CSV file.",
    ) + "\n" + UL(
        "<strong>It does not process payments.</strong> No money moves through Salon Ledger. A tip "
        "on a ticket is a record that a tip was given; the tip itself is paid and handled by you "
        "and your techs, outside the app.",
        "<strong>It is not payroll.</strong> It adds up tickets. It does not calculate wages, "
        "commission, withholding, overtime or tax, and it does not pay anyone.",
        "<strong>It is not advice.</strong> Totals are a record-keeping aid. They are not "
        "payroll, tax, accounting or legal advice, and you should not treat them as such.",
        "<strong>It does not record your customers.</strong> Tickets have no customer name or "
        "contact. Do not enter customer details anywhere else in the app either, such as in a "
        "service name.",
    )),

    ("account", "5. Your Account and Your Salon", P(
        "You sign in with an email address, and each account has one salon. Keep access to that "
        "email address secure, and do not share your sign-in with anyone.",
        "Sign-in during the pilot is a simplified mechanism, not yet the production "
        "authentication system, as the <a href=\"/salonledger/privacy/#security\">Privacy "
        "Policy</a> explains. Decide what you record with that in mind.",
        "You are responsible for what happens in your salon's account, including on the phones "
        "you link to it.",
    )),

    ("techs", "6. Techs and Linked Phones", P(
        "You add techs by name and link each tech's phone by showing it a one-time QR code. Treat "
        "that code like a key: show it only to the tech whose phone you are linking.",
        "<strong>You are responsible for having the right to enter your techs' names and to "
        "record their work in Salon Ledger</strong>, and for telling your techs that you use it "
        "and what it records. The <a href=\"/salonledger/privacy/\">Privacy Policy</a> sets out "
        "what that is.",
        "If a phone is lost, or a tech stops working with you, unlink the phone. Until you do, "
        "that phone can keep logging tickets to your salon.",
    )),

    ("tickets", "7. Tickets, Corrections and History", P(
        "Tickets can be logged without a connection and are sent to Salon Ledger when the phone "
        "next connects. A ticket is not in your totals until it has arrived.",
        "<strong>Your edits take precedence over a tech's edits.</strong> When you correct a "
        "ticket, your correction stands. <strong>Every change is kept in the ticket's "
        "history</strong> — what changed, who changed it, and when — whether it was made by you "
        "or by a tech.",
        "Tickets are not deleted. A ticket that should not count is voided, which keeps it and "
        "its history. A change sent from a phone that Salon Ledger does not accept is kept for "
        "you to review rather than discarded.",
    )),

    ("responsibilities", "8. Your Responsibilities", P(
        "Salon Ledger records what you and your techs put into it. You are responsible for:",
    ) + "\n" + UL(
        "the accuracy of the tickets in your salon, and of the totals you rely on;",
        "checking totals before you pay anyone from them;",
        "how you pay your techs, and the arrangement you have with each of them;",
        "your obligations as a business — including employment, wage, tip, tax and "
        "record-keeping obligations — which Salon Ledger does not fulfil for you;",
        "keeping your own copies of records you are required to keep, for example by exporting "
        "them.",
    )),

    ("acceptable-use", "9. Acceptable Use", P(
        "Whether you are an owner or a tech, you must not:",
    ) + "\n" + UL(
        "enter information about the salon's customers;",
        "record tickets you know to be false, or alter tickets to mislead anyone about the work "
        "done or the money taken;",
        "use Salon Ledger for anything unlawful;",
        "link a phone, or use a QR code, that you are not entitled to;",
        "attempt to access another salon's data, or anything you are not entitled to see;",
        "attempt to break, overload, reverse engineer or gain unauthorised access to the service;",
        "use Salon Ledger to build a competing product.",
    )),

    ("your-data", "10. Your Salon's Records", P(
        "Your salon's records are yours. You give us permission to store, process and display "
        "them for the purpose of providing Salon Ledger to you, and for nothing else.",
        "You can export each tech's totals as a CSV file at any time. To have your account or "
        "your salon's data deleted, write to <a href=\"mailto:hello@neuera.app\">hello@neuera.app</a>; "
        "there is no in-app deletion yet.",
    )),

    ("ip", "11. Our Rights", P(
        "Salon Ledger — the apps, the server, the software, the name and the design — belongs to "
        "NeuEra Apps LLC. You may use it to run your salon under these terms. You may not copy, "
        "resell, decompile or redistribute it, or present it as your own.",
        "If you send us feedback or suggestions, we may use them without obligation to you.",
    )),

    ("suspension", "12. Suspension and Ending This Agreement", P(
        "You may stop using Salon Ledger at any time, and you may ask us to delete your account "
        "and your salon's data.",
        "We may suspend or end access for a salon, or for a linked phone, if these terms are "
        "breached, if continuing would put the service or other salons at risk, or if we end the "
        "pilot or discontinue the service. Where we reasonably can, we will tell you first.",
        "The sections on your responsibilities, our rights, disclaimers and limitation of "
        "liability survive the end of this agreement.",
    )),

    ("disclaimers", "13. Disclaimers", P(
        "The service is provided \"as is\" and \"as available\", without warranties of any kind, "
        "whether express or implied, including any implied warranty of merchantability, fitness "
        "for a particular purpose, or non-infringement.",
        "We do not promise that Salon Ledger will be uninterrupted, that tickets will always sync "
        "promptly, that totals will be free of errors, or that it will meet any legal or "
        "record-keeping requirement that applies to your business.",
        "Nothing in these terms excludes any liability that cannot lawfully be excluded. Some "
        "jurisdictions do not allow certain exclusions, and where that is the case those "
        "exclusions do not apply.",
    )),

    ("liability", "14. Limitation of Liability", P(
        "To the fullest extent the law allows, NeuEra Apps LLC is not liable for indirect, "
        "incidental, special or consequential losses arising from the use of Salon Ledger — "
        "including lost profits, lost data, errors in tickets or totals, underpayment or "
        "overpayment of anyone, or penalties arising from your business's obligations.",
        "The pilot is free, so there are no fees to refund. Where liability cannot be excluded and "
        "a monetary cap is permitted, our total liability is limited to one hundred US dollars.",
    )),

    ("changes", "15. Changes to These Terms", P(
        "When these terms change we publish a new version at a new dated address, leave the old "
        "one online permanently, and summarise what changed in the "
        "<a href=\"./archive.html\">version history</a>. For a change that materially affects you, "
        "we will tell you before it takes effect. Continuing to use Salon Ledger after that means "
        "you accept the new version.",
    )),

    ("law", "16. Governing Law", P(
        "These terms are governed by the laws of the State of California, United States, without "
        "regard to its conflict of law principles. Where the mandatory law of the place your "
        "business operates gives you protections that cannot be waived by agreement, nothing here "
        "removes them.",
    )),

    ("contact", "17. Contact", P(
        "NeuEra Apps LLC<br>"
        "Email: <a href=\"mailto:hello@neuera.app\">hello@neuera.app</a><br>"
        "Legal documents: <a href=\"https://legal.neuera.app\">legal.neuera.app</a>",
    )),
]


# ==================================================================================================

PRIVACY_TITLE = f"{APP_NAME} Privacy Policy - NeuEra Apps"
PRIVACY_DESC = ("Salon Ledger Privacy Policy — what is recorded about salon owners, techs, linked "
                "phones and tickets, nothing about the salon's customers, no payments processed, "
                "and no analytics or advertising SDK.")
TERMS_TITLE = f"{APP_NAME} Terms of Use - NeuEra Apps"
TERMS_DESC = ("Salon Ledger Terms of Use — the closed pilot, what the owner is responsible for, "
              "why totals are not payroll or tax advice, and how corrections and ticket history "
              "work.")


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
        "description": "Service tickets for nail salons: techs log tickets on their own phones, "
                       "owners get payday totals",
        "privacy": {"current_version": CURRENT, "versions": VERSIONS["privacy"]},
        "terms": {"current_version": CURRENT, "versions": VERSIONS["terms"]},
    }
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("  updated _data/policies.json")


if __name__ == "__main__":
    main()
