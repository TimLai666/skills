# Design options and palette

Read when choosing detail, layout or colors.

## Configuration Options

These are design preferences, not universal Mermaid API parameters. Translate them into syntax supported by the chosen diagram type and renderer.

**Layout:**
- `direction`: "vertical" (TB), "horizontal" (LR), "right-to-left" (RL), "bottom-to-top" (BT)
- `aspect`: "portrait" (default), "landscape" (wide), "square"

**Detail Level:**
- `simple`: Core elements only, minimal labels
- `standard`: Balanced detail with key descriptions (default)
- `detailed`: Full annotations, explanations, and metadata
- `presentation`: Optimized for slides (larger text, fewer details)

**Style:**
- `minimal`: Monochrome, clean lines
- `professional`: Semantic colors, clear hierarchy (default)
- `colorful`: Vibrant colors, high contrast
- `academic`: Formal styling for papers/documentation

**Additional Options:**
- `show_legend`: true/false - Include color/symbol legend
- `numbered`: true/false - Add sequence numbers to steps
- `title`: string - Add diagram title

## Color Scheme Defaults

Standard professional palette:
- Green (#d3f9d8/#2f9e44): Input, perception, start states
- Red (#ffe3e3/#c92a2a): Planning, decision points
- Purple (#e5dbff/#5f3dc4): Processing, reasoning
- Orange (#ffe8cc/#d9480f): Actions, tool usage
- Cyan (#c5f6fa/#0c8599): Output, execution, results
- Yellow (#fff4e6/#e67700): Storage, memory, data
- Pink (#f3d9fa/#862e9c): Learning, optimization
- Blue (#e7f5ff/#1971c2): Metadata, definitions, titles
- Gray (#f8f9fa/#868e96): Neutral elements, traditional systems

