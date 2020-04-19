import bpy
from math import radians


### Provide your own information here:

# Provide the path to your numbers here
numbers_filepath = "/home/your/file/path/here"
numbers_file = bpy.path.abspath(numbers_filepath)

objs = bpy.data.objects
numbers_required = ["1", "2", "3", "4", "5", "6", "underscore"]
faces = [
    {"number": "6", "x": 0, "y": 90, "z": -90},
    {"number": "2", "x": 0, "y": 90, "z": -90},
    {"number": "4", "x": 180, "y": 0, "z": 0},
    {"number": "3", "x": 0, "y": -90, "z": 90},
    {"number": "1", "x": 0, "y": -90, "z": 90},
    {"number": "5", "x": 0, "y": 90, "z":  -90}
]


### Helper Functions

def select_object(obj):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = obj

def apply_bool_mod(main_object, secondary_object):
    # Create a boolean modifier named 'bool_mod' for the main_object.
    mod_bool = main_object.modifiers.new('bool_mod', 'BOOLEAN')
    # Set the mode of the modifier to DIFFERENCE.
    mod_bool.operation = 'DIFFERENCE'
    # Set the number to be used by the modifier.
    mod_bool.object = secondary_object

    # The modifier_apply function only works on the active object.
    # Set the main_object as the active object.
    select_object(main_object)

    # Apply the modifier.
    res = bpy.ops.object.modifier_apply(modifier='bool_mod')


def wipe_slate():
    col = bpy.data.collections.get("Master Collection")
    if col:
       for obj in col.objects:
           obj.select_set(True)
    bpy.ops.object.delete()

### Main Script:

# Create a simple cube.
bpy.ops.mesh.primitive_cube_add()

# Resize the cube to 16mx16mx16m
bpy.ops.transform.resize(value=(8, 8, 8))

# Get the cube object and rename it.
cube = bpy.context.object
cube.name = 'cube'

# append all objects from the numbers file that are in the "numbers_required" list
with bpy.data.libraries.load(numbers_file) as (data_from, data_to):
    data_to.objects = [name for name in data_from.objects if name in numbers_required]


# link them to scene
scene = bpy.context.scene
for obj in data_to.objects:
    if obj is not None:
        scene.collection.objects.link(obj)

for face in faces:
    # Select the face
    num_obj = bpy.data.objects[face['number']]
    select_object(num_obj)

    # Move and resize the face
    num_obj.location = (0, 0, 8.6)
    num_obj.scale = (625, 625, 1)

    # Apply the Difference Bool mod to the cube & number
    apply_bool_mod(cube, num_obj)

    if face['number'] in ['6', '9']:
        underscore = bpy.data.objects['underscore']
        select_object(underscore)

        # Move and resize the face
        underscore.location = (0, 0, 8.6)
        underscore.scale = (625, 625, 1)
        # Apply the Difference Bool mod to the cube & underscore
        apply_bool_mod(cube, underscore)

    # Rotate the cube.
    bpy.ops.object.select_all(action='DESELECT')
    cube.select_set(True)
    bpy.ops.transform.rotate(value=radians(face['x']), orient_axis='X')
    bpy.ops.transform.rotate(value=radians(face['y']), orient_axis='Y')
    bpy.ops.transform.rotate(value=radians(face['z']), orient_axis='Z')

    # Delete the number
    objs.remove(objs[face['number']], do_unlink=True)

# Delete underscore at the very end
objs.remove(objs['underscore'], do_unlink=True)
