**<h1>JC SWTOR Tools</h1>**

The tools here allow for the import of armor into Blender, as well as adding a character creator.

**<h2>Enabling the Plugin</h2>**

Make sure to point to the path of your extracted SWTOR assets to the "resources" folder.  

**<h2>Sections of the Plugin<h2>**

**<h3>Armor Import</h3>**

Allows the import of armor via the ModelID and ColorSchemeID values.  To find this, search for any armor on https://swtor.jedipedia.net/en, for example "Havoc Squad Greaves".  Take a look under name under the appearance section, "ipp.mtx.season7.havoc_squad.legs".

![image](https://github.com/user-attachments/assets/e41e89f7-5304-4376-bd28-47c89034f5e8)

Search this value in the "node" section of the file reader (https://swtor.jedipedia.net/reader), and click on the node that pops up.  

![image](https://github.com/user-attachments/assets/7aae6d6b-5cd9-49d6-8135-028b378c0902)

Copy the value from "appAppearanceSlotModelID" to the appropriate "ModelID" part of the blender plugin, and do the same thing with the "ippColorScheme" value.  You can also select a body type.  

![image](https://github.com/user-attachments/assets/fcf00d82-a7fc-451f-b8c5-17e186f2e7a2)

Repeat this for any armor pieces to import, or leave them blank, and click "Import Armor" and the armor will import:

![image](https://github.com/user-attachments/assets/debbc5ab-bc90-48e2-b46f-f6fdb066478a)

**<h3>Armor Import (FQN)</h3>**

Allows for armor import by looking up FQN values.  Some armor pieces have part of their name in the FQN value (ie the havoc squad armor, shae vizla armor, satele shan armor, etc), but others do not.  If the armor you're searching for doesn't appear likely the FQN name and the in-game name are different, and the FQN name would need to be looked up manually at Jedipedia).  If after a game update, an armor does not appear (since the file holding all the info for the FQN names and related values needs to be updated manually), then the other Armor Import section can be used by looking up the ModelID and the ColorSCheme.

**<h3>Save Texture Files</h3>**

Takes any textures inside the scene, saves them to the folder specified, and updates the Blender file to reference the textures in the newly saved location.  Useful for saving textures file in a different folder when using the armor import function, but can also be used if for any other purposes, such as if a .gr2 file was manually imported and the process materials function from the ZG SWTOR Tools.

**<h3>Dye Import</h3>**

Ability to search for any dye file in the game, and import it into the active object & material as node groups.  Using either of the import armor functions, the primary and secondary color scheme values get applied as node groups.  One can use this to import a dye color, then just change the node group name on the node groups that are connected to the armor shader to the name of the dye that was just imported to change the colors of the armor.  Like the FQN armor import function, the dye names and associated color scheme values need to be manually updated if new dyes get added to the game.  

**<h3>Node Groups to SWTOR Garment Shader</h3>**

Since dyes get applied as node groups, this function adds node groups to an active object that has a ZG SWTOR Garment Shader.  Intended to be able to quickly apply different dye colors.  

**<h3>Character Creation</h3>**

Import character based on input settings.  Contains the following features:

- Rename/Group Objects: Rename all objects and materials, and put them into a seperate group, based on the input of the "Character Name" field
- Normal Skeleton Import: Import & parent objects to the normal/default skeleton
- JC Skeleton/Empty: Import & parent object to a modified version of the normal skeleton - deleted VFX bones, parented the skeleton to a plain axis empty, and added two single arrow empties parented to the plain axis empty.
- Create Folder Structure: Saves materials to selected folder directory
- Character Preview: Press the "Preview" button to preview the current character.  Character by default is in one of the character creation poses, uncheck the "Preview Pose" to not use this pose and use an unposed character in the preview
- Existing Character - Import Settings: Import an existing character created with this plugin - opens up a text editor window to paste in settings.
- Export Character JSON: Creates paths.json, skeleton.json, preset.json, creates folder structure, and saves material files to folders - for using with ZG SWTOR Tool Character Importer.
- Randomize: Randomizes the various input options (excluding the armor options).  Each input option has a lock button to exclude it from the randomizing function.
- Keep Head (Skin) Model: Default is having this checked - having this option unchecked does not import the head (skin) objects.
- TORC or Game corruption values: Ssee "Global Settings" tab - TORC and the ingame files calculate eye color values for corruption levels differently, one can pick either option to use.

Other features/items worth mentioning - there is a "unify to Chest Colors" option in the "Dye Color: Overall" field, to be able to use the equivelent of the in game feature for unifying to chest piece.  All imports for hair with either of the skeleton parenting option enables auto fixex the vertex groups and sets them all to the "head" vertex group. 

Issues/Notes - for certain armor pieces (for example, many chest armor pieces that have a hood), this plugin will import all attachments to armor pieces, and sometimes the game only uses part of the attachments for an armor set.  One can just delete the excess attachments after import to fix this.  Similar issue for "hair" objects (ie hair, twilek headbands) and "facehair" objects (facehair, jewelery), this will import all attachments for these, and the game only uses part of the attachents for them.  One can delete the excess attachment pieces to get the "Hair" or "facehair" to the proper ingame version of it.

**<h2>Source Files and Updating References Files</h2>**
