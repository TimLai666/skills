---
version: alpha
name: Project Name
description: One-line description of the project's visual identity
colors:
  primary: "#000000"
  secondary: "#000000"
  tertiary: "#000000"
  neutral: "#000000"
typography:
  h1:
    fontFamily: Font Name
    fontSize: 48px
    fontWeight: 600
    lineHeight: 1.1
    letterSpacing: -0.02em
  h2:
    fontFamily: Font Name
    fontSize: 32px
    fontWeight: 600
    lineHeight: 1.2
  body-lg:
    fontFamily: Font Name
    fontSize: 18px
    fontWeight: 400
    lineHeight: 1.6
  body-md:
    fontFamily: Font Name
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.6
  label-caps:
    fontFamily: Font Name
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1
    letterSpacing: 0.1em
rounded:
  sm: 4px
  md: 8px
  lg: 12px
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 32px
  xl: 64px
components:
  button-primary:
    backgroundColor: "{colors.tertiary}"
    textColor: "#ffffff"
    rounded: "{rounded.md}"
    padding: 12px
  button-secondary:
    backgroundColor: "transparent"
    textColor: "{colors.primary}"
    rounded: "{rounded.md}"
    padding: 12px
  card:
    backgroundColor: "#ffffff"
    rounded: "{rounded.lg}"
    padding: 24px
---

## Overview

<!-- What is this project? Who is the audience? What emotional response should the UI evoke? -->

## Colors

<!-- Why these colors? What role does each play? How are they used? -->

- **Primary (#000000):** <!-- e.g. Deep ink for headlines and core text -->
- **Secondary (#000000):** <!-- e.g. Sophisticated slate for borders and metadata -->
- **Tertiary (#000000):** <!-- e.g. The sole driver for interaction -->
- **Neutral (#000000):** <!-- e.g. Foundation background -->

## Typography

<!-- Why these fonts? What's the pairing logic? -->

- **Headlines:** <!-- Font, weight, why -->
- **Body:** <!-- Font, size, why -->
- **Labels:** <!-- Font, case, spacing, why -->

## Layout

<!-- Grid system, spacing rhythm, containment logic -->

## Elevation & Depth

<!-- Shadows, tonal layers, or flat alternative -->

## Shapes

<!-- Corner radius language, shape philosophy -->

## Components

<!-- Button, card, input, chip specs. Use token references like {colors.tertiary} -->

## Do's and Don'ts

- <!-- Do: ... -->
- <!-- Don't: ... -->
