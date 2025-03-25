# ![](/git_assets/tx_logo.png)

## How It Works

Texture Packs work by overwriting the default textures in the game with your own. By default the game looks for the texture in the active texture pack folder. If the texture is not found in the active texture pack folder, it will use the default texture.

## File organization
![Namespace Folder](/git_assets/folder.png) `namespace`

![](/git_assets/I-.png) ![Assets Folder](/git_assets/folder.png) `assets`

![](/git_assets/I.png) ![](/git_assets/I-.png) ![Modded](/git_assets/folder_.png) [`modded`](#modded)

![](/git_assets/I.png) ![](/git_assets/-.png) ![UI Folder](/git_assets/folder.png) `ui`

![](/git_assets/I.png) ![](/git_assets/blank.png) ![](/git_assets/-.png) ![UI Image File](/git_assets/m_png.png) [`UI Images`](#ui-images)

![](/git_assets/I-.png) ![Data Folder](/git_assets/folder.png) `data`

![](/git_assets/I.png) ![](/git_assets/blank.png) ![](/git_assets/-.png) ![Data Image File](/git_assets/m_json.png) [`UI Json`](#ui-json)

![](/git_assets/I-.png) ![Mod Image File](/git_assets/png.png)`mod.png`

![](/git_assets/-.png) ![Mod Json File](/git_assets/json.png)`mod.json`

## Splicing
Splicing data is contained within a ![](/git_assets/json.png) `.json` file. These files are used to describe to divide an image file to fit an area such as a button.

Example splicing data:
```json
{
    "slices": {
        "(0, 0)": [[0, 0], [7, 7]],
        "(1, 0)": [[8, 0], [23, 7]],
        "(2, 0)": [[24, 0], [31, 7]],

        "(0, 1)": [[0, 8], [7, 23]],
        "(1, 1)": [[8, 8], [23, 23]],
        "(2, 1)": [[24, 8], [31, 23]],

        "(0, 2)": [[0, 24], [7, 31]],
        "(1, 2)": [[8, 24], [23, 31]],
        "(2, 2)": [[24, 24], [31, 31]]
    }
}
```
This is a 32x32 image file before the splicing operation.

![Not Spliced](/git_assets/splicing/not_spliced.png)

This is how the image file will be broken up based on the above splicing data.

![Spliced](/git_assets/splicing/spliced.png)

## Modded

![Modded](/git_assets/folder_.png) `modded`

![](/git_assets/-.png) ![Namespace Folder](/git_assets/folder.png) `default`

![](/git_assets/blank.png) ![](/git_assets/I-.png) ![Mover Cell](/git_assets/folder.png) `mover`

![](/git_assets/blank.png) ![](/git_assets/I.png) ![](/git_assets/I-.png) ![Mover Image](/git_assets/png.png) `mover.png`

![](/git_assets/blank.png) ![](/git_assets/I.png) ![](/git_assets/-.png) ![Mover Splicing](/git_assets/png.png) `mover.bloom.png`

![](/git_assets/blank.png) ![](/git_assets/-.png) ![Slider Cell](/git_assets/folder.png) `slider`

![](/git_assets/blank.png) ![](/git_assets/blank.png) ![](/git_assets/I-.png) ![Slider Image](/git_assets/png.png) `slider.png`

![](/git_assets/blank.png) ![](/git_assets/blank.png) ![](/git_assets/-.png) ![Slider Splicing](/git_assets/png.png) `slider.bloom.png`

#

`default` is the namespace of the mod.

`mover` and `slider` are the names of the cells you wish to overwrite textures for.

In those folders you can place a `.png` file which has the same name as the texture you wish to overwrite. In thise case it's the same as the name of the cell.

The files ending in `.bloom.png` are files that indicate the how the bloom is applied to the texture. When the bloom setting is enabled the texture will be multiplied by the bloom texture.