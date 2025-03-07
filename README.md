**<h1>JC SWTOR Tools</h1>**

Tools built for Blender 3.6 (and tested in Blender 3.6.7) to be able to do various functions for SWTOR:
- Armor Import
- Dye Import
- Character Creation
- NPC Import

This plugin uses information on armor and character creation properties that is stored in the plugin directory from game update from update 7.5.1 (Oct. 1, 2024).  Character selection properties added after this will not appear, and neither will armor that have been added after this.  However, armor pieces from future updates can still be added via the "Armor Import (Non-FQN)", as long as the extracted assets are up to date. 

**<h2>Prerequisites/Enabling the Plugin</h2>**

This plugin makes use of the "ZeroGravitas SWTOR Tools" (https://github.com/SWTOR-Slicers/ZG-SWTOR-Tools) for importing objects and material processing.  This in turn requires the use of the .gr2 importer (https://github.com/SWTOR-Slicers/Granny2-Plug-In-Blender-2.8x/releases/tag/4.0.6).

Built and tested this plugin with the "2024-09" version of the ZG SWTOR Tools and the v4.0.4 of the .gr2 importer.

When enabling the plugin through Blender, make sure to point the input directory to the "resources" folder of your extracted SWTOR assets.  

**<h2>Sections of the Plugin<h2>**

**<h3>Armor Import (Non-FQN)</h3>**

Allows the import of armor via the ModelID, MaterialID, ColorSchemeID values.  To find this, search for any armor on https://swtor.jedipedia.net/en, for example "Havoc Squad Greaves".  Take a look under name under the appearance section, "ipp.mtx.season7.havoc_squad.legs".

![image](https://github.com/user-attachments/assets/e41e89f7-5304-4376-bd28-47c89034f5e8)

Search this value in the "node" section of the file reader (https://swtor.jedipedia.net/reader), and click on the node that pops up.  

![image](https://github.com/user-attachments/assets/7aae6d6b-5cd9-49d6-8135-028b378c0902)

Copy the value from "appAppearanceSlotModelID" to the appropriate "ModelID" part of the blender plugin, "appAppearanceSlotMaterialIndex" to the Material ID field, and "ippColorScheme" to the Color Scheme ID field.  Select the body type of the armor that you want to import from the dropdown.

![image](https://github.com/user-attachments/assets/b77033ed-40b5-46ed-bca1-57412a3b4bda)

Repeat this for any other armor pieces or slots to import, or leave them blank, and click "Import Armor" and the armor will import:

![image](https://github.com/user-attachments/assets/6d5c4c72-77b0-433f-9029-e432104c4200)

This can be helpful if the armor source files have not been updated for future game armors.  Instead of doing the whole process manually, you can still use the Model ID, Material ID, and Color Scheme ID to import armor that is not in armor source files, as long as it is in the extracted assets directory. 

**<h3>Armor Import (FQN)</h3>**

Allows for armor import by looking up either in-game (English) name values or by FQN values (if set in "Global Settings").  Note that many armor values have been translated from their FQN name to their in game name, but not all.  If in searching for an armor by it's in-game name, search for it by its FQN name and it most likely will be in there, unless it has been added after the last time the armor source files were updated.

**<h3>Save Texture Files</h3>**

Takes textures, saves them to the folder specified, and updates the Blender file to reference the textures in the newly saved location.  Useful for saving textures file in a different folder when using the armor import function, but can also be used if for any other purposes, such as if a .gr2 file was manually imported and the process materials function from the ZG SWTOR Tools was used, and one wanted to save the textures to a different folder.  Can be done for the entire scene or just for selected objects.

**<h3>Dye Import</h3>**

Ability to search for any dye file in the game, and import it into the active object & material as node groups.  Using either of the import armor functions, the primary and secondary color scheme values get applied as node groups.  One can use this to import a dye color, then just change the node group name on the node groups that are connected to the armor shader to the name of the dye that was just imported to change the colors of the armor.  Like the FQN armor import function, the dye names and associated color scheme values need to be manually updated if new dyes get added to the game.  

**<h3>Node Groups to SWTOR Garment Shader</h3>**

Since dyes get applied as node groups, this function adds node groups to an active object that has an existing ZG SWTOR Garment Shader without node groups created & connected.  Intended to be able to quickly apply different dye colors to previously created SWTOR nodes.  

**<h3>Character Creation</h3>**

Import character based on input settings.  Contains the following features:

- Rename/Group Objects: Rename all objects and materials, and put them into a seperate group, based on the input of the "Character Name" field
- Normal Skeleton Import: Import & parent objects to the normal/default skeleton
- JC Skeleton/Empty: Import & parent object to a modified version of the normal skeleton - deleted VFX bones and bones set to display "in-front", parented the skeleton to a plain axis empty, and added two single arrow empties parented to the plain axis empty.
- Create Folder Structure: Saves materials to selected folder directory.  Generates a .txt file inside the folder with the character settings, to be able to be used with the existing character import feature.
- Character Preview: Press the "Preview" button to preview the current character.  Character by default is in one of the character creation poses, uncheck the "Preview Pose" to not use this pose and use an unposed character in the preview
- Existing Character - Import Settings: Import an existing character created with this plugin - opens up a text editor window to paste in settings.
- Export Character JSON: Creates paths.json, skeleton.json, preset.json, creates folder structure, and saves material files to folders - for using with ZG SWTOR Tool Character Importer.
- Randomize: Randomizes the various input options (excluding the armor options).  Each input option has a lock button to exclude it from the randomizing function.
- Keep Head (Skin) Model: Default is having this checked - having this option unchecked does not import the head (skin) objects.  For use if importing a helmet, and don't want to import the head/hair.  
- TORC or Game corruption values: See "Global Settings" tab - TORC and the ingame files calculate eye color values for corruption levels differently, one can pick either option to use.

Other features/items worth mentioning - there is a "Unify to Chest Colors" option in the "Dye Color: Overall" field, to be able to use the equivalent of the in game feature for unifying to chest piece.  All imports for hair with either of the skeleton parenting option enabled auto fixes the vertex groups and sets them all to the "head" vertex group. 

Issues/Notes - for certain armor pieces (for example, many chest armor pieces that have a hood), this plugin will import all attachments to armor pieces, and sometimes the game only uses part of the attachments for an armor set.  One can just delete the excess attachments after import to fix this.  Similar issue for "hair" objects (ie hair, twilek headbands) and "facehair" objects (facehair, jewelery), this will import all attachments for these, and the game only uses part of the attachments for them.  One can delete the excess attachment pieces to get the "Hair" or "facehair" to the proper in-game version of it.

**<h3>NPC Import</h3>**

Import NPCs.  This allows import of regular (non-creature, ie Kira Carsen) NPCs, as well as creature (both humanoid, ie Lana and non-humanoid, ie kath hound) NPCs.  To use this feature:

Go to the Jedipedia database section (https://swtor.jedipedia.net/en), and search for an NPC, and select the NPC you want to import.  For example Nadia Grell, Alliance version of the character.  Look under the appearance section, and the FQN, and copy this.  In this example, "npp.daily_area.ossus.world.republic.nadia_grell".    

![image](https://github.com/user-attachments/assets/102f4fd7-84f6-4701-a03c-f18b99b466ae)

Go to the Jedipedia File Reader, to the node section, search for the node, and open it.  

![image](https://github.com/user-attachments/assets/358c9171-5a00-4ea6-9f77-0ab534de15d2)

Once this is selected, select all (control-a), and copy it (control-c). 

Go to Blender, and under the "NPC Import" section, click the "NPC - Load Settings" button.  This opens up a text editor window.  Paste the text that was copied from the node from Jedipedia, then press the "NPC - Store Settings", and the text editor window pop up will go away.

![image](https://github.com/user-attachments/assets/7e0e6c32-e554-4a11-b62f-952a29756ecb)

Once the settings are stored, the NPC can be previewed (has the same Preview Pose option as the Character Creation section), or Imported.  The "NPC - Settings Stored" button can be clicked to change or reenter the NPC data if desired.  This section has the same options as the character creation for Rename/Group Objects, Parent to Normal Skeleton, Parent to JC Skeleton/Empty, and Create Folder Structure.  

Unique to the NPC Import is the "Special Eye Material" and the "2nd Material Slot - Non-Skin Material" options.  

Some NPCs on Jedipedia (for example, one of the pre-KOTFE Lana NPCs), have special eye materials, and they don't appear in the Appearance FQN node.  To get around this, one would need to click on the "Special Eye Material" checkbox, then go back to the database page for Jedipedia of the NPC (not the node in the reader), and look under head, and get the eye material name.  One would then need to put that name into the input box for the special eye material.  

![image](https://github.com/user-attachments/assets/c2b31a5f-56b8-40bd-a2d4-5360743d9653)

Some NPCs (for example Kira Carsen Post KOTFE, Lana pre-KOTFE) have armor leg pieces that import with a second material slot, and this second material slot will normally be processed as a skin material, even though in the actual NPC this is an armor material, not a skin shader.  To fix this, select the "2nd Material Slot - Non-Skin Material" option, and the second material slot in the leg will be correctly set as an armor material.  If one is unsure if an NPC has this or not, this can be tried out in the preview for NPCs to determine which of these two options need to be selected.

Some NPCs can have multiple enteries for some of the slots (ie multiple skin color options, multiple eye color options, etc).  These will show up as additional lines in Jedpedia (ie for multiple skin color options, instead of just displaying "1", it can have "1", "2", "3", "4", as the start of different entries for different skin color options).  One can delete entries for options they don't want to create different versions of the same NPC from the same NPC data.  

**<h3>Global Settings</h3>**

Armor Language - can set the language of the armor names - currently only "English", and "FQN" (ie displaying the FQN names instead of the in-game names) are functional.

Corruption Values - corruption values for eyes in the TORC Character Creator are slightly different than those calculated by the values derived directly from the in-game nodes - can choose between using the TORC values or the in-game corruption values for eyes.

![image](https://github.com/user-attachments/assets/5435be43-3046-4b81-a4b9-eb02824ad4f0)

Material Processing - Choose between the process for processing material file - using the default method (ZG SWTOR Tools), or using a custom version of it that can be tried if the default method has issues.

Preview Render Engine - set the render engine for the character creation and NPC import preview - choose between Eevee or Cycles.

Direction Maps - Enables or disables the direction map texture slot on hair & facehair import.  Leaving this enabled will leave the texture slot in - if a direction map is not used a hair will appear as a pink color.  Disabling this will mute the direction map node.

Debugging outputs - write the debugging output to a file for various functions of the plugin instead of writing it to a console.  Note that if chosen for a particular function, it will not output the debugging code to the system console.

