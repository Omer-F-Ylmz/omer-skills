---
name: scroll-image-sequence
description: Build a scroll-driven frame sequence (canvas frames tied to scroll position). Use for scroll-image-sequence, Apple-style frame-by-frame scroll heroes, or scrubbing pre-rendered stills on scroll.
---

# Scroll image sequence

Source: `scroll-image-sequence` npm package by Ivan Lutskyi (MIT, see `LICENSE` next to this file; repo github.com/ivan-lutskyi/scroll-image-sequence). Keep the license file with any copy of the package.

## When to use
- A pinned section where scroll position picks the frame (canvas draw), not a video element.
- Frames are exported stills (JPG/WEBP) numbered with zero padding, e.g. `FIG_0001.jpg`.

## Steps
1. Export frames at the display size (1x and 2x source sizes if needed). Keep the count low: 100-150 frames is typical; compress first (`baoyu-compress-image` or `squoosh`-style tools).
2. Install: `npm install scroll-image-sequence`.
3. Add a `<canvas id="hero">` inside a tall wrapper (the wrapper sets scroll length; the canvas stays sticky).
4. Call the API:
   ```js
   import { initScrollImageSequence } from 'scroll-image-sequence';

   initScrollImageSequence({
     canvas: document.querySelector('#hero'),
     frameCount: 100,
     imagePath: (i) => `/imgs/FIG_${String(i).padStart(4, '0')}.jpg`,
     scrollArea: window.innerHeight * 2, // optional px
     onLoaded: () => document.documentElement.classList.add('seq-ready'),
   });
   ```
5. Text or overlays that move with the sequence: drive them from the same progress with `onFrame(frameIndex)` or with GSAP ScrollTrigger (see `gsap-scrolltrigger`); do not add a second scroll listener that fights the library.
6. Verify desktop, mobile, and reduced motion. Under `prefers-reduced-motion`, show the first or last frame as a still.

## Gotchas
- Preload failures: a missing frame stalls progress; log the failing index while developing.
- Smooth scroll libraries (Lenis) change the scroll source; test that frames and the pin stay in sync (see `smooth-scroll`).
- Large frame sets hurt mobile memory; prefer fewer, smaller frames over more.
