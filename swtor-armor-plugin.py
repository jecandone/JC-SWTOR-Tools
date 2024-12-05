bl_info = {
    "name": "JC SWTOR Tools",
    "author": "JC",
    "version": (0, 2),
    "blender": (3, 6, 0),
    "location": "View3D > N-Panel > JC SWTOR Tools",
    "description": "Import SWTOR armor pieces",
    "category": "Import-Export",
}

import bpy
import os
import shutil
import csv
import os.path
import xml.etree.ElementTree as ET
from bpy.props import StringProperty, PointerProperty, EnumProperty
from bpy.types import (Panel, 
                      Operator,
                      AddonPreferences,
                      PropertyGroup)
                      
# Define body type items
BODY_TYPE_ITEMS = [
    ('bfa', 'bfa (Female BT1)', 'Female Body Type 1'),
    ('bfn', 'bfn (Female BT2)', 'Female Body Type 2'),
    ('bfs', 'bfs (Female BT3)', 'Female Body Type 3'),
    ('bfb', 'bfb (Female BT4)', 'Female Body Type 4'),
    ('bma', 'bma (Male BT1)', 'Male Body Type 1'),
    ('bmn', 'bmn (Male BT2)', 'Male Body Type 2'),
    ('bms', 'bms (Male BT3)', 'Male Body Type 3'),
    ('bmf', 'bmf (Male BT4)', 'Male Body Type 4'),
]

# Addon Preferences
class JCSWTORArmorImportPreferences(AddonPreferences):
    bl_idname = __name__

    import_directory: StringProperty(
        name="Import Directory",
        subtype='DIR_PATH',
        default="B:\\Downloads\\0_Games Mod\\SWTOR\\Assets_2023.12.16\\resources"
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "import_directory")

# Property Group
class ArmorImportProperties(PropertyGroup):
    def validate_input(self, value):
        """Remove any leading/trailing spaces from input"""
        if isinstance(value, str):
            return value.strip()
        return value

    body_type: EnumProperty(
        name="BodyType",
        items=BODY_TYPE_ITEMS,
        description="Select the body type"
    )
    
    face_model_id: StringProperty(
        name="FaceModelID",
        default="",
        update=lambda self, context: setattr(self, "face_model_id", self.validate_input(self.face_model_id))
    )
    face_color_scheme: StringProperty(
        name="FaceColorScheme",
        default="",
        update=lambda self, context: setattr(self, "face_color_scheme", self.validate_input(self.face_color_scheme))
    )
    chest_model_id: StringProperty(
        name="ChestModelID",
        default="",
        update=lambda self, context: setattr(self, "chest_model_id", self.validate_input(self.chest_model_id))
    )
    chest_color_scheme: StringProperty(
        name="ChestColorScheme",
        default="",
        update=lambda self, context: setattr(self, "chest_color_scheme", self.validate_input(self.chest_color_scheme))
    )
    hand_model_id: StringProperty(
        name="HandModelID",
        default="",
        update=lambda self, context: setattr(self, "hand_model_id", self.validate_input(self.hand_model_id))
    )
    hand_color_scheme: StringProperty(
        name="HandColorScheme",
        default="",
        update=lambda self, context: setattr(self, "hand_color_scheme", self.validate_input(self.hand_color_scheme))
    )
    wrist_model_id: StringProperty(
        name="WristModelID",
        default="",
        update=lambda self, context: setattr(self, "wrist_model_id", self.validate_input(self.wrist_model_id))
    )
    wrist_color_scheme: StringProperty(
        name="WristColorScheme",
        default="",
        update=lambda self, context: setattr(self, "wrist_color_scheme", self.validate_input(self.wrist_color_scheme))
    )
    waist_model_id: StringProperty(
        name="WaistModelID",
        default="",
        update=lambda self, context: setattr(self, "waist_model_id", self.validate_input(self.waist_model_id))
    )
    waist_color_scheme: StringProperty(
        name="WaistColorScheme",
        default="",
        update=lambda self, context: setattr(self, "waist_color_scheme", self.validate_input(self.waist_color_scheme))
    )
    leg_model_id: StringProperty(
        name="LegModelID",
        default="",
        update=lambda self, context: setattr(self, "leg_model_id", self.validate_input(self.leg_model_id))
    )
    leg_color_scheme: StringProperty(
        name="LegColorScheme",
        default="",
        update=lambda self, context: setattr(self, "leg_color_scheme", self.validate_input(self.leg_color_scheme))
    )
    feet_model_id: StringProperty(
        name="FeetModelID",
        default="",
        update=lambda self, context: setattr(self, "feet_model_id", self.validate_input(self.feet_model_id))
    )
    feet_color_scheme: StringProperty(
        name="FeetColorScheme",
        default="",
        update=lambda self, context: setattr(self, "feet_color_scheme", self.validate_input(self.feet_color_scheme))
    )

class TextureSaveProperties(PropertyGroup):
    output_directory: StringProperty(
        name="Output Directory",
        description="Directory to save texture files",
        default="",
        subtype='DIR_PATH'
    )

def get_dye_values(self, context):
    """Get all dye values from the CSV file"""
    dye_values = []
    try:
        addon_dir = os.path.dirname(os.path.realpath(__file__))
        csv_path = os.path.join(addon_dir, "DyeColors.csv")
        
        with open(csv_path, 'r') as file:
            reader = csv.reader(file, delimiter=' ')
            for row in reader:
                if len(row) >= 3:
                    dye_name = ' '.join(row[2:])
                    if dye_name.lower() != 'n/a' and '-' not in dye_name:
                        dye_values.append(dye_name)
    except Exception as e:
        print(f"Error loading dye colors: {str(e)}")
    
    return sorted(dye_values)  # Return sorted list of dye names

def update_enum_items(self, context):
    """Update dropdown items based on search query"""
    dye_values = get_dye_values(self, context)
    items = [(v, v, "") for v in dye_values if self.dye_search.lower() in v.lower()]
    if not items:
        items = [('NONE', 'None', '')]
    return items

# Add new property group for dye import
class DyeImportProperties(PropertyGroup):
    dye_search: StringProperty(
        name="Search Dye",
        description="Search for dye colors",
        default="",
        update=lambda self, context: self.update_search(context)
    )
    
    filtered_dye: EnumProperty(
        name="Dye Color",
        description="Select dye color",
        items=update_enum_items,
        update=lambda self, context: self.update_search_field(context)
    )

    slot_type: EnumProperty(
        name="Slot Type",
        description="Select slot type",
        items=[
            ('face', 'Face', ''),
            ('chest', 'Chest', ''),
            ('hand', 'Hand', ''),
            ('wrist', 'Wrist', ''),
            ('waist', 'Waist', ''),
            ('leg', 'Leg', ''),
            ('feet', 'Feet', '')
        ],
        default='chest'
    )

    def update_search(self, context):
        """Trigger UI update when search changes"""
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

    def update_search_field(self, context):
        """Update search field when selection is made"""
        self.dye_search = self.filtered_dye

def get_color_scheme_id(csv_path, dye_name):
    print(f"Searching for dye name: {dye_name}")
    try:
        with open(csv_path, 'r') as file:
            reader = csv.reader(file, delimiter=' ')
            for row in reader:
                if len(row) >= 3:
                    current_dye_name = ' '.join(row[2:])
                    print(f"Checking row - current_dye_name: {current_dye_name}, row data: {row}")
                    if current_dye_name == dye_name:
                        print(f"Found match! Color scheme ID: {row[1]}")
                        return row[1]  # Return the color scheme ID
    except Exception as e:
        print(f"Error reading CSV: {str(e)}")
    print("No matching dye name found")
    return None

def parse_dye_name(dye_name):
    """Parse dye name into primary and secondary colors"""
    if dye_name.lower() == 'n/a':
        return None, None
    elif '-' in dye_name:
        return None, None
    elif ' and ' in dye_name:
        parts = dye_name.split(' and ')
        # Handle special case with "Ancient Warrior's" etc.
        if "'" in parts[0]:
            primary = parts[0]
            secondary = f"{parts[0].split(chr(39))[0]}'s {parts[1]}"
        else:
            primary = parts[0]
            secondary = parts[1]
    elif '/' in dye_name:
        primary, secondary = dye_name.split('/')
        # Check for None values
        if primary.strip().lower() == 'none':
            primary = None
        if secondary.strip().lower() == 'none':
            secondary = None
    else:
        return None, None
        
    # Add dye_ prefix only to non-None values
    if primary:
        primary = f"dye_{primary.strip()}"
    if secondary:
        secondary = f"dye_{secondary.strip()}"
        
    return primary, secondary

class JCSWTOR_OT_apply_dye(Operator):
    bl_idname = "jcswtor.apply_dye"
    bl_label = "Import Dye"
    bl_description = "Import selected dye into active object as node groups"
    
    def execute(self, context):
        preferences = context.preferences.addons[__name__].preferences
        props = context.scene.dye_import_props
        
        # Check if an object is selected and has a material
        if not context.active_object or not context.active_object.active_material:
            self.report({'ERROR'}, "Active object not selected, or the active object does not have a material")
            return {'CANCELLED'}
            
        # Get dye name and validate
        dye_name = props.filtered_dye  # Updated to use filtered_dye instead of dye_name
        if dye_name.lower() == 'n/a':
            self.report({'ERROR'}, "Error: n/a dye name selected")
            return {'CANCELLED'}
        elif '-' in dye_name:
            self.report({'ERROR'}, "Error: non-dye color selected")
            return {'CANCELLED'}
            
        # Get color scheme ID
        addon_dir = os.path.dirname(os.path.realpath(__file__))
        csv_path = os.path.join(addon_dir, "DyeColors.csv")
        color_scheme_id = get_color_scheme_id(csv_path, dye_name)
       
        print(f"Retrieved color_scheme_id: {color_scheme_id}")
        if color_scheme_id:  # Only try to print lowercase if not None
            print(f"Lowercase version: {color_scheme_id.lower()}")
        else:
            print("color_scheme_id is None")

        if not color_scheme_id or color_scheme_id.lower() == 'n/a':
            self.report({'ERROR'}, "Invalid color scheme ID")
            return {'CANCELLED'}
        
        if not color_scheme_id or color_scheme_id.lower() == 'n/a':
            self.report({'ERROR'}, "Invalid color scheme ID")
            return {'CANCELLED'}
            
        # Get primary and secondary IDs
        primary_id, secondary_id = get_color_scheme_ids(
            preferences.import_directory,
            color_scheme_id,
            props.slot_type
        )
        
        if primary_id and secondary_id:
            # Get the garment hue files
            primary_file, secondary_file = get_garment_hue_files(
                preferences.import_directory,
                primary_id,
                secondary_id,
                props.slot_type
            )
            
            if primary_file and secondary_file:
                # Parse primary dye file
                primary_values = parse_garment_hue_xml(preferences.import_directory, primary_file, True)
                secondary_values = parse_garment_hue_xml(preferences.import_directory, secondary_file, False)
                
                # Get node group names
                primary_group_name, secondary_group_name = parse_dye_name(dye_name)
                if primary_group_name is None and secondary_group_name is None:
                    self.report({'ERROR'}, "Invalid dye name format")
                    return {'CANCELLED'}
                
                # Create and add node groups to material
                material = context.active_object.active_material
                
                # Create and add the node groups to the material
                primary_node, secondary_node = create_dye_nodes(
                    material, 
                    props.slot_type, 
                    primary_values if primary_group_name else None,
                    secondary_values if secondary_group_name else None
                )
                
                # Set the custom names
                if primary_node and primary_node.node_tree and primary_group_name:
                    primary_node.node_tree.name = primary_group_name
                if secondary_node and secondary_node.node_tree and secondary_group_name:
                    secondary_node.node_tree.name = secondary_group_name
                
                self.report({'INFO'}, f"Successfully applied {dye_name} dye")
                return {'FINISHED'}
        
        self.report({'ERROR'}, "Failed to apply dye")
        return {'CANCELLED'}

class JCSWTOR_OT_add_shader_nodes(Operator):
    bl_idname = "jcswtor.add_shader_nodes"
    bl_label = "Add Sockets/Nodes"
    bl_description = "Add node groups to SWTOR Garment Shader"

    def execute(self, context):
        # Check if there's an active object with material
        if not context.active_object or not context.active_object.active_material:
            self.report({'ERROR'}, "No active object selected or object does not have material")
            return {'CANCELLED'}

        material = context.active_object.active_material

        # Find SWTOR shader nodes
        swtor_nodes = [node for node in material.node_tree.nodes if node.name == "SWTOR"]

        # Check for exactly one SWTOR node
        if len(swtor_nodes) != 1:
            self.report({'ERROR'}, "No SWTOR Garment Node Shader or Multiple SWTOR Garment Node Shaders")
            return {'CANCELLED'}

        swtor_node = swtor_nodes[0]

        # Setup custom shader inputs from ChosenPalette
        setup_custom_shader_inputs(material)

        # Get the node tree for the shader group
        garment_group = swtor_node.node_tree
        if not garment_group:
            self.report({'ERROR'}, "Could not access SWTOR shader node tree")
            return {'CANCELLED'}

        # Find ChosenPalette node
        chosen_node = None
        for node in garment_group.nodes:
            if hasattr(node, 'node_tree') and "ChosenPalette" in node.node_tree.name:
                chosen_node = node
                break

        if not chosen_node:
            self.report({'ERROR'}, "Could not find ChosenPalette node")
            return {'CANCELLED'}

        # Get values from ChosenPalette node
        primary_values = {}
        secondary_values = {}

        # Extract values from ChosenPalette node inputs
        for input_name, socket in chosen_node.inputs.items():
            if input_name.startswith("Palette1"):
                if socket.type == 'RGBA':
                    primary_values[input_name] = [*socket.default_value][:3]  # Get RGB values
                else:
                    primary_values[input_name] = socket.default_value
            elif input_name.startswith("Palette2"):
                if socket.type == 'RGBA':
                    secondary_values[input_name] = [*socket.default_value][:3]  # Get RGB values
                else:
                    secondary_values[input_name] = socket.default_value

        # Generate unique names for node groups
        def get_unique_name(base_name):
            counter = 1
            while f"{base_name} ({counter})" in bpy.data.node_groups:
                counter += 1
            return f"{base_name} ({counter})"

        primary_name = get_unique_name("Dye_Primary")
        secondary_name = get_unique_name("Dye_Secondary")

        # Create and connect node groups
        primary_node, secondary_node = create_dye_nodes(material, "custom", primary_values, secondary_values)

        # Position nodes relative to SWTOR shader
        swtor_location = swtor_node.location
        if primary_node:
            primary_node.location = (swtor_location.x - 200, swtor_location.y - 650)
        if secondary_node:
            secondary_node.location = (swtor_location.x - 200, swtor_location.y - 850)

        # Rename node groups
        if primary_node and primary_node.node_tree:
            primary_node.node_tree.name = primary_name
        if secondary_node and secondary_node.node_tree:
            secondary_node.node_tree.name = secondary_name

        # Connect nodes to SWTOR shader
        if primary_node and secondary_node:
            links = material.node_tree.links

            # Connect primary node outputs
            for output_name in primary_node.outputs.keys():
                if output_name in swtor_node.inputs:
                    links.new(primary_node.outputs[output_name], swtor_node.inputs[output_name])

            # Connect secondary node outputs
            for output_name in secondary_node.outputs.keys():
                if output_name in swtor_node.inputs:
                    links.new(secondary_node.outputs[output_name], swtor_node.inputs[output_name])

        self.report({'INFO'}, f"Successfully added {primary_name} and {secondary_name} node groups")
        return {'FINISHED'}

def get_color_scheme_ids(import_dir, color_scheme_id, slot_type):
    """Get primary and secondary color IDs for a given color scheme and slot type"""
    if not color_scheme_id:
        return None, None
        
    # Map our input types to XML slot names
    slot_map = {
        "face": "face",
        "chest": "chest",
        "hand": "hand",
        "wrist": "bracer",
        "waist": "waist",
        "leg": "leg",
        "feet": "boot",     # Add mapping for feet to boot
        "boot": "boot"      # Also allow direct boot reference
    }
    
    # Get the XML slot name
    xml_slot_name = slot_map.get(slot_type)
    if not xml_slot_name:
        print(f"Invalid slot type: {slot_type}")
        return None, None
        
    try:
        # Construct path to index.xml
        xml_path = os.path.join(import_dir, "art", "dynamic", "colorscheme", "index.xml")
        
        if not os.path.exists(xml_path):
            print(f"Error: Could not find ColorScheme index.xml at {xml_path}")
            return None, None
            
        # Parse XML file
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # Find the asset with matching ID
        for asset in root.findall('Asset'):
            asset_id = asset.find('ID')
            if asset_id is not None and asset_id.text == color_scheme_id:
                # Find ColorScheme in CustomData
                color_scheme = asset.find('.//ColorScheme')
                if color_scheme is not None:
                    # Find matching slot
                    for slot in color_scheme.findall('slot'):
                        if slot.get('name') == xml_slot_name:
                            primary_id = slot.get('primary')
                            secondary_id = slot.get('secondary')
                            
                            print(f"{slot_type.capitalize()} Primary Color Scheme is {primary_id}")
                            print(f"{slot_type.capitalize()} Secondary Color Scheme is {secondary_id}")
                            
                            return primary_id, secondary_id
                            
        print(f"No color scheme found with ID: {color_scheme_id} for slot: {xml_slot_name}")
        return None, None
        
    except ET.ParseError as e:
        print(f"Error parsing XML file: {str(e)}")
        return None, None
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return None, None

def get_garment_hue_files(import_dir, primary_id, secondary_id, slot_type=""):  # Add slot_type parameter
    """Get garment hue filenames for primary and secondary IDs"""
    xml_path = os.path.join(import_dir, "art", "dynamic", "garmenthue", "index.xml")
    
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        primary_file = None
        secondary_file = None
        
        # Look up primary ID
        for asset in root.findall('Asset'):
            asset_id = asset.find('ID')
            if asset_id is not None and asset_id.text == primary_id:
                base_file = asset.find('BaseFile')
                if base_file is not None:
                    primary_file = os.path.basename(base_file.text)
                    print(f"{slot_type.capitalize()} Primary Dye Garment File is {primary_file}")
                break
                
        # Look up secondary ID
        for asset in root.findall('Asset'):
            asset_id = asset.find('ID')
            if asset_id is not None and asset_id.text == secondary_id:
                base_file = asset.find('BaseFile')
                if base_file is not None:
                    secondary_file = os.path.basename(base_file.text)
                    print(f"{slot_type.capitalize()} Secondary Dye Garment File is {secondary_file}")
                break
                
        return primary_file, secondary_file
        
    except Exception as e:
        print(f"Error processing face garment hue files: {str(e)}")
        return None, None

def parse_garment_hue_xml(import_dir, xml_filename, is_primary=True):
    """Parse garment hue XML file and extract values"""
    if not xml_filename:
        return None
    
    # Construct path to XML file
    xml_path = os.path.join(import_dir, "art", "dynamic", "garmenthue", xml_filename)
    
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # Dictionary to store values
        values = {}
        prefix = "Palette1" if is_primary else "Palette2"
        
        # Get basic float values
        value_mappings = {
            f"{prefix} Hue": "Hue",
            f"{prefix} Saturation": "Saturation",
            f"{prefix} Brightness": "Brightness",
            f"{prefix} Contrast": "Contrast"
        }
        
        for node_name, xml_tag in value_mappings.items():
            element = root.find(xml_tag)
            if element is not None:
                value = float(element.text)
                values[node_name] = value
                print(f"{node_name}: {value}")
        
        # Get RGB values
        rgb_mappings = {
            f"{prefix} Specular": "Specular",
            f"{prefix} Metallic Specular": "Metallicspecular"
        }
        
        for node_name, xml_tag in rgb_mappings.items():
            element = root.find(xml_tag)
            if element is not None:
                # Split RGB values and discard alpha
                rgb_values = [float(x.strip()) for x in element.text.split(',')][:3]
                values[node_name] = rgb_values
                print(f"{node_name}: R={rgb_values[0]}, G={rgb_values[1]}, B={rgb_values[2]}")
        
        return values
        
    except ET.ParseError as e:
        print(f"Error parsing face garment hue XML file {xml_path}: {str(e)}")
        return None
    except Exception as e:
        print(f"Unexpected error processing garment hue file: {str(e)}")
        return None

def create_dye_node_group(material, slot_type, xml_values, is_primary=True):
    """Create and setup a dye node group"""
    # Create the node group name
    prefix = "Dye_Primary_Default" if is_primary else "Dye_Secondary_Default"
    group_name = f"{prefix}_{slot_type}"
    
    # Create new node group
    node_group = bpy.data.node_groups.new(name=group_name, type='ShaderNodeTree')
    
    # Create output node in group
    group_outputs = node_group.nodes.new('NodeGroupOutput')
    group_outputs.location = (300, 0)
    
    # Setup output sockets
    value_outputs = ["Hue", "Saturation", "Brightness", "Contrast"]
    rgb_outputs = ["Specular", "Metallic Specular"]
    
    prefix = "Palette1" if is_primary else "Palette2"
    
    # Create value outputs
    for i, name in enumerate(value_outputs):
        full_name = f"{prefix} {name}"
        node_group.outputs.new('NodeSocketFloat', full_name)
        
        # Create value node and set value
        value_node = node_group.nodes.new('ShaderNodeValue')
        value_node.location = (0, -i * 100)
        if full_name in xml_values:
            value_node.outputs[0].default_value = xml_values[full_name]
            
        # Connect to output
        node_group.links.new(value_node.outputs[0], group_outputs.inputs[full_name])
    
    # Create RGB outputs
    for i, name in enumerate(rgb_outputs):
        full_name = f"{prefix} {name}"
        node_group.outputs.new('NodeSocketColor', full_name)
        
        # Create RGB node and set value
        rgb_node = node_group.nodes.new('ShaderNodeRGB')
        rgb_node.location = (0, -(len(value_outputs) + i) * 100)
        if full_name in xml_values:
            rgb_node.outputs[0].default_value = (*xml_values[full_name], 1.0)
            
        # Connect to output
        node_group.links.new(rgb_node.outputs[0], group_outputs.inputs[full_name])
    
    return node_group

def setup_custom_shader_inputs(material, color_scheme=None):
    """Setup custom inputs in the SWTOR Garment Shader node group"""
    if not material or not material.node_tree:
        return
        
    # Find the SWTOR shader node
    garment_node = None
    for node in material.node_tree.nodes:
        if node.name == "SWTOR":
            garment_node = node
            break
            
    if not garment_node:
        return
        
    # Get the node tree for the shader group
    garment_group = garment_node.node_tree
    if not garment_group:
        return
        
    # Get the ChosenPalette node inside the shader
    chosen_node = None
    for node in garment_group.nodes:
        if hasattr(node, 'node_tree') and "ChosenPalette" in node.node_tree.name:
            chosen_node = node
            break
            
    if not chosen_node:
        return

    # Create a new Group Input node if it doesn't exist
    group_input = None
    for node in garment_group.nodes:
        if node.type == 'GROUP_INPUT':
            group_input = node
            break
    
    if not group_input:
        group_input = garment_group.nodes.new('NodeGroupInput')
    
    # Position the group input node to the left of the ChosenPalette node
    group_input.location = (chosen_node.location.x - 300, chosen_node.location.y)
    
    # Define all the input names we want to create and connect
    input_names = [
        "Palette1 Hue", "Palette1 Saturation", "Palette1 Brightness", "Palette1 Contrast",
        "Palette1 Specular", "Palette1 Metallic Specular",
        "Palette2 Hue", "Palette2 Saturation", "Palette2 Brightness", "Palette2 Contrast",
        "Palette2 Specular", "Palette2 Metallic Specular"
    ]
    
    # Create inputs in the group and connect them
    for input_name in input_names:
        # Create the input in the group if it doesn't exist
        if input_name not in garment_group.inputs:
            new_input = garment_group.inputs.new('NodeSocketFloat', input_name)
            new_input.min_value = 0.0
            new_input.max_value = 1.0
        
        # Create the connection to the ChosenPalette node
        if input_name in chosen_node.inputs:
            # Create link between group input and ChosenPalette input
            input_socket = group_input.outputs[input_name]
            chosen_socket = chosen_node.inputs[input_name]
            
            # Remove any existing links to the chosen_socket
            for link in garment_group.links:
                if link.to_socket == chosen_socket:
                    garment_group.links.remove(link)
            
            # Create new link
            garment_group.links.new(input_socket, chosen_socket)

def add_and_connect_dye_nodes(material, slot_type, primary_values, secondary_values):
    """Add dye node groups to material and connect to SWTOR Garment Shader"""
    if not material or not material.node_tree:
        return
    
    # Find the SWTOR shader node
    swtor_node = None
    for node in material.node_tree.nodes:
        if node.name == "SWTOR":
            swtor_node = node
            break
            
    if not swtor_node:
        print("SWTOR shader node not found (face)")
        return
        
    # Create primary dye node group
    primary_group = create_dye_node_group(material, slot_type, primary_values, True)
    secondary_group = create_dye_node_group(material, slot_type, secondary_values, False)
    
    # Add node group instances to material
    primary_node = material.node_tree.nodes.new('ShaderNodeGroup')
    primary_node.node_tree = primary_group
    primary_node.location = (swtor_node.location.x - 200, swtor_node.location.y - 650)
    
    secondary_node = material.node_tree.nodes.new('ShaderNodeGroup')
    secondary_node.node_tree = secondary_group
    secondary_node.location = (swtor_node.location.x - 200, swtor_node.location.y - 850)
    
    # Create connections
    links = material.node_tree.links
    
    # Connect primary node outputs
    primary_output_names = [
        "Palette1 Hue", "Palette1 Saturation", "Palette1 Brightness", "Palette1 Contrast",
        "Palette1 Specular", "Palette1 Metallic Specular"
    ]
    
    for output_name in primary_output_names:
        if output_name in primary_node.outputs and output_name in swtor_node.inputs:
            links.new(primary_node.outputs[output_name], swtor_node.inputs[output_name])
    
    # Connect secondary node outputs
    secondary_output_names = [
        "Palette2 Hue", "Palette2 Saturation", "Palette2 Brightness", "Palette2 Contrast",
        "Palette2 Specular", "Palette2 Metallic Specular"
    ]
    
    for output_name in secondary_output_names:
        if output_name in secondary_node.outputs and output_name in swtor_node.inputs:
            links.new(secondary_node.outputs[output_name], swtor_node.inputs[output_name])

def create_dye_nodes(material, slot_type, primary_values, secondary_values):
    """Create dye node groups in material without connections"""
    if not material or not material.node_tree:
        return None, None
    
    primary_node = None
    secondary_node = None
    
    # Create primary dye node group if we have values
    if primary_values:
        primary_group = create_dye_node_group(material, slot_type, primary_values, True)
        primary_node = material.node_tree.nodes.new('ShaderNodeGroup')
        primary_node.node_tree = primary_group
        primary_node.location = (-600, -650)
    
    # Create secondary dye node group if we have values
    if secondary_values:
        secondary_group = create_dye_node_group(material, slot_type, secondary_values, False)
        secondary_node = material.node_tree.nodes.new('ShaderNodeGroup')
        secondary_node.node_tree = secondary_group
        secondary_node.location = (-600, -850)
    
    return primary_node, secondary_node

def process_dye_settings(material, import_dir, slot_type, primary_file, secondary_file):
    """Process dye settings for a material"""
    # Parse primary dye file
    primary_values = None
    if primary_file:
        primary_values = parse_garment_hue_xml(import_dir, primary_file, True)
    
    # Parse secondary dye file
    secondary_values = None
    if secondary_file:
        secondary_values = parse_garment_hue_xml(import_dir, secondary_file, False)
    
    # Add and connect nodes if we have values
    if primary_values or secondary_values:
        add_and_connect_dye_nodes(material, slot_type, primary_values, secondary_values)

def get_gender_from_bodytype(body_type):
    """Extract gender (m/f) from body type string"""
    if len(body_type) >= 2:
        return body_type[1].lower()
    return 'm'  # default to male if invalid body type
    
def get_slot_mapping(slot_type):
    """Get the correct mapping for both filesystem paths and material names"""
    slot_map = {
        "face": "face",
        "chest": "chest",
        "hand": "hand",
        "wrist": "bracer",  # Maps wrist to bracer for file paths
        "waist": "waist",
        "leg": "leg",
        "feet": "boot"      # Maps feet to boot for file paths
    }
    return slot_map.get(slot_type, slot_type)

def get_skin_default_name(slot_type):
    """Get the skin default material name for a given slot type"""
    mapped_slot = get_slot_mapping(slot_type)
    return f"skinDefault_{mapped_slot.capitalize()}"

def process_model_file(import_dir, model_type, model_id, body_type, color_scheme=None):
    """Process the index.xml file for a given model type and ID"""
    if not model_id:
        return None
        
    # Get the correct path mapping for this model type
    mapped_model_type = get_slot_mapping(model_type)
        
    # Store dye files for later use
    primary_file = None
    secondary_file = None
        
    # Look up color scheme IDs if provided - use original model_type for color schemes
    if color_scheme:
        primary_id, secondary_id = get_color_scheme_ids(
            import_dir,
            color_scheme,
            model_type  # Use original model_type for color scheme lookups
        )
        
        if primary_id and secondary_id:
            # Get the garment hue files
            primary_file, secondary_file = get_garment_hue_files(import_dir, primary_id, secondary_id, model_type)
        
    # Construct path to index.xml using the correct directory structure and mapped type
    xml_path = os.path.join(import_dir, "art\\dynamic", mapped_model_type, "index.xml")
    
    if not os.path.exists(xml_path):
        print(f"Error: Could not find index.xml at {xml_path}")
        return None
        
    try:
        # Parse XML file
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # Search for matching asset
        for asset in root.findall('Asset'):
            asset_id = asset.find('ID')
            if asset_id is not None and asset_id.text == model_id:
                # Store the currently selected objects before import
                previously_selected = bpy.context.selected_objects[:]
                active_object = bpy.context.active_object
                
                imported_objects = []  # Track all imported objects
                processed_materials = set()  # Track which materials have been processed for color nodes
                
                # Process base file
                base_file = asset.find('BaseFile')
                if base_file is not None:
                    # Get the filename and replace [bt] with body_type
                    filename = os.path.basename(base_file.text)
                    filename = filename.replace('[bt]', body_type)
                    print(f"{mapped_model_type} Base GR2 file: {filename}")
                    
                    # Construct full path to the GR2 file using mapped type
                    gr2_path = os.path.join(import_dir, "art", "dynamic", mapped_model_type, "model", filename)
                    
                    try:
                        # Import the base mesh
                        bpy.ops.import_mesh.gr2('EXEC_DEFAULT', filepath=gr2_path)
                        print(f"Successfully imported base file: {gr2_path}")
                        
                        # Find the newly imported object
                        for obj in bpy.context.selected_objects:
                            if obj not in previously_selected:
                                imported_objects.append(obj)
                                
                    except Exception as e:
                        print(f"Error importing base GR2 file: {str(e)}")
                
                # Process attachments if they exist
                attachments = asset.find('Attachments')
                if attachments is not None:
                    for attachment in attachments.findall('Attachment'):
                        filename = attachment.get('filename')
                        if filename:
                            # Get the filename and replace [bt] with body_type
                            filename = os.path.basename(filename)
                            filename = filename.replace('[bt]', body_type)
                            print(f"{mapped_model_type} Attachment GR2 file: {filename}")
                            
                            # Construct full path to the attachment GR2 file using mapped type
                            gr2_path = os.path.join(import_dir, "art", "dynamic", mapped_model_type, "model", filename)
                            
                            try:
                                # Import the attachment mesh
                                bpy.ops.import_mesh.gr2('EXEC_DEFAULT', filepath=gr2_path)
                                print(f"Successfully imported attachment: {gr2_path}")
                                
                                # Find the newly imported attachment object
                                for obj in bpy.context.selected_objects:
                                    if obj not in previously_selected and obj not in imported_objects:
                                        imported_objects.append(obj)
                                        
                            except Exception as e:
                                print(f"Error importing attachment GR2 file: {str(e)}")
                
                # Process materials for all imported objects
                materials = asset.find('Materials')
                if materials is not None:
                    gender = get_gender_from_bodytype(body_type)
                    
                    # Get the first material entry
                    first_material = materials.find('Material')  # This gets only the first Material element
                    
                    if first_material is not None:
                        filename = first_material.get('filename')
                        
                        if filename:
                            # Use the filename (without path and .mat) as the material name for all parts
                            material_name = os.path.splitext(os.path.basename(filename))[0]
                            
                            # Handle gender replacement if needed
                            if '[gen]' in filename:
                                material_name = material_name.replace('_[gen]', f'_{gender}')
                            print(f"Material name from filename: {material_name}")
                            
                            # Process each imported object
                            for obj in imported_objects:
                                if obj.data.materials:
                                    # For objects with multiple material slots
                                    if len(obj.data.materials) > 1:
                                        # Handle first material slot
                                        if obj.data.materials[0]:
                                            # Check if material already exists in Blender
                                            existing_material = bpy.data.materials.get(material_name)
                                            if existing_material:
                                                # Use existing material instead of creating duplicate
                                                print(f"Using existing material: {material_name}")
                                                obj.data.materials[0] = existing_material
                                            else:
                                                # Set name of current material
                                                obj.data.materials[0].name = material_name
                                                print(f"Set first material slot to: {material_name}")
                                        
                                        # Handle second material slot (skinDefault)
                                        if obj.data.materials[1]:
                                            skin_default_name = get_skin_default_name(model_type)
                                            # Check if skinDefault material already exists
                                            existing_skin = bpy.data.materials.get(skin_default_name)
                                            if existing_skin:
                                                obj.data.materials[1] = existing_skin
                                            else:
                                                obj.data.materials[1].name = skin_default_name
                                            print(f"Set second material slot to: {skin_default_name}")
                                    else:
                                        # Single material slot
                                        for mat_slot in obj.data.materials:
                                            if mat_slot:
                                                # Check if material already exists
                                                existing_material = bpy.data.materials.get(material_name)
                                                if existing_material:
                                                    # Use existing material
                                                    mat_index = obj.data.materials.find(mat_slot.name)
                                                    obj.data.materials[mat_index] = existing_material
                                                else:
                                                    # Set name of current material
                                                    mat_slot.name = material_name
                                                print(f"Set material name to: {material_name}")
                
                # Process materials using ZG SWTOR Tools for all imported objects individually
                try:
                    if imported_objects:
                        # Process each object separately
                        for obj in imported_objects:
                            # Check if object has any materials that haven't been processed
                            has_unprocessed_materials = False
                            if obj.data.materials:
                                for mat in obj.data.materials:
                                    if mat and mat.name not in processed_materials:
                                        has_unprocessed_materials = True
                                        break
                            
                            if has_unprocessed_materials:
                                # Deselect all objects
                                bpy.ops.object.select_all(action='DESELECT')
                                
                                # Select only this object and make it active
                                obj.select_set(True)
                                bpy.context.view_layer.objects.active = obj
                                
                                # Run the material processing operator for this object
                                bpy.ops.zgswtor.process_named_mats(use_selection_only=True)
                                print(f"Successfully processed materials for object: {obj.name}")
                            
                            # Process materials on this object
                            if obj.data.materials:
                                for mat in obj.data.materials:
                                    if mat and not mat.name.startswith('skinDefault'):
                                        # Setup custom shader inputs for all materials
                                        setup_custom_shader_inputs(mat)
                                        
                                        # Only add color nodes if we haven't processed this material yet
                                        if mat.name not in processed_materials and primary_file and secondary_file:
                                            process_dye_settings(
                                                mat,
                                                import_dir,
                                                model_type,
                                                primary_file,
                                                secondary_file
                                            )
                                            processed_materials.add(mat.name)
                    
                except Exception as e:
                    print(f"Error processing materials: {str(e)}")
                
                # Restore previous selection state
                bpy.ops.object.select_all(action='DESELECT')
                for obj in previously_selected:
                    obj.select_set(True)
                if active_object:
                    bpy.context.view_layer.objects.active = active_object
                
                return True
                    
        print(f"No matching asset found for {mapped_model_type} ID: {model_id}")
        return None
        
    except ET.ParseError as e:
        print(f"Error parsing XML file {xml_path}: {str(e)}")
        return None
    except Exception as e:
        print(f"Unexpected error processing {xml_path}: {str(e)}")
        return None

# Operator

class JCSWTOR_OT_save_textures(Operator):
    bl_idname = "jcswtor.save_textures"
    bl_label = "Save Texture Files to Folder"
    bl_description = "Save all texture files to the specified directory and update paths"
    
    def process_node_tree(self, node_tree, processed_files, output_dir):
        """Recursively process nodes in a node tree"""
        if not node_tree:
            return
            
        for node in node_tree.nodes:
            # Process texture nodes
            if node.type == 'TEX_IMAGE' and node.image:
                image = node.image
                print(f"Found texture image node: {image.name}")
                
                # Skip if already processed or no filepath
                if not image.filepath:
                    print(f"- Skipping {image.name}: No filepath")
                    continue
                if image.filepath in processed_files:
                    print(f"- Skipping {image.name}: Already processed")
                    continue
                    
                # Get the original filepath and filename
                orig_path = bpy.path.abspath(image.filepath)
                if not os.path.exists(orig_path):
                    print(f"Warning: Could not find texture file: {orig_path}")
                    continue
                    
                filename = os.path.basename(orig_path)
                new_path = os.path.join(output_dir, filename)
                
                try:
                    # Copy the file
                    shutil.copy2(orig_path, new_path)
                    
                    # Update the image filepath
                    image.filepath = new_path
                    
                    # Mark as processed
                    processed_files.add(orig_path)
                    print(f"Processed texture: {filename}")
                    
                except Exception as e:
                    print(f"Error processing {filename}: {str(e)}")
            
            # Recursively process node groups
            if node.type == 'GROUP' and node.node_tree:
                self.process_node_tree(node.node_tree, processed_files, output_dir)
                
            # Process custom SWTOR shader nodes (they might have a different type)
            if hasattr(node, 'node_tree') and node.node_tree:
                self.process_node_tree(node.node_tree, processed_files, output_dir)
    
    def execute(self, context):
        output_dir = context.scene.texture_save_props.output_directory
        print(f"\nStarting texture save process...")
        print(f"Output directory: {output_dir}")
        
        if not output_dir:
            self.report({'ERROR'}, "Please select an output directory first")
            return {'CANCELLED'}
            
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except Exception as e:
                self.report({'ERROR'}, f"Could not create directory: {str(e)}")
                return {'CANCELLED'}
        
        # Track processed files to avoid duplicates
        processed_files = set()
        
        # Process all materials in the file
        for material in bpy.data.materials:
            if material.node_tree:
                print(f"Processing material: {material.name}")
                self.process_node_tree(material.node_tree, processed_files, output_dir)
                
                # Also process all node groups used in the material
                for node_group in bpy.data.node_groups:
                    print(f"Processing node group: {node_group.name}")
                    self.process_node_tree(node_group, processed_files, output_dir)
        
        # Also check for any packed images
        for image in bpy.data.images:
            if image.packed_file:
                filename = image.name
                if not filename.endswith(('.png', '.tga', '.dds')):
                    filename += '.png'  # Add default extension if none exists
                
                new_path = os.path.join(output_dir, filename)
                
                try:
                    # Save packed image to file
                    image.save_render(new_path)
                    image.filepath = new_path
                    image.packed_file = None  # Unpack the image
                    
                    # Mark as processed
                    processed_files.add(new_path)
                    print(f"Processed packed image: {filename}")
                    
                except Exception as e:
                    print(f"Error processing packed image {filename}: {str(e)}")
        
        self.report({'INFO'}, f"Saved {len(processed_files)} texture files to {output_dir}")
        return {'FINISHED'}

class JCSWTOR_PT_texture_save(Panel):
    bl_label = "Save Texture Files"
    bl_idname = "JCSWTOR_PT_texture_save"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "JC SWTOR Tools"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.texture_save_props
        
        box = layout.box()
        box.prop(props, "output_directory")
        box.operator("jcswtor.save_textures")

class JCSWTOR_OT_import_armor(Operator):
    bl_idname = "jcswtor.import_armor"
    bl_label = "Import Armor"
    bl_description = "Import SWTOR armor pieces"
    
    def execute(self, context):
        preferences = context.preferences.addons[__name__].preferences
        import_dir = preferences.import_directory
        props = context.scene.armor_import_props
        
        # Process each model type with its corresponding color scheme
        if props.face_model_id:
            face_model = process_model_file(
                import_dir,
                "face",
                props.face_model_id,
                props.body_type,
                props.face_color_scheme
            )
            
        if props.chest_model_id:
            chest_model = process_model_file(
                import_dir,
                "chest",
                props.chest_model_id,
                props.body_type,
                props.chest_color_scheme
            )
            
        if props.hand_model_id:
            hand_model = process_model_file(
                import_dir,
                "hand",
                props.hand_model_id,
                props.body_type,
                props.hand_color_scheme
            )
            
        if props.wrist_model_id:
            wrist_model = process_model_file(
                import_dir,
                "wrist",
                props.wrist_model_id,
                props.body_type,
                props.wrist_color_scheme
            )
            
        if props.waist_model_id:
            waist_model = process_model_file(
                import_dir,
                "waist",
                props.waist_model_id,
                props.body_type,
                props.waist_color_scheme
            )
            
        if props.leg_model_id:
            leg_model = process_model_file(
                import_dir,
                "leg",
                props.leg_model_id,
                props.body_type,
                props.leg_color_scheme
            )
            
        if props.feet_model_id:
            feet_model = process_model_file(
                import_dir,
                "feet",
                props.feet_model_id,
                props.body_type,
                props.feet_color_scheme
            )
            
        return {'FINISHED'}

# Panel
class JCSWTOR_PT_armor_import(Panel):
    bl_label = "Armor Import"    # This is the section title that appears at the top of the panel
    bl_idname = "JCSWTOR_PT_armor_import"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "JC SWTOR Tools"    # This is the tab name in the N-panel
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.armor_import_props
        
        box = layout.box()
        box.label(text="Import Armor")
        
        # Add all property fields
        box.prop(props, "body_type")
        box.prop(props, "face_model_id")
        box.prop(props, "face_color_scheme")
        box.prop(props, "chest_model_id")
        box.prop(props, "chest_color_scheme")
        box.prop(props, "hand_model_id")
        box.prop(props, "hand_color_scheme")
        box.prop(props, "wrist_model_id")
        box.prop(props, "wrist_color_scheme")
        box.prop(props, "waist_model_id")
        box.prop(props, "waist_color_scheme")
        box.prop(props, "leg_model_id")
        box.prop(props, "leg_color_scheme")
        box.prop(props, "feet_model_id")
        box.prop(props, "feet_color_scheme")
        
        # Add import button
        box.operator("jcswtor.import_armor")

class JCSWTOR_PT_dye_import(Panel):
    bl_label = "Dye Import"
    bl_idname = "JCSWTOR_PT_dye_import"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "JC SWTOR Tools"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.dye_import_props
        
        box = layout.box()
        # Add search field
        box.prop(props, "dye_search", text="Search Dye")
        # Add filtered dropdown
        box.prop(props, "filtered_dye", text="Dye Colors")
        box.prop(props, "slot_type")
        box.operator("jcswtor.apply_dye")

class JCSWTOR_PT_node_groups(Panel):
    bl_label = "Node Groups to SWTOR Garment Shader"
    bl_idname = "JCSWTOR_PT_node_groups"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "JC SWTOR Tools"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.operator("jcswtor.add_shader_nodes")

# Registration
classes = (
    JCSWTORArmorImportPreferences,
    ArmorImportProperties,
    TextureSaveProperties,
    DyeImportProperties,
    JCSWTOR_OT_import_armor,
    JCSWTOR_OT_save_textures,
    JCSWTOR_PT_armor_import,
    JCSWTOR_PT_texture_save,
    JCSWTOR_PT_dye_import,
    JCSWTOR_OT_apply_dye,
    JCSWTOR_OT_add_shader_nodes,
    JCSWTOR_PT_node_groups,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.armor_import_props = PointerProperty(type=ArmorImportProperties)
    bpy.types.Scene.texture_save_props = PointerProperty(type=TextureSaveProperties)
    bpy.types.Scene.dye_import_props = PointerProperty(type=DyeImportProperties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.armor_import_props
    del bpy.types.Scene.texture_save_props
    del bpy.types.Scene.dye_import_props

if __name__ == "__main__":
    register()