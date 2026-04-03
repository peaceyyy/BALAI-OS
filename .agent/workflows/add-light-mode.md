---
description: Implement scalable, accessible light/dark mode toggles adapted to the existing CSS variable architecture.
---

# /add-light-mode

> **Purpose**: A formal workflow for adding or migrating to dual-theme (Light/Dark) support. It honors the user's "Dark First" cosmic aesthetic while building scalable and accessible state management.
> **Personas Invoked**: **Sparks** (for the UI/UX token mapping) and **Kairou** (for state management architecture).

## Overview

Implementing light/dark mode at scale requires minimizing DOM re-renders and maintaining codebase consistency. The gold standard is utilizing **CSS Custom Properties (Variables)** controlled by a `data-theme` attribute on the `<html>` or `<body>` tag, managed via a global context provider.

---

## 1. Context & Setup (Kairou)

**Goal**: Prepare the environment and audit existing variables without enforcing destructive rewrites.

1.  **Locate Global Styles**: Find the root CSS file (e.g., `index.css`, `globals.css`).
2.  **Audit Existing CSS Variables**:
    -   *Constraint*: **Do not aggressively refactor** established CSS variable scopes if they are too broad and fundamental to the app. Work within the established naming conventions.
    -   *Action*: Identify root colors. If they are hardcoded hexadecimal/RGB values in component files, map them into the root CSS file as variables.
3.  **Establish Dark-First Baseline**:
    -   Acknowledge the owner's design philosophy (`sparks_design_system.md`): Deep charcoals, neutral grays, cosmic blues, muted purples.
    -   Ensure `[data-theme='dark']` (or the default `:root` if Dark is standard) maps to these tones.

## 2. Semantic Mapping & Light Mode Overrides (Sparks)

**Goal**: Add the inverse theme (Light Mode) adhering to aesthetic principles.

1.  **Create Inverse Theme**: Add `[data-theme='light']` class/attribute block below the root variables.
2.  **Map Light Mode Equivalents**:
    -   *Backgrounds*: Avoid harsh pure white (`#FFFFFF`). Use soft off-whites (e.g., `#FAFAFA`, `#F4F4F5`).
    -   *Accents*: Tone down highly saturated cosmic blues/purples so they do not vibrate on light backgrounds.
    -   *Elevation*: Since shadows work better in Light Mode than Dark Mode, ensure `--shadow` variables enhance elevation without looking harsh.
3.  **Accessibility Check (Sparks)**: Ensure WCAG contrast ratios (minimum 4.5:1 for body text) are maintained in the new light palette.

## 3. State Management Implementation (Kairou)

**Goal**: Store and retrieve user preference securely and continuously.

1.  **Create Theme Provider** (e.g., React Context, Vue Provide/Inject, or vanilla JS closure):
    -   Manage the `theme` state (`light`, `dark`, `system`).
    -   Persist the selected theme string into `localStorage`.
2.  **FOIT Prevention (Flash of Incorrect Theme)**:
    -   Inject a minimal blocking script in the `<head>` of `index.html` (or `_document.js` / root layout) that reads `localStorage` and `window.matchMedia('(prefers-color-scheme: dark)')` to set the `data-theme` attribute *before* the body renders.
3.  **Hydration Match**: Ensure the initial state of the React/Vue component tree matches the server/blocking script to prevent hydration mismatches.

## 4. UI Toggle Component (Sparks)

**Goal**: Give the user control through a familiar, calm interface.

1.  **Component Creation**: Build a `ThemeToggle.jsx/tsx` component.
2.  **Design Patterns**:
    -   Use familiar iconography (Sun / Moon).
    -   *Sparks Principle*: Motion must be calm. Use a subtle crossfade or rotational transition using `framer-motion` or standard CSS. No bouncy or loud animations.
3.  **Accessibility**:
    -   Use an `<button>` wrapping the icon.
    -   Include `aria-label="Toggle theme"` and `aria-pressed={isDark}`.
    -   Ensure visible focus states in both light and dark modes.

## 5. Verification & Clean-Up (Janitor)

**Goal**: Test edge cases and clean up leftover hardcoded colors.

1.  Search the `src` directory for hardcoded color values (`#`, `rgb`, `hsl`) that slipped past the CSS variable mapping. Replace them with `var(--semantic-name)`.
2.  Test the toggle:
    -   Does it remember the state on page reload?
    -   Do newly rendered components respect the `data-theme` attribute without requiring an app reboot?
