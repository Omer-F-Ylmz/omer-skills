# SOSYAL-OTO-1 — Platform rules & patterns research (seen 2026-10-30)
Scope: 2 faceless EN channels (A "Free AI Drop", B "Curiosity Well"), same 1080x1920 30-60 s video to YT Shorts / IG Reels / TikTok.
Legend: [O] = official source, [3P] = third-party, "doğrulanamadı" = could not verify. ~25 web calls used, 0 paid APIs.

## 1. YouTube (YPP)
- [O] Inauthentic content — https://support.google.com/youtube/answer/1311392 (YPP monetization policies). Dated update **2025-07-15**:
  "renaming this policy from 'repetitious content' to 'inauthentic content'", to clarify it "includes content that is repetitive or mass-produced"; "always been ineligible". "There is no change to our reused content policy."
  Not allowed: "Similar or repetitive content with low educational value, commentary, narratives, or minimal variation across videos";
  "AI-generated content made with generic or unoriginal templates giving the impression of mass production";
  "videos that stitch together unrelated or inconsistent AI clips"; "AI-generated personas to deliver information on sensitive topics".
  Allowed: "using AI to edit your video scripts or generate a unique background visual"; with automation "the final product must still demonstrate your creative vision".
  Reused content: "Content that exclusively features readings of other materials you did not originally create" is NOT allowed (=> Group B must not just read Wikipedia text; write original narrative).
- TTS/faceless: official page never mentions TTS -> explicit TTS rule **doğrulanamadı**. [3P] consensus (ytgrowth.io, nofacetube.com, newmoneymatrix.org): AI voice / faceless alone is not demonetized; evaluated per channel; Jan 2026 "AI slop" enforcement wave (16 channels, 35M subs terminated — [3P] only). [3P] newmoneymatrix claims a further rename to "Generic or Repetitive Content" in July 2026 — **doğrulanamadı**.
- [O] Thresholds today — https://www.youtube.com/creators/earn/youtube-partner-program/ & https://support.google.com/youtube/answer/72851:
  Tier 1 (fan funding/Shopping): 500 subs + 3 qualified uploads (90 d) + 3,000 long-form watch h (365 d) OR 3M Shorts views (90 d).
  Tier 2 (Ads & Premium revenue): 1,000 subs + 4,000 h (365 d) OR 10M qualified Shorts views (90 d). Shorts-feed watch hours do not count toward 4,000 h. US is eligible ([3P] vidiq).
- [O] **Change from 2027-02-01** — https://support.google.com/youtube/answer/12843009 + https://blog.youtube/news-and-events/youtube-partner-program-updates-2027-new-opportunities-earn/ (blog ~2026-08-10):
  new applicants: 1k subs + "8,000 qualified watch hours in the last 365 days, or 20M qualified Shorts views in the last 90 days"; existing partners keep status;
  Shorts Creator Pool payout requires to "maintain 10M qualified Shorts views over the last 90 days" (applies to all, incl. existing); 500-sub tier unchanged; accept new terms by 2027-01-31.
  Activity rule (blog, via search snippet): active = 1,000 h/365 d OR 1M Shorts views/90 d OR 2 long-form or 5 Shorts per 90 d.
  => Implication: applying before 2027-01-31 23:59 UTC uses the old 10M bar ([3P] relevantaudience); daily Shorts alone unlikely to earn ad revenue below 10M/90 d.
- [O] Altered/synthetic disclosure — https://support.google.com/youtube/answer/14328491: required when content "seems realistic" and
  "Makes a real person appear to say or do something they didn't do", "Alters footage of a real event or place", "Generates a realistic scene that didn't actually occur", or AI music is the main focus.
  Not required: scripts/titles/thumbnails/infographics made with genAI, "Caption creation", unrealistic/animated content, color/lighting, upscaling. Only voice item listed: cloning one's own voice = exempt. Generic TTS not named (**doğrulanamadı**; likely exempt as it does not depict a real person). Disclosure "won't limit reach or monetization"; repeated non-disclosure -> removal / YPP suspension.
  => Group B: real archival photos = no label; AI-generated "realistic historical scene" images WOULD need the label. Group A: screen recordings = no label.

## 2. TikTok
- Creator Rewards Program: official page did not render (JS) -> exact official text **doğrulanamadı**. [3P] consensus (toptal, postlinkapp, gemlist, 2026): 18+, personal account, 10,000 followers, 100,000 views in last 30 d, US eligible, videos must be original and **>1 minute**; [3P] some say >=1,000 FYF views per video. TikTok Discover snippet quoting TikTok: "Videos should be longer than 1 minute." => 30-60 s videos earn **nothing** from CRP; need 61+ s TikTok cut to qualify.
- [3P quoting Creator Academy, Oct 2026] CRP low-quality factors: "split screens, meaningless reactions, low-quality images, or slide videos"; 5 violations / 30 d -> ineligible. **Slideshow-style archival montage (Group B) is a risk** — add motion/narrative edits.
- [O] AIGC labeling — Community Guidelines Integrity & Authenticity (https://www.tiktok.com/community-guidelines/en-GB/integrity-authenticity?cgversion=2025H2update, via search):
  must label AI-generated or significantly edited content showing realistic-looking scenes or people (AIGC label, caption, sticker or watermark); unlabelled may be removed/restricted/labelled; auto-labels via C2PA Content Credentials. AIGC defined as image, video or audio made/changed by AI. TTS-specific rule **doğrulanamadı**.
- [O-ish] Unoriginal: FYF-ineligible = "Reused or unoriginal content posted without creative edits ... Low-quality or minimally edited content" (quoted via [3P] shapelessai/contentiq; Safety Center page). FYF Eligibility Standards version: released 2026-08-25, effective 2026-09-24 (https://www.tiktok.com/community-guidelines/en/fyf-standards).
- [O] Content Posting API — https://developers.tiktok.com/doc/content-posting-api-get-started: "All content posted by unaudited clients will be restricted to private viewing mode"; audit needed; scope `video.publish`; MP4+H.264.
  [O] https://developers.tiktok.com/docs/en/content-sharing-guidelines (via search): unaudited = max 5 users / 24 h, SELF_ONLY, accounts must be private. Per-creator daily cap ~15 posts — [3P] breakreach only, **doğrulanamadı**. Audit ~4-14 days ([3P]).

## 3. Instagram / Meta
- Reels monetization US: [3P] only — Gifts (Stars, $0.01 each), invite-only Bonuses, brand deals main income; "Ads on Reels" US availability **doğrulanamadı**. No open, guaranteed per-view payout for Reels in US found.
- Originality: [3P] TechCrunch/PetaPixel/MediaPost 2026-04-30: accounts that primarily post unoriginal content (photos/carousels, in addition to reels) "will no longer be shown in places where we recommend content"; judged over a month; recovery = "most" posts original over 30 d. Earlier (Apr 2024, [3P] Nasdaq/RTT): 10+ unoriginal reposts in 30 d -> Reels not recommended. Official IG post itself **doğrulanamadı** (not fetched).
- [O] AI label — https://about.fb.com/news/2024/04/metas-approach-to-labeling-ai-generated-content-and-manipulated-media/ (upd. 2025-10-23): "Made with AI" -> "AI info" (2024-07-01); edited-only content label moved to menu (2024-09-12). [O] https://about.fb.com/news/2026/02/meta-prepares-for-2026-us-midterms/ (via search): disclosure required for organic "photorealistic video or realistic-sounding audio that was digitally created or altered", "may apply penalties". [3P] Meta example list includes "a Reel narrated with a realistic AI voiceover" => **Kokoro/edge TTS voiceover on IG likely needs the "AI info" self-disclosure** (official help page did not render on desktop; exact wording **doğrulanamadı**).
- [O] Publishing API — https://developers.facebook.com/docs/instagram-platform/content-publishing: professional account only; Facebook Login (Page-linked; PPA may block) or Instagram Login (`instagram_business_basic`, `instagram_business_content_publish`); media must be on public URL (except resumable upload to rupload.facebook.com); limit: page says "100 API-published posts within a 24-hour moving period" but carousel section says 50 — conflicting, check `GET /<IG_ID>/content_publishing_limit`.
- [O] Reels specs — https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/media: MOV/MP4, moov atom front, no edit lists; H264/HEVC progressive, closed GOP, 4:2:0; AAC <=48 kHz; 23-60 fps; 9:16 recommended; max 1920 px wide; 3 s-15 min; <=300 MB; video <=25 Mbps VBR, audio 128 kbps. => ffmpeg: `-c:v libx264 -pix_fmt yuv420p -r 30 -c:a aac -ar 48000 -b:a 128k -movflags +faststart`.

## 4. Faceless shorts patterns (data quality: weak, vendor blogs only)
- Hook: [3P] grow-it.se (claims 50k videos): push threshold ~60%+ 3-s hold, 45%+ at midpoint, 25-35% completion for 30-s video; Shorts ~70%+ APV. 360uniquizer gives much lower averages (28-35% 3-s) — sources conflict. aibrify: 30-50% leave in 0-3 s; cutting intro cards +10-20 pp AVD. => No logo/intro; first frame = payoff/claim.
- Length: [3P] Kapwing 21-34 s best engagement; Zebracat (via virvid) 20-25 s highest completion. Conflicts with TikTok CRP >60 s need => plan 2 cuts (YT/IG ~25-40 s, TikTok 61-70 s).
- Captions: [3P] Kapwing: captions +12% watch time (method unknown). Word-by-word highlight / big centered style, loop endings, US posting times: no data-backed source found in budget -> **doğrulanamadı**.
- Series format: no data-backed source found -> **doğrulanamadı**.

## 5. Free US trend sources
- [O/3P verified 2026-10] Google Trends RSS: `https://trends.google.com/trending/rss?geo=US` — 10 newest trends, `ht:approx_traffic`, ~3 news links; old pytrends dailytrends/realtime endpoints 404, pytrends archived (dev.to 2026-10). trendspy lib returns more.
- [O] Wikipedia On this day: `https://en.wikipedia.org/api/rest_v1/feed/onthisday/{all|selected|events|births|deaths|holidays}/{MM}/{DD}` (zero-padded, no auth, set User-Agent). api.wikimedia.org `/feed/v1/...` is in gradual deprecation, global rate limits since 2026-03 (wikitech API_Portal/Deprecation).
- [O] Product Hunt API v2 GraphQL (https://api.producthunt.com/v2/docs): "must not be used for commercial purposes" by default; monetized channel use => email hello@producthunt.com. Risk for Group A.
- Hacker News (Firebase API), Reddit r/artificial (API terms/rate limits 2026), There's An AI For That, Futurepedia feeds: not checked within the ~25-call budget -> **doğrulanamadı**.

## Key implications
1. Inauthentic/mass-produced is THE risk for a fully automated pipeline: vary formats, original scripts with commentary/opinion, no pure reading of sources, no slideshow-only visuals.
2. TikTok CRP needs >60 s; YT Shorts ad money needs 10M views/90 d (and 2027 entry 20M). Early revenue realistically = none/fan funding; budget accordingly.
3. Labels: YT/TikTok only for realistic synthetic people/events; Meta likely wants "AI info" for realistic AI voiceover.
4. TikTok auto-posting is private-only until audit; IG needs professional account + public video URL.
