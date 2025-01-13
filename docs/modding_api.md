# ![](/git_assets/api_logo.png)

## Overview
- Introduction to the modding system
- Key concepts and terminology
- Getting started with mod development

## Setup & Installation
- Prerequisites
- Development environment setup
- Required dependencies

## Mod Structure
- File organization
- Required manifest files
- Resource management
- Asset handling

## Core API Reference
- Cell types and properties
- Grid manipulation functions
- Event system
- Tick system

## Creating Custom Cells
- Base cell class
- Cell properties and attributes
- Behavior implementation
- Collision handling
- Texture and appearance

## Examples
- Basic mod template
- Custom cell creation
- Event handling examples
- Advanced modification samples

## Best Practices
- Performance optimization
- Code organization
- Testing guidelines
- Common pitfalls

## API Reference
- Complete function listing
- Class documentation
- Property definitions
- Constants and enums

## Troubleshooting
- Common issues
- Debug tools
- Error handling
- Support resources

## Version Compatibility
- API version history
- Breaking changes
- Migration guides

---

# Overview
## Introduction to the modding system
## Key concepts and terminology
## Getting started with mod development

# Setup & Installation
## Prerequisites
- You must have PyCellMachine installed on your device.
- You must have a basic understanding of Python programming with knowledge on Classes, Functions, and Variables.
## Development environment setup
- It is recommended to use a code editor like Visual Studio Code or PyCharm when making your mod.
   - [Visual Studio Code](https://code.visualstudio.com/)
   - [PyCharm](https://www.jetbrains.com/pycharm/)
## Required dependencies
- [Python](https://www.python.org/)
- [Pygame Community Edition](https://github.com/pygame-community/pygame-ce)

# Mod Structure
## File organization
![Namespace Folder](/git_assets/folder.png) `namespace`

![](/git_assets/I-.png) ![Cells Folder](/git_assets/folder.png) `cells`

![](/git_assets/I.png) ![](/git_assets/-.png) ![Cell Folder](/git_assets/folder.png) `cell_name`

![](/git_assets/I.png) ![](/git_assets/blank.png) ![](/git_assets/I-.png) ![Cell Image File](/git_assets/png.png)`cell.png`

![](/git_assets/I.png) ![](/git_assets/blank.png) ![](/git_assets/I-.png) ![Cell Python File](/git_assets/py.png)`cell.py`

![](/git_assets/I.png) ![](/git_assets/blank.png) ![](/git_assets/-.png) ![Cell Json File](/git_assets/json.png)`cell.json`

![](/git_assets/I-.png) ![Mod Image File](/git_assets/png.png)`mod.png` / `mod.gif`

![](/git_assets/-.png) ![Mod Json File](/git_assets/json.png)`mod.json`
## Required manifest files
![Mod Json File](/git_assets/json.png)`mod.json`
```json
{
    "format": 1,
    "name": "Mod Name",
    "description": "Mod Description",
    "author": "Author(s)",
    "version": "1.0.0",
    "thumbnail_type": "png"
}
```
`format` - The format of the mod.json file.

`name` - The name of the mod.

`description` - A brief description of the mod.

`author` - The author(s) of the mod.

`version` - The version of the mod.

`thumbnail_type` - The type of thumbnail image to use.

##

![Cell Json File](/git_assets/json.png)`cell.json`
```json
{
    "name": "Cell Name",
    "description": "Cell Description",
    "texture": {
        "mode": "standard",
        "texture": "texture.png"
    }
}
```
`name` - The name of the cell.

`description` - A brief description of the cell.

`texture` - The texture of the cell. (Subject to be moved to `cell.py` for more customization options)

- `mode` - The mode of the texture.

   - `standard` - Single image file that rotates when the cell rotates.
      - `texture` - The image file to use.
   - `animated` - Gif file that rotates when the cell rotates.
      - `texture` - The gif file to use.
   - `static` - Seperate image file for each cell rotation.
      - `0` - North
      - `1` - East
      - `2` - South
      - `3` - West
   - `static_animated` - Seperate gif file for each cell rotation.
      - `0` - North
      - `1` - East
      - `2` - South
      - `3` - West

##

## Resource management
## Asset handling

# Core API Reference
## Cell types and properties
## Grid manipulation functions
## Event system
## Tick system

# Creating Custom Cells
## Base cell class
## Cell properties and attributes
## Behavior implementation
## Collision handling
## Texture and appearance

# Examples
## Basic mod template
## Custom cell creation
## Event handling examples
## Advanced modification samples

# Best Practices
## Performance optimization
## Code organization
## Testing guidelines
## Common pitfalls

# API Reference
## Complete function listing
## Class documentation
## Property definitions
## Constants and enums

# Troubleshooting
## Common issues
## Debug tools
## Error handling
## Support resources

# Version Compatibility
## API version history
## Breaking changes
## Migration guides