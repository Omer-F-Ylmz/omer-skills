# context7 /websites/gsap_v3 — ScrollTrigger scrub pin matchMedia refresh cleanup

### Teardown function in ScrollTrigger.matchMedia()

Source: https://gsap.com/docs/v3/Plugins/ScrollTrigger/static.matchMedia%28%29

Shows how to return a teardown function from a matchMedia callback for custom cleanup. ScrollTrigger automatically kills all ScrollTriggers created inside the function when the breakpoint no longer matches, so the teardown is only needed for non-ScrollTrigger animations. The returned function is called when the breakpoint no longer matches.

```javascript
ScrollTrigger.matchMedia({
  // desktop
  "(min-width: 800px)": function () {
    // ScrollTrigger (this automatically gets killed when the breakpoint no longer matches...
    gsap.to(".panel", {
      xPercent: -100,
      scrollTrigger: {
        trigger: ".panel",
        scrub: 1,
        end: "+=500",
      },
    });

    // other animations that aren't ScrollTrigger-related...
    let tl = gsap.timeline();
    tl.to(".box", { rotation: 360 }).to(".box", { y: 100 });

    // THIS IS THE KEY! Return a function that'll get called when the breakpoint no longer matches so we can kill() the animation (or whatever)
    return function () {
      tl.kill();
      // other cleanup code can go here.
    };
  },
});
```

--------------------------------

### Teardown Function

Source: https://gsap.com/docs/v3/Plugins/ScrollTrigger/static.matchMedia%28%29

Documentation for the optional teardown function in ScrollTrigger.matchMedia() callbacks.

```APIDOC
## Teardown Function

### Description
Optionally return a function from a media query callback to perform custom cleanup when the breakpoint no longer matches. This is useful for killing animations that are not ScrollTrigger-related.

### Syntax
Inside a media query function, return a function that will be called when the breakpoint no longer matches.

### Example
```javascript
ScrollTrigger.matchMedia({
  // desktop
  "(min-width: 800px)": function () {
    // ScrollTrigger (this automatically gets killed when the breakpoint no longer matches...
    gsap.to(".panel", {
      xPercent: -100,
      scrollTrigger: {
        trigger: ".panel",
        scrub: 1,
        end: "+=500",
      },
    });

    // other animations that aren't ScrollTrigger-related...
    let tl = gsap.timeline();
    tl.to(".box", { rotation: 360 }).to(".box", { y: 100 });

    // THIS IS THE KEY! Return a function that'll get called when the breakpoint no longer matches so we can kill() the animation (or whatever)
    return function () {
      tl.kill();
      // other cleanup code can go here.
    };
  },
});
```

### Notes
- ScrollTrigger automatically kills all ScrollTriggers created inside the media query function when that media query no longer matches.
- Only need a teardown function for things that aren't directly related to ScrollTriggers.
- Any (or all) of the media queries can return a function.
```

--------------------------------

### Teardown function

Source: https://gsap.com/docs/v3/Plugins/ScrollTrigger/static.matchMedia%28%29

You can \[optionally] **return a function** which will be called when that breakpoint no longer matches so that you can do custom cleanup routines like killing other animations that aren't ScrollTrigger-related. For example:

```
ScrollTrigger.matchMedia({
  // desktop
  "(min-width: 800px)": function () {
    // ScrollTrigger (this automatically gets killed when the breakpoint no longer matches...
    gsap.to(".panel", {
      xPercent: -100,
      scrollTrigger: {
        trigger: ".panel",
        scrub: 1,
        end: "+=500",
      },
    });

    // other animations that aren't ScrollTrigger-related...
    let tl = gsap.timeline();
    tl.to(".box", { rotation: 360 }).to(".box", { y: 100 });

    // THIS IS THE KEY! Return a function that'll get called when the breakpoint no longer matches so we can kill() the animation (or whatever)
    return function () {
      tl.kill();
      // other cleanup code can go here.
    };
  },
});
```

Remember, ScrollTrigger automatically kills all ScrollTriggers created inside the media query function when that media query no longer matches, so you only need a teardown function for things that aren't directly related to ScrollTriggers. The animation that is associated with a particular ScrollTrigger will be killed along with the ScrollTrigger when the media query no longer matches. Any (or all) of the media queries can return a function.

--------------------------------

### Refresh a timeline's ScrollTrigger instance

Source: https://gsap.com/docs/v3/Plugins/ScrollTrigger/refresh%28%29

Create a timeline with a ScrollTrigger, then after adding all animations, manually call tl.scrollTrigger.refresh() to recalculate its start/end. Alternatively, use the static ScrollTrigger.refresh() to refresh all instances.

```javascript
// create a timeline with a ScrollTrigger
const tl = gsap.timeline({ scrollTrigger: {...}});

// after adding all animations to that timeline, we can manually force it to calculate its start/end (on just that instance):
tl.scrollTrigger.refresh();

// or cause ALL ScrollTrigger instances to refresh using the static method:
ScrollTrigger.refresh();
```

--------------------------------

### ScrollTrigger.matchMedia()

Source: https://gsap.com/docs/v3/Plugins/ScrollTrigger/static.matchMedia%28%29

Documentation for ScrollTrigger.matchMedia() method, including syntax, parameters, and example usage.

```APIDOC
## ScrollTrigger.matchMedia()

### Description
Creates media query-based breakpoints for ScrollTrigger animations. Each function is executed when the corresponding media query matches, and all ScrollTriggers created inside are automatically reverted when the breakpoint no longer matches.

### Method
matchMedia()

### Syntax
ScrollTrigger.matchMedia(vars)

### Parameters
- **vars** (Object) - Required - An object where keys are media query strings (e.g., "(min-width: 800px)") or "all", and values are functions to execute when the media query matches.

### Return Value
Returns a function that can be called to revert all ScrollTriggers created within the media query functions.

### Example
```javascript
ScrollTrigger.matchMedia({
  // desktop
  "(min-width: 800px)": function () {
    gsap.to(".panel", {
      xPercent: -100,
      scrollTrigger: {
        trigger: ".panel",
        scrub: 1,
        pin: true,
        end: "+=500",
      },
    });
  },

  // mobile
  "(max-width: 799px)": function () {
    gsap.to("#logo", {
      scale: 0.5,
      scrollTrigger: {
        trigger: ".nav-bar",
        start: "top top",
        toggleActions: "play none reverse none",
      },
    });
  },

  // all
  all: function () {
    gsap.set(".photo", { opacity: 0 });
    ScrollTrigger.batch(".photo", {
      onEnter: (elements) =>
        gsap.to(elements, { opacity: 1, stagger: 0.1, overwrite: true }),
    });
  },
});
```

### Notes
- Added in GSAP 3.4.0.
- The teardown return function capability was added in 3.5.0.
- ScrollTrigger automatically kills all ScrollTriggers created inside the media query function when that media query no longer matches.
- Use ScrollTrigger.saveStyles() to record initial inline CSS for elements so ScrollTrigger can revert them even if animations add inline styles later.
```