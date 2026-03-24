---
name: product-positioning-analysis
description: Use when you need to analyze reviews, customer feedback, or text using the Product Positioning Theory to extract and structure attributes, functions, benefits, and usage/service contexts.
---

# Product Positioning Analysis Skill

## Overview

This skill leverages the Product Positioning Theory to systematically decompose consumer feedback, reviews, and textual data. It structures the text into four key dimensions: Product Attributes, Product Functions, Consumer Benefits, and Usage Context & Service Experience.

## Input Contract

Provide the following:

- `text`: The raw text, reviews, or interview transcripts to be analyzed.
- `analysis_goal`: (Optional) The specific focus or goal of this analysis.

## Expected Output

The agent will output a structured Markdown report containing:

1. **Summary**: A brief overview of the positioning landscape based on the text.
2. **Dimension Breakdown**:
   - Product Attributes (產品屬性)
   - Product Functions (產品功能)
   - Consumer Benefits (消費者利益)
   - Usage Context & Service Experience (使用用途與服務場景)
3. **Key Insights**: Actionable takeaways to improve product positioning or marketing.

## Workflow

1. Read `references/01-theory-concept.md` to align on the core theory.
2. Read `references/02-dimension-guidelines.md` to understand the rules for each dimension.
3. Analyze the provided `text` according to these guidelines.
4. Synthesize and output the structured analysis.
