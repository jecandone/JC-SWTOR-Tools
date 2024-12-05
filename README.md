The tools here allow for the import of armor into Blender, as well as adding a character creator.

**<h1>Enabling the Plugin</h1>**

Make sure to point to the path of your extracted SWTOR assets to the "resources" folder.  

##**Armor Import**##

Allows the import of armor via the ModelID and ColorSchemeID values.  To find this, search for any armor on https://swtor.jedipedia.net/en, for example "Havoc Squad Greaves".  Take a look under name under the appearance section, "ipp.mtx.season7.havoc_squad.legs".

![image](https://github.com/user-attachments/assets/e41e89f7-5304-4376-bd28-47c89034f5e8)

Search this value in the "node" section of the file reader (https://swtor.jedipedia.net/reader), and click on the node that pops up.  

![image](https://github.com/user-attachments/assets/7aae6d6b-5cd9-49d6-8135-028b378c0902)

Copy the value from "appAppearanceSlotModelID" to the appropriate "ModelID" part of the blender plugin, and do the same thing with the "ippColorScheme" value.  You can also select a body type.  

![image](https://github.com/user-attachments/assets/fcf00d82-a7fc-451f-b8c5-17e186f2e7a2)

Repeat this for any armor pieces to import, or leave them blank, and click "Import Armor" and the armor will import:

![image](https://github.com/user-attachments/assets/debbc5ab-bc90-48e2-b46f-f6fdb066478a)
