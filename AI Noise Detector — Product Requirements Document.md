# AI Noise Detector — Product Requirements Document

Nov 10, 2026 · @Muhammed Roshan

## Overview

AI Noise Detector listens to an environment through a phone, laptop or small sensor, detects unwanted noise in real time, and tells the user what it is, how loud it is and when it happened. Version 1 targets noise disputes and quality control in shared spaces: apartments, offices, classrooms and call-centre floors.

**Problem.** Noise complaints today rest on memory and a basic decibel meter. A meter reports volume but not source, so users cannot show that a barking dog, a drill or a party caused the disturbance, and cannot separate it from normal background sound.

**Vision.** A private, on-device assistant that turns raw sound into a clear, evidence-ready log of noise events, without storing recordings of conversations.

## Goals and non-goals

V1 succeeds if users can trust the detector enough to act on its logs.

**Goals**

- Detect and label at least 12 common noise classes with 90% precision on the validation set
- Run fully on-device with under 300 ms detection latency
- Produce an exportable noise log (time, duration, level in dB, class, confidence) in under 3 taps
- Reach 70% week-4 retention among users who complete calibration

**Non-goals for v1**

- Speech transcription or identifying who is speaking
- Legal-grade certified sound measurement (we will not claim calibration to IEC 61672 standards)
- Active noise cancellation or noise removal from audio
- Locating the physical direction of a source (multi-microphone arrays come later)

## Target users

Three personas drive v1, in priority order.

| Persona | Context | Key need | Primary use case |
| --- | --- | --- | --- |
| Renter or homeowner | Apartment or housing society with noisy neighbours or construction | Evidence for a landlord, society committee or authority | Overnight monitoring with an exportable log |
| Office or facility manager | Open-plan office, co-working space, school | Find recurring noise hotspots and times | Daily noise report per room |
| Remote worker or student | Home study or call setup | Know when background noise will disturb a call | Live alert before or during a meeting |

## User stories

| # | As a... | I want to... | So that... | Priority |
| --- | --- | --- | --- | --- |
| 1 | Renter | start overnight monitoring with one tap | I capture disturbances while I sleep | P0 |
| 2 | Renter | see each event labelled (dog, drilling, music, shouting) with dB level and time | I can show exactly what happened | P0 |
| 3 | Renter | export the log as a PDF or CSV | I can send it to my landlord or authority | P0 |
| 4 | Any user | get an alert when noise passes my threshold for a set duration | I react in time | P1 |
| 5 | Any user | calibrate against my room's normal background level | alerts ignore ordinary sound | P1 |
| 6 | Facility manager | view noise by room, hour and day | I find recurring problems | P1 |
| 7 | Any user | listen to a short clip of a flagged event and delete it | I verify detections while keeping control of my audio | P2 |
| 8 | Any user | mark a detection as wrong | the model improves for my environment | P2 |

## Functional requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| FR-1 | Capture audio continuously from the device microphone in 1-second frames, with foreground and background modes | P0 |
| FR-2 | Detect noise events and classify each into one of at least 12 classes (traffic, construction, music, barking, shouting, appliance, alarm, footsteps, door slam, machinery, crowd, other) | P0 |
| FR-3 | Show a live sound level in dB(A) with the current top class and confidence | P0 |
| FR-4 | Log every event with start time, duration, peak and average dB, class and confidence | P0 |
| FR-5 | Export the log as PDF and CSV, with a summary page (total events, loudest event, hours over threshold) | P0 |
| FR-6 | Let the user set threshold (dB), minimum duration and quiet hours; send a push alert when exceeded | P1 |
| FR-7 | Guide a 30-second room calibration that sets the adaptive background baseline | P1 |
| FR-8 | Show a dashboard of events by hour, day and class, with filters | P1 |
| FR-9 | Save an optional 10-second clip around an event, off by default, with one-tap delete | P2 |
| FR-10 | Accept a thumbs-up or thumbs-down on each detection to feed model evaluation | P2 |
| FR-11 | Provide an API and webhook for sending events to facility systems | P2 |
| FR-12 | Delete all data from the device and account in one action | P0 |

## AI and model requirements

The model must classify short audio frames accurately on a mid-range phone without sending audio off the device.

| Area | Requirement |
| --- | --- |
| Architecture | Log-mel spectrogram features into a compact audio classifier (for example a MobileNet or audio transformer variant), quantized to INT8 |
| Size and speed | Under 25 MB on disk; under 300 ms end-to-end latency on a mid-range Android phone; under 5% battery per hour in background mode |
| Accuracy (v1) | Macro precision of at least 90% and recall of at least 85% across the 12 classes on a held-out set recorded in at least 6 environment types |
| False alarms | Fewer than 1 false event per hour in a quiet room |
| Training data | Public sets such as AudioSet and ESC-50 (check each licence), plus consented, labelled recordings from pilot users |
| Robustness | Evaluate across microphones, distance, reverberation and overlapping sounds; test with background music and speech present |
| Calibration | Adaptive baseline per room; report confidence scores and suppress labels below 60% confidence as "other" |
| Monitoring | Track weekly precision from user feedback, and retrain when precision drops 5 points or more on any class |
| Fairness and privacy | No speech content retained or transcribed; voice detected only as a class, never as identity |

## Non-functional requirements

| Category | Requirement |
| --- | --- |
| Privacy | Audio is processed on-device; raw audio never leaves the phone unless the user saves and shares a clip |
| Compliance | Explicit microphone consent screen; comply with GDPR, India's DPDP Act and local recording laws; show a notice that recording others may need consent |
| Security | Encrypt logs at rest (AES-256) and in transit (TLS 1.3); account data stored separately from event logs |
| Performance | App cold start under 2 seconds; dashboard loads 30 days of data in under 1 second |
| Reliability | Continuous monitoring for 10 hours without crash; recover automatically after a call or app interruption |
| Accessibility | WCAG 2.1 AA; alerts offered as visual, vibration and sound |
| Platforms | Android 10+ and iOS 16+ at launch; web dashboard for managers |
| Localization | English at launch; Hindi and Malayalam in the first update |
| Offline | Full detection and logging with no internet; sync when connected |

## User experience and key flows

A new user should reach a first detection in under 2 minutes.

1. **Onboarding.** Explain what is and is not recorded, request microphone permission, choose a use case (night monitoring, office, call).
2. **Calibration.** Stay quiet for 30 seconds; the app sets a baseline and shows it as a line on the live meter.
3. **Monitoring.** One large start button; the live screen shows dB, the current class and a running event count. A dim screen mode saves battery overnight.
4. **Alerts.** A push notification names the class, level and duration; tapping it opens the event.
5. **Review.** The timeline lists events; the user can confirm, correct or dismiss each one.
6. **Export.** Choose a date range, then share a PDF or CSV.

## Success metrics

| Type | Metric | Target at 90 days after launch |
| --- | --- | --- |
| Activation | Users who complete calibration and start monitoring | 60% of installs |
| Engagement | Users running 3+ monitoring sessions per week | 35% of active users |
| Retention | Week-4 retention | 30% overall, 70% among calibrated users |
| Outcome | Users who export at least one log | 25% of active users |
| Model quality | Precision from user feedback | 90% or higher |
| Model quality | False events per quiet hour | Under 1 |
| Trust | Share of users who enable clip saving | Under 15% (a sign that on-device labels are trusted) |
| Business | Paid conversion on manager plan | 4% of manager sign-ups |

## Technical architecture

&#91;embedded content: architecture · on-device pipeline, optional cloud\]

Raw audio is classified on the device; only event logs sync to an optional cloud service for accounts, the web dashboard and integrations.

## Release plan and milestones

&#91;embedded content: release roadmap · 3 phases, 2 gates\]

Week counts are a proposal for a small team and should be confirmed once engineering has sized the work. Success metrics are reviewed 90 days after GA.

## Risks, assumptions and open questions

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Phone microphones differ, so dB readings are off | High | Medium | Label readings "approximate"; offer per-device calibration with a reference meter |
| Misclassification weakens trust in exported logs | Medium | High | Show confidence, allow correction, tune the 60% threshold in the pilot |
| Background recording breaks on iOS or Android battery limits | High | High | Test OS limits in week 1; fall back to a plug-in, screen-on mode |
| Recording laws and consent vary by region | Medium | High | Legal review before launch; consent notice in the app |
| Public training data has licence limits | Medium | Medium | Audit licences; build a consented in-house dataset |

**Assumptions.** Most users will monitor with a phone placed in one room; users accept on-device labels as evidence for informal disputes.

**Open questions**

- Is the first market India only, or global from launch?
- Do managers need a dedicated hardware sensor, or is a phone enough?
- What is the pricing model: free tier for individuals and paid plans for facilities?
- Do we need a certified measurement mode for legal use in v2?
