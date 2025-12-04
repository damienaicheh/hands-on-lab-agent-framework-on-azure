---
description: MOAW (Microsoft Open-source Academy Workshops) workshop implementation guidelines
applyTo: '**/docs/**/*.md,**/workshop*.md'
---

# MOAW Workshop Implementation Guidelines

This project uses the [MOAW (Microsoft Open-source Academy Workshops)](https://aka.ms/moaw) format for creating and hosting workshops.

## Workshop Structure

### Front Matter (Required)

Every workshop must start with YAML front matter containing:

```yaml
---
published: true                         # Set to true to publish the workshop
type: workshop                          # Required: must be 'workshop'
title: Full workshop title              # Required: Full title of the workshop
short_title: Short title for header     # Optional: Short title for header
description: This is a workshop for...  # Required: Description of the workshop
level: beginner                         # Required: 'beginner', 'intermediate' or 'advanced'
authors:                                # Required: List of authors
  - Author Name
contacts:                               # Required: Must match number of authors
  - "@author_handle"
duration_minutes: 120                   # Required: Estimated duration in minutes
tags: tag1, tag2, tag3                  # Required: Tags for filtering and searching
banner_url: assets/banner.jpg           # Optional: Should be 1280x640px image
video_url: https://youtube.com/link     # Optional: Link to workshop video
audience: students                      # Optional: Target audience
navigation_numbering: false             # Optional: Enable/disable section numbering
navigation_levels: 3                    # Optional: Number of heading levels in navigation
wt_id: <cxa_tracking_id>                # Optional: Advocacy tracking code
oc_id: <marketing_tracking_id>          # Optional: Marketing tracking code
sections_title:                         # Optional: Custom section titles
  - Section 1 title
  - Section 2 title
---
```

## Section Separators

Create multiple workshop sections (pages) by separating them with `---` (three dashes), preceded and followed by empty lines:

```markdown
# Section 1 Content

Some content here...

---

# Section 2 Content

More content here...
```

## Admonitions

Use special syntax for admonitions to highlight important information:

```markdown
<!-- Information note -->
<div class="info" data-title="Note">

> Important information here

</div>

<!-- Warning note -->
<div class="warning" data-title="Warning">

> Warning message here

</div>

<!-- Important note -->
<div class="important" data-title="Important">

> Critical information here

</div>

<!-- Tip note -->
<div class="tip" data-title="Tip">

> Helpful tip here

</div>

<!-- Task or assignment -->
<div class="task" data-title="Task">

> Task description here

</div>
```

## Assets

- Store all assets (images, files, sample code) in the `/assets` folder inside your workshop folder
- Use relative paths to reference assets: `assets/image.png`
- Banner images should be 1280x640px

## Workshop URL Format

- Main workshop: `https://aka.ms/ws?src=<workshop_folder>/`
- From GitHub: `https://aka.ms/ws?src=gh:<github_repo/path_to_file>`
- Specific section: `&step=<section_index>#<heading_id>`

## Translations

- Create translations in a `translations` folder
- Name format: `<original_name>.<country_code>.<extension>`
- Example: `translations/workshop.fr.md` for French

## Best Practices

1. Keep sections focused and concise
2. Use clear, action-oriented headings
3. Include estimated duration for each section
4. Add prerequisites section at the beginning
5. Include verification steps after each major task
6. Use code blocks with language identifiers for syntax highlighting
7. Add screenshots for complex UI interactions
8. Include troubleshooting tips where appropriate
