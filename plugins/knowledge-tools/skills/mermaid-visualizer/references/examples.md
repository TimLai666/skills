# Examples

Read when selecting a layout or constructing a similar diagram.

## Example Usage Patterns

**Pattern 1: Basic request**
```
User: "Visualize the software development lifecycle"
Response: [Analyze → Choose graph TB → Generate with standard detail]
```

**Pattern 2: With configuration**
```
User: "Create a horizontal flowchart of our sales process with lots of detail"
Response: [Analyze → Choose graph LR → Generate with detailed level]
```

**Pattern 3: Comparison**
```
User: "Compare traditional AI vs AI agents"
Response: [Analyze → Choose comparison layout → Generate with contrasting styles]
```

## Common Patterns

### Swimlane Pattern (Grouping)
```mermaid
graph TB
    subgraph core["Core Process"]
        A --> B --> C
    end
    subgraph support["Supporting Systems"]
        D
        E
    end
    core -.-> support
```

### Feedback Loop Pattern
```mermaid
graph TB
    A[Start] --> B[Process]
    B --> C[End]
    C -.->|Feedback| A
```

### Hub and Spoke Pattern
```mermaid
graph TB
    Central[Hub]
    A[Spoke 1] --> Central
    B[Spoke 2] --> Central
    C[Spoke 3] --> Central
```

