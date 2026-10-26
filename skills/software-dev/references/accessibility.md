# Web Accessibility (A11y) Guide

Accessibility is not a feature; it is a requirement. The web is for everyone.

## 1. The Core Principles (POUR)

*   **Perceivable:** Users must be able to perceive the information (e.g., see it, hear it).
*   **Operable:** Users must be able to operate the interface (e.g., keyboard only).
*   **Understandable:** Information and operation must be understandable.
*   **Robust:** Content must be robust enough to be interpreted reliably (standards-compliant).

## 2. Semantic HTML

The single most important thing you can do.

*   **Buttons vs Links:**
    *   `<button>`: Performs an action (Submit, Toggle, Modal).
    *   `<a>`: Navigates to a new URL.
    *   *Never* put `onClick` on a `<div>`. It is not focusable or actionable by screen readers.
*   **Headings:** `<h1>` through `<h6>`. Do not skip levels (e.g., `h1` -> `h3`). They form the "Table of Contents" for screen reader users.
*   **Landmarks:** Use `<main>`, `<nav>`, `<aside>`, `<header>`, `<footer>`. Allows users to jump to sections.

## 3. Keyboard Navigation

*   **Focusable:** All interactive elements must be focusable (Tab key).
*   **Visible Focus:** NEVER remove the outline (`outline: none`) without replacing it with a custom high-contrast style.
*   **Skip Links:** Provide a "Skip to Main Content" link at the top of the page.

## 4. ARIA (Accessible Rich Internet Applications)

**Rule #1 of ARIA:** Don't use ARIA if HTML can do it.

*   **Role:** Defines what an element is (`role="dialog"`).
*   **State:** Defines current status (`aria-expanded="true"`, `aria-checked="false"`).
*   **Labeling:**
    *   `aria-label`: String label (Invisible).
    *   `aria-labelledby`: Refers to another element's ID (Visible).
    *   `aria-describedby`: Refers to description/help text.

## 5. Visual Considerations

*   **Color Contrast:** Text must have 4.5:1 contrast ratio against background (WCAG AA).
*   **Color Meaning:** Don't use color alone to convey meaning (e.g., "Red means error"). Use icons or text labels too.
*   **Motion:** Respect `prefers-reduced-motion`. Disable auto-playing animations.

## 6. Testing Tools

*   **Automated:** `axe-core` (Lighthouse, axe-linter). Catches ~30% of issues.
*   **Manual:**
    *   **Keyboard:** Unplug your mouse. Can you use the site?
    *   **Screen Reader:** NVDA (Windows), VoiceOver (Mac).
