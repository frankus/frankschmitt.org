+++
title = "Résumé"
template = "page.html"
description = "Frank Schmitt — senior iOS engineer, 16 years shipping production Swift and Objective-C."

[extra]
layout = "resume"
+++

Senior iOS engineer with 16 years shipping production Swift and Objective-C.
Most recently the technical owner of a customer feedback SDK running inside
consumer apps from CNN, eBay, JetBlue, and Marriott, where I led a ground-up
Objective-C to Swift rewrite and a later migration from Grand Central Dispatch
to structured concurrency. Comfortable owning ambiguous, multi-quarter work end
to end, and working across iOS, Android, and web teams to keep one product
coherent on every platform.

Bellingham, WA · [frank@frankschmitt.org](mailto:frank@frankschmitt.org) ·
[github.com/frankus](https://github.com/frankus) ·
[linkedin.com/in/fschmi](https://www.linkedin.com/in/fschmi)

## Experience

### Senior iOS SDK Developer — Alchemer (acquired Apptentive)
*Remote · 2015–2026*

- Technical owner of ApptentiveKit, the company's iOS SDK, integrated across
  roughly a thousand apps in retail, banking, media, and travel and reaching
  hundreds of millions of devices.
- Led a ground-up rewrite from Objective-C to Swift, shipped 2022 — scoped the
  architecture, sequenced the work over four quarters, and ran both SDKs in
  parallel so existing integrators could migrate on their own timeline.
- Designed the rewritten SDK's consumer-facing UI around MVVM with the view
  models as a published extension point, so integrators needing deep
  customization could supply their own view controllers and drive them with our
  models instead of forking our UI or waiting on another configuration flag.
- Owned the public API surface and distribution: Swift Package Manager and
  CocoaPods, shipped as a pre-built XCFramework under semantic versioning.
  Treated binary and source compatibility as a hard constraint across 30
  releases, since any break cascades into thousands of downstream builds I
  don't control.
- Rewrote the SDK's survey UI in SwiftUI, using Claude Code as the primary
  implementation tool — architecture and review by hand, generation and
  iteration by agent. Completed and pending release.
- Partnered with the product team on ground-up redesigns of Message Center and
  Survey — the end-user-facing surfaces inside every integrator's app — taking
  them from product direction through shipped implementation.
- Worked across team boundaries as the mobile group's cross-platform
  generalist — implemented encryption and decryption of multipart request data
  in the Android SDK in Kotlin, and built and automated the release pipeline for
  our React Native, Flutter, Cordova, and Capacitor plugins.
- Partnered directly with enterprise customers' engineering teams to diagnose
  integration failures inside codebases I couldn't see, turning ambiguous bug
  reports into reproducible cases and API changes.
- Mentored four junior and mid-level engineers through code review, pairing, and
  design feedback.
- Contributed a merged pull request to
  [apple/swift-format](https://github.com/apple/swift-format).

### Software Developer — Moz
*Seattle, WA · 2013–2015*

- Built and shipped consumer-facing iOS apps for local business owners and their
  customers — Objective-C and Swift against a Node.js REST API — taking features
  from loose product hypotheses to App Store release.
- Shipped the official conference app for MozCon 2014 (~1,400 attendees), from
  spec to App Store release against a date that could not move.

### Lead iOS Developer — MacroView Labs / Bally Technologies
*2010–2013*

- Led iOS client architecture for a CMS-driven concierge platform, delivering
  roughly 80 branded apps for hotel, resort, and casino guests from a single
  configurable codebase.

### Earlier

- Web Application Developer, Emergency Reporting (2009–2010)
- Software Engineer, Innuity (1999–2009)
- Controls Engineer, AeroVironment (1997–1998) — embedded software for
  electric-vehicle battery management and fast-charging systems.

## Education

- **Harvey Mudd College** — BS Engineering
- **Western Washington University** — Post-Baccalaureate, Vehicle Design

## Skills

| | |
| --- | --- |
| **Languages** | Swift, Objective-C, Kotlin, JavaScript, C, Ruby |
| **iOS** | UIKit, SwiftUI, Swift Concurrency, Combine, XCTest, Instruments |
| **Distribution** | Swift Package Manager, CocoaPods, XCFramework, semantic versioning, CI/CD |
| **Cross-platform** | React Native, Flutter, Cordova, Capacitor |
| **AI-assisted development** | Claude Code, Xcode agentic coding |
