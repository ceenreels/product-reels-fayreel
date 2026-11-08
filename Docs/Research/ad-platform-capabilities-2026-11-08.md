# Ad platform capabilities for short-drama monetization

Research date and source access date: **2026-11-08**. Scope: public first-party documentation only; native Android/iOS (including Flutter), desktop Web and mobile Web/H5. No advertising accounts, SDKs, component repositories, or campaigns were changed. These are capability findings, not an architecture decision or revenue forecast. **Fact** means documented by the named provider; **inference** means a proposed implication. Vendor marketing claims do not establish expected Fayreel performance.

## Findings that affect the choice

- **Fact:** MAX's official Flutter repository identifies Android and iOS as its platforms. A Flutter integration is not a Flutter Web integration. Its public format guides cover interstitial, rewarded and native ads; no dedicated rewarded-interstitial Flutter format/API was established in the sources reviewed. [Official MAX Flutter repository](https://github.com/AppLovin/AppLovin-MAX-Flutter), [Flutter interstitial guide](https://support.applovin.com/en/max/flutter/ad-formats/interstitial-ads), [Flutter rewarded guide](https://support.applovin.com/en/max/flutter/ad-formats/rewarded-ads).
- **Fact:** TradPlus has Android/iOS Flutter integrations. Its **TPX exchange separately claims Web and CTV traffic support**. That is insufficient evidence that its mobile mediation SDK also supplies general browser mediation, a browser rewarded-unlock API, or identical demand across App and Web. [Flutter downloads](https://docs.tradplusad.com/docs/download_flutter/), [TPX overview](https://docs.tradplusad.com/docs/operation/basic_guide/10-2/6-2/1-2/).
- **Inference:** Separate native-app and browser stacks are a practical baseline. Neither vendor's reviewed public documentation establishes one drop-in API that unifies native mediation and a short-drama website with the requested timing guarantees.
- **Fact:** Google announced rewarded-Web server-side verification (SSV) from **2026-10-29**, in its **2026-11-02** release notes. Advice that rewarded Web categorically lacks SSV is now stale. Public Web documentation remains much thinner than mobile SSV documentation. [Ad Manager release notes](https://support.google.com/admanager/answer/179039?hl=en).

## Native app mediation

| Option | Verified capabilities | Operational implication |
| --- | --- | --- |
| AppLovin MAX | Android/iOS and Flutter; interstitial and rewarded; manual native rendering in Flutter. The native guide exposes individual assets, requires the privacy-information icon, and does not guarantee that each network supplies every asset. | A native card can follow the app's feed layout; video and assets still depend on the supplying network. [Native guide](https://support.applovin.com/en/max/flutter/ad-formats/native-ads) |
| TradPlus | Flutter interstitial/rewarded APIs and native template or self-rendered layouts. The download page lists plugin **1.2.9, dated 2026-10-10**, with native Android/iOS SDK compatibility. | Native mediation is established; verify each chosen network, OS and format combination. [Flutter interstitial](https://docs.tradplusad.com/docs/integration_flutter/flutter_integration_base/interstitial/), [Flutter rewarded](https://docs.tradplusad.com/docs/integration_flutter/flutter_integration_base/rewarded/), [Flutter native](https://docs.tradplusad.com/docs/integration_flutter/flutter_integration_base/native/), [Downloads](https://docs.tradplusad.com/docs/download_flutter/) |

**Fact:** Mediation reduces application-facing integrations, but the underlying SDKs/adapters and commercial network setup remain. MAX's Flutter preparation guide generates Android Gradle and iOS CocoaPods integrations for selected networks. Its list includes Google, Meta, AppLovin-related demand, Pangle, Mintegral, Liftoff, Unity, InMobi and others. Support differs by format and network; the presence of a network in a list does not establish every format. [MAX mediated-network preparation](https://support.applovin.com/en/max/flutter/preparing-mediated-networks), [MAX network configuration guides](https://support.applovin.com/en/max/mediated-network-guides/sdk-bidder-network-guides).

**Fact:** TradPlus's Flutter integration likewise requires selecting native network SDKs/adapters and configuring Android and iOS dependencies. Its format mapping explicitly lists Google AdMob/Ad Manager rewarded-interstitial demand under its rewarded family. This is not evidence that every network or Flutter combination supplies that format. [Flutter integration](https://docs.tradplusad.com/docs/integration_flutter/flutter_integration_base/sdk_config/), [TradPlus format mapping](https://docs.tradplusad.com/docs/operation/adnetwork_qa/tpadtypeadnetworkadtype/).

**Fact:** TradPlus Flutter rewarded requests support `userId` and `customData` for server reward verification, and distinguish reward, close and video-play-end callbacks. MAX Flutter also supports S2S reward callbacks. A close callback alone is not the reward event. [TradPlus Flutter rewarded](https://docs.tradplusad.com/docs/integration_flutter/flutter_integration_base/rewarded/), [MAX Flutter rewarded](https://support.applovin.com/en/max/flutter/ad-formats/rewarded-ads).

### Timing and close controls

**Fact:** These SDK guides establish load/readiness/show/lifecycle APIs, not a universal publisher command to make every network's video exactly 6, 10 or 30 seconds. TradPlus explicitly describes rewarded playback as a third-party Activity that generally cannot be customized. Its description of a typical 15–30-second ad is not a duration guarantee. Google Flutter rewarded ads cannot be programmatically removed after `show()` and require user input. [TradPlus Android rewarded](https://docs.tradplusad.com/docs/tradplussdk_android_doc_v6/tradplussdk_android_doc_v6/rewardvideo/), [Google Flutter rewarded](https://developers.google.com/ad-manager/mobile-ads-sdk/flutter/rewarded).

**Fact:** Google's current AdMob **high-engagement** setting allows interstitial skip time up to **12 seconds**, rewarded reward/skip time up to **60 seconds**, and up to **three exit steps**. Disabled standard units use up to **5 seconds**, **30 seconds**, and **two exit steps** respectively. It is enabled by default for standard and partner-bidding units, but its on/off switch **does not control partner-bidding units**. These are skip/reward thresholds, not guaranteed total time until content resumes. [AdMob high-engagement setting](https://support.google.com/admob/answer/15525707?hl=en).

**Fact:** MAX's Google-bidding guide instructs creation of partner-bidding ad units, whose advanced settings are excluded. **Inference:** Do not promise that disabling the AdMob setting bounds Google bidding inside MAX or TradPlus, or bounds any other network's supply. Confirm the precise unit/integration type and available exclusions with the mediation vendor. [MAX Google bidding setup](https://support.applovin.com/en/max/mediated-network-guides/sdk-bidder-network-guides).

**Fact:** AppLovin's advertiser documentation describes interstitial video being skippable after at least five seconds **into an interactive stage**, while rewarded video may run up to 60 seconds. This describes AppLovin demand, not every network mediated by MAX. [AppLovin ad experience](https://support.applovin.com/en/growth/promoting-your-websites/welcome-to-applovin/ad-format).

**Inference:** “Skip after five seconds,” “reward earned at 30 seconds,” and “back to the drama by 30 seconds” are different requirements. Use approved provider controls and callbacks; do not overlay a fake close button, obscure SDK controls, truncate creatives, or fabricate completion. A swipeable native card can be investigated for early episodes, subject to native-format requirements; it is not a way to turn an SDK fullscreen rewarded ad into an arbitrary swipeable video.

## Browser Web/H5 options

### Google Ad Manager and GPT

**Fact:** Ad Manager account creation requires a valid AdSense account. Ad Exchange demand access is separate: Google documents direct access (typically for large publishers) or a Google Certified Publishing Partner using MCM. Merely adding GPT or opening GAM does not automatically activate every network or buyer. [GAM signup](https://support.google.com/admanager/answer/7084151?hl=en), [Ad Exchange access paths](https://support.google.com/admanager/answer/188529?hl=en).

**Fact:** GPT web interstitials are managed full-page ads for desktop/tablet/mobile. GPT must run in the **top window**; unsupported environments may return `null`. Triggers include eligible anchor navigation and optional inactivity, return-to-tab and article-related interactions. The default cap is one impression per ten minutes; the minimum configured interval is one minute. This is not a general “show fullscreen now after any episode/swipe” API. [GPT web-interstitial sample](https://developers.google.com/publisher-tag/samples/display-web-interstitial-ad).

**Fact:** GAM may withhold an interstitial even after an eligible trigger while optimizing future opportunities. Its help page says that, from 2024-11-04, interstitials can serve without local-storage consent by default, and `requireStorageAccess: true` opts out of that behavior. However, the same page's introduction and the GPT sample still say storage/Purpose-1 consent is required. **Unresolved documentation inconsistency:** confirm deployed GPT behavior and consent handling; do not infer a privacy exemption. [Current interstitial help](https://support.google.com/admanager/answer/9840201?hl=en).

**Fact:** GAM rewarded Web covers desktop, mobile and tablet on mobile-optimized pages. Both video and display demand fill by default; video-only demand requires applying through the account manager. The publisher supplies the opt-in screen and reward. Display needs at least seven seconds in view; completion can mean video end, display threshold, or TrueView skip threshold. Some demand grants before ad end; the ad remains until user close. Only one rewarded request should be active. SSV now sends GET callbacks when an SSV URL is configured on the relevant ad units. [Rewarded-Web help](https://support.google.com/admanager/answer/9116812?hl=en).

**Fact:** Use `rewardedSlotGranted` for grant eligibility; `rewardedSlotVideoCompleted` means video completion, and `rewardedSlotClosed` means user close. They are distinct. The grant payload contains reward amount/type, not a documented signed per-episode entitlement. `makeRewardedVisible()` follows affirmative opt-in. Unsupported pages/devices may return `null`; neutral zoom/mobile viewport matters. [GPT rewarded sample](https://developers.google.com/publisher-tag/samples/display-rewarded-ad), [GPT reference](https://developers.google.com/publisher-tag/reference).

**Unverified:** The reviewed public Web SSV section does not specify Web signature validation, transaction IDs, retry behavior, or per-request user/custom-data binding. Native Mobile Ads SSV docs do document such mechanisms, but cannot establish that GPT Web exposes identical fields. Before secure episode unlocking, obtain the current Web contract, verify authentication and bind callbacks to a single-use unlock attempt. Do not treat a browser callback, arbitrary timer, or unsigned client POST as proof of a payable view. This is an implementation inference, not a claim that Web SSV lacks security.

**Inference:** GPT Web interstitial is unsuitable inside a generic cross-origin wrapper iframe because of its top-window restriction. No general iframe embedding guarantee was established for rewarded Web either; use top-level integration or obtain explicit vendor support for the exact host/iframe arrangement. In-app WebView, browser H5, and an H5 game are different integrations.

**Fact:** Browser extensions/ad blockers can prevent requests and creatives from loading; a successful HTTP response can still contain no ad. Provide explicit unavailable/error states rather than waiting forever. Reward availability, approval and fill must be tested by market and device. [Google web-ad troubleshooting](https://support.google.com/admanager/answer/10358597?hl=en).

### Managed Web partner: Playwire RAMP

**Fact:** Playwire advertises Web rewarded video with opt-in rewards/content unlock, configurable portion watched and APIs, as well as web interstitial and pre-content formats. It offers managed and self-service arrangements and dynamically inserted scripts. This makes it a concrete vendor to evaluate when the publisher wants a partner to operate demand. It does **not** establish guaranteed yield, exact timing, Flutter parity or server-verifiable episode unlocks. [Playwire formats](https://www.playwire.com/ad-formats), [Web rewarded product sheet](https://www.playwire.com/hubfs/Sales%20Resources/Playwire%20Rewarded%20Video%20Ad%20Unit.pdf).

**Fact:** Public admission guidance conflicts: qualification suggests applying at 100,000+ pageviews and describes stronger average revenue with 20%+ US traffic; its FAQ requires 500,000 monthly pageviews and an English-country footprint. Confirm current program, traffic threshold, rights/content acceptance, revenue share, payment terms, reporting and integration obligations before treating it as available to Fayreel. [Qualification](https://www.playwire.com/qualification-criteria), [FAQ](https://www.playwire.com/faq).

### GAM + IMA + Prebid for a publisher-operated stack

**Fact:** IMA HTML5 handles browser video ads; Prebid supplies bidder adapters/auctions and can pass video bids into GAM and a player. Prebid's documentation requires video bidders, modules and ad-server line-item setup; it recommends its Video Module. **Inference:** This is a credible Web demand architecture, but carries more engineering/ad-operations work than a managed vendor and is not a one-SDK MAX equivalent. It does not automatically supply all buyers, contracts or rewarded semantics. [IMA compatibility](https://developers.google.com/interactive-media-ads/docs/sdks/html5/client-side/compatibility), [Prebid video setup](https://docs.prebid.org/prebid-video/video-getting-started.html), [Prebid video auction flow](https://docs.prebid.org/prebid-video/video-overview.html).

**Fact:** IMA's `skip()` works only when an ad is skippable and IMA is not rendering its own skip button. Its SDK does not support changing UI element layout/size/content. Do not assume a publisher timer can replace demand-controlled skip/close behavior. [IMA AdsManager](https://developers.google.com/interactive-media-ads/docs/sdks/html5/client-side/reference/interface/google.ima.AdsManager), [IMA FAQ](https://developers.google.com/interactive-media-ads/docs/sdks/html5/client-side/faq).

### TradPlus Web claims: keep scope precise

**Fact:** TPX says it accepts Web inventory and supports major formats, but public mobile SDK documentation does not establish a browser SDK equivalent. TradPlus's H5 interactive-ad case studies concern particular floating/icon interactions; its reporting list's `zMaticoo (H5)` identifier proves a reporting category, not general Web video mediation. Ask for an actual browser integration guide, supported formats/networks, domain approval, consent, reward callbacks/SSV and timing controls. [TPX overview](https://docs.tradplusad.com/docs/operation/basic_guide/10-2/6-2/1-2/), [H5 case examples](https://www.tradplusad.com/en/news/44), [Reporting API](https://docs.tradplusad.com/en/docs/api_cn/api_report_v2_0/).

## Policy constraints relevant to episode ads

**Fact:** Google's rewards policy permits nontransferable rewards usable within the publisher's platform, subject to its requirements. It requires clear action/reward disclosure and affirmative opt-in, except the distinct rewarded-interstitial format, which needs an advance opt-out screen. Skipping must not interfere with normal use, and the promised reward must be delivered. **Inference:** Episode access can be evaluated as the reward; a user who declines should still be able to use already available content/navigation. A climax is not a policy exception allowing involuntary rewarded ads. [Google rewarded policy](https://support.google.com/admanager/answer/7496282?hl=en).

**Fact:** For personalized Google ads in the EEA, UK and Switzerland, Google requires a certified CMP integrated with TCF. Its EU user-consent policy separately covers legally required storage consent and ad-personalization data. Consent to watch a rewarded ad is not interchangeable with consent for personal-data processing. [Google CMP requirement](https://support.google.com/admanager/answer/13554116?hl=en), [EU user-consent policy](https://www.google.com/about/company/user-consent-policy/).

**Fact:** Coalition for Better Ads distinguishes environments. Mobile-Web prestitials fall below its standard; desktop prestitials dismissible immediately do not. Mobile-Web postitials requiring a countdown fall below the standard; immediately dismissible examples do not. These are not universal “five seconds allowed everywhere” rules. [Mobile prestitial](https://www.betterads.org/mobile-prestitial-ad/), [Desktop prestitial](https://www.betterads.org/desktop-prestitial-ad-with-countdown/), [Mobile postitial](https://www.betterads.org/mobile-postitial-ad-with-countdown/).

**Fact:** The CBA November 2021 content-environment guidance applies its short-form standard to video of eight minutes or less and, in multi-video sessions, the first eight minutes. It specifically addresses between-video ads over 31 seconds that cannot be skipped within five seconds. Ads extending beyond the player can also be assessed under Web rules; overlapping environments use the stricter standard. Feeds and OTT/CTV are excluded from that document's short-form standard. [CBA content environments, November 2021 v2.1](https://www.betterads.org/hubfs/Better-Ads-Standards-Content-Environments-11-10-2021.pdf).

**Fact:** CBA lists in-video mid-rolls among unacceptable short-form experiences. Its native-app pages distinguish unexpected interruptions from ads at content boundaries, with specific tested exceptions. **Inference:** “Middle of the story, between completed episodes” differs from interrupting an episode during playback; do not generalize a tested boundary exception into approval for any forced 25–30-second ad. [CBA current standards](https://www.betterads.org/standards/), [App interstitial boundaries](https://www.betterads.org/mobile-app-interruptive-interstitials), [App non-skippable examples](https://www.betterads.org/mobile-app-non-skippable-video-interruptive-interstitials).

## Market evidence and remaining validation

**Fact:** Mintegral/Insightrackr's **2026 Global Non-Gaming App Trends Report**, using January–December **2025** data excluding mainland China, reports North America strongest for short-drama rewarded monetization, with Latin America/SEA lower. Values are indices within categories on Mintegral, not universal dollar eCPMs or Fayreel forecasts. Its methodology combines Mintegral's own aggregate platform data with Insightrackr. Use this to form experiments, not select a market solely from ad price. [Report, methodology p.4 and geography p.26](https://assets-official.mintegral.com/v3/file-link/2026/02/05/Mintegral%20x%20Insightrackr%20-%202026%20Global%20Non-Gaming%20App%20Trends%20Report.pdf).

**Inference:** Evaluate AppLovin MAX and TradPlus for native app operations/demand, and Playwire or GAM-based options for Web. Compare actual net revenue per viewer/session and retention by country, OS, format and episode position. A higher impression eCPM can still lose against poor fill, slower loading, longer exit paths, lower retention or acquisition costs. Do not promise “highest eCPM,” universal 6–10-second interstitials, exact 30-second rewarded ads, or guaranteed fill until those claims have been validated against the chosen supply and integration.

## Proposed Fayreel pilot (recommendations, not provider guarantees)

The user confirmed Android and iOS, permits separate App and PC/H5 stacks, and has not chosen countries. The following is an initial experiment design, not an instruction to launch campaigns or modify production.

### Stack and vendor selection

Use one native mediation platform in the App. MAX is a reasonable first technical pilot because its official Flutter integration covers the needed native, interstitial and rewarded formats; TradPlus remains an equally relevant commercial candidate. This does not establish MAX as the higher-paying option. Before choosing, compare each vendor's actual supported country/network/OS combinations, format support, short-duration inventory controls, server reward verification, net fees and payment terms. Do not add both full mediation stacks merely to discover which one pays more.

For PC/mobile Web, evaluate a managed video/rewarded partner such as Playwire RAMP, conditional on acceptance, pricing and the exact integration contract. A GAM-based implementation is another route; AdX access and additional demand relationships need separate qualification. Defer a self-operated Prebid stack until the traffic and operations justify it. TPX Web inventory is a business inquiry, not a verified drop-in TradPlus Flutter-to-Web migration.

Mediation consolidates the application-facing SDK and lifecycle logic, but selected native SDK adapters, demand-source approvals/accounts and credentials may still be required. Ask the vendor which commercial relationships it manages rather than assuming that one plugin activates all buyers.

### Episode policy

| Viewing stage | Starting experiment | Boundary |
| --- | --- | --- |
| First 1–3 episodes | No forced fullscreen ad | A retention baseline, adjustable after measurement |
| Early engagement | Clearly labelled native feed card between completed episodes; allow swipe/continue | A native card, not a fullscreen rewarded creative with its close controls replaced |
| Established viewing | An optional candidate short interstitial slot, target 6–8 seconds and a 10-second return-to-content ceiling | Enable only sources/experiences validated against that ceiling; otherwise keep the swipeable card |
| Cliffhanger at an episode boundary | Offer a voluntary rewarded unlock | Start by testing one valid reward for two episodes, avoiding an immediate second interruption |
| Locked content | Explicit reward action and benefit, target one roughly 30-second experience | A hard total 30-second maximum requires vendor-confirmed inventory, end-card and exit behavior; do not promise it from a normal mediation load/show API |

Place interruptions between complete episodes, not in the middle of a spoken line or playing episode. “Climax” is a story-level placement tag, not automatic permission for involuntary rewarded ads. Prevent back-to-back ads and a routine interstitial immediately after a rewarded unlock. Providers offering ad pods must be configured for a single ad when that is the promised experience.

Keep distinct light-ad and rewarded placements, with country/OS/source controls. Ordinary placements with no fill should continue the viewing flow. For a locked reward with no fill, offer a clear retry/alternative or an explicitly server-authorized limited free pass; never leave a black screen or mint an unlock from a client timer. Measure the whole show-to-content-resume path, not only video length or the first skip threshold.

### Market experiment

The user subsequently emphasized competition from TikTok, YouTube and dedicated short-drama services. **Revised recommendation:** country selection must first pass a competition/content/distribution review. The United States and the Philippines are unranked comparison candidates under an English-content assumption, not an established recommended launch pair. The US can test the North American high-value hypothesis; the Philippines can test a different cohort. Neither Philippine acquisition cost nor a lower competitive intensity has been established. If the catalog is Spanish or Portuguese, Mexico or Brazil may enter the same screening process. Language and genre fit, available content differentiation and a viable acquisition path precede the final country choice. See the [competition follow-up](short-drama-competition-2026-11-08.md).

Separate Android, iOS and Web results. Compare settlement-adjusted ad revenue per acquired viewer and per active session, qualified fill, loading failures, actual exit time, next-episode continuation, day-1/day-7 retention, acquisition cost and delivery/content costs. Start with a roughly two-week observation window and extend it when impression/cohort volume is insufficient. A calendar deadline alone does not make an experiment conclusive.

Select scale-up countries by net contribution and retention. The simple business calculation is ad settlement revenue less user acquisition, content/localization and playback infrastructure costs. Country eCPM rankings alone do not answer that question. Similarly, test price-floor changes against total revenue and fill rather than celebrating a higher reported eCPM with fewer paid impressions.

### Competition-aware launch gate

These are strategy hypotheses and proposed measurements, not measured advantages for Fayreel:

- Compare attention substitutes (general video feeds and full-length video), direct serialized-drama services, and free/ad-supported drama services. A competitor can also be a distribution channel, but its own content and link rules still apply.
- Evaluate a **country + language + genre/audience + acquisition route** combination. A country alone is too broad to establish an opportunity. Free access or a swipe interface is not sufficient differentiation from other free/ad-supported options.
- Establish a concrete reason to move: differentiated licensed content, meaningful localization, reliable complete-series access, transparent ad-for-episode terms, or a better continuation experience. Test that reason against the actual alternatives available to the cohort.
- Compare the same title or a genuinely comparable genre/cohort for opening free access, minutes of content per ad, time until the next episode, total ad exit burden, content completeness and continuation. A 30-second ad after a one-minute episode and the same ad after several episodes are different offers.
- Cap the acquisition test using **expected net advertising lifetime value per activated viewer**, not impression eCPM. Subscription/IAP-funded competitors may rationally bid above the acquisition cost an advertising-only product can recover; this is an economic implication, not an observation of any named competitor's current bids.
- Measure the complete funnel: acquisition impression to qualified visit, first-episode start, first-ad exposure, post-ad continuation, repeat viewing and settled ad revenue. Include attribution losses, campaign spend and the cost of organic content/channel operations; organic impressions are not proof of free acquisition.
- Test a Web viewing entry point and an App entry point separately. A Web-first route may reduce installation friction, but conversion, retention and net contribution must be measured rather than assumed. Optional App migration should have its own benefit and observed conversion.
- Test an authorized teaser's actual outbound path before extrapolating a large social funnel. Ordinary URLs in YouTube Shorts descriptions/comments are non-clickable; profile links, related YouTube videos and eligible brand-deal links have different conditions. [YouTube link documentation](https://support.google.com/youtube/answer/13748639?hl=en).

The next country decision should therefore use competitor/content observations plus a small acquisition-and-viewing cohort. Neither high CPM nor fast category download growth establishes a weakly contested, profitable market.

### Existing integration implications

Repository inspection found an existing Google Mobile Ads integration in the Flutter App and a signed provider-adapter/session boundary for Web rewards in the shared backend. These are starting points, not evidence of enrolled live demand or provider acceptance. The App's close-versus-earned-reward problem is already tracked in [App Issue #18](https://github.com/ceenreels/product-reels-fayreel-app/issues/18); it must be resolved before ad-based unlocking is enabled. The existing Web iframe adapter must be reassessed for the selected provider; GPT's top-window requirement cannot be satisfied merely by putting its interstitial in that iframe.

Share business policy, reporting dimensions and server-owned episode entitlements across clients. Keep native SDK rendering and browser ad rendering separate. For rewards, validate provider evidence, bind it to one user/session/benefit and make fulfillment idempotent; close, skip or browser completion messages alone must not grant episode access.

### Questions to resolve with shortlisted vendors

1. Do you accept short-drama App and browser inventory in the initial countries, and which formats and buyers are actually enabled on each OS/browser?
2. Can you enforce the *entire* maximum interruption, including playable/end-card/ad-pod/exit steps, for the selected placements? Which sources must be excluded, and what remains unbounded?
3. What server-authenticated reward contract binds one viewing attempt to an account and episode entitlement, with duplicate and delayed callbacks handled?
4. What are the eligibility thresholds, net revenue share/fees, payout thresholds/schedule, currency and network-account obligations?
5. Can a pilot export country/OS/placement/source revenue, paid impressions, fill/errors and reward outcomes so the final decision is based on Fayreel's own traffic?
