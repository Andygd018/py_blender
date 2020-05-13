from pathlib import Path
from os import listdir
from os.path import isfile, join

import bpy
import addon_utils
from math import radians


if addon_utils.check("add_mesh_extra_objects") != (True, True):
    addon_utils.enable("add_mesh_extra_objects")

##########################################
# Provide your own information here:
##########################################

# Provide the path to your numbers here:
# IMPORTANT: the number objects are expected to be named simply the number they are:
#   For instance: 1, 2, 3 or underscore
#   The default assumes that if you want to use an underscore, you've already
#    combined it the numbers file.
#   If you have not, you can simply remove the `#` at the beginning of the
#    "underscore" lines in the rotations object below.
numbers_filepath = Path("/path/to/your/numbers.blend")

# If you want to save the files, provide the output path to a folder here:
#   This folder must already exist, and it will not replace any current files
output_folderpath = Path("/path/to/folder/saved_dice")

# Set to True and it will output a .blend file and .stl file
#   for each dice object separately, for ease of importing to slicing software
# Set to False and it will display them all in blender to be viewed
save_files = False

tweaks_for_font = {
    # "num_version": "1",
    "num_scale":
        {
            "d6": (None, None, None),
            "d4": (None, None, None),
            "d8": (None, None, None),
            "d10-single": (None, None, None),
            "d10-double-vertical": (None, None, None),
            "d12": (None, None, None),
            "d20": (None, None, None)
        }
}


##########################################
# !!!!!!!!!!!!
# WARNING NOTE IF YOU WANT TO EDIT:
#       certain factors of using this script appear to be
#       different to using the normal interface, most notably:
#       - Angles appear to be "inversed",
#           i.e. 90 degrees on the X axis in the interface, is -90 here
#       - Scales appear to be halved, i.e. scaling up by 1000 is 500 here
# !!!!!!!!!!!!
##########################################
# Dice info here for transforming the numbers onto the respective dice:
####################
#   - "name": STRING
#       The name of the dice, which will translate to name of the file for each dice.
#        so long as the name starts with one of the following
#        d4, d6, d8, d10-single, d10-double, d12, d20
#   - "num_location": (X-cordinate, Y-cordinate, Z-cordinate)
#       Where the number is placed from the origin when it's going to be BOOLEAN-ed against the dice.
#        CHANGE THIS if the numbers are the correct size on the face, but too close to the edge.
#   - "num_scale": (X-scale, Y-scale, Z-scale)
#       The scale factor to apply to each axis of the number.
#        CHANGE THIS if the numbers on your face are too large or too small,
#        DO NOT CHANGE THE Z-scale from 1, that is done in another variable below
#   - "final_location": (X-cordinate, Y-cordinate, Z-cordinate)
#       Where the dice are place once finished to display them more easily
#   - "number_height": NUMBER [OPTIONAL]
#       If the Z height isn't large enough, and you want deeper numbers,
#        you can change this to larger than the default of 2
#   - "rotations": List[Dictionary{}]
#       A list of operations to apply to the dice to rotate it and apply the
#        numbers to it's faces.
#
##########################################


dice_list = [
    {
        "name": "d6",  # "Follow-the-number" config, each number's orientation
        "num_location": (0, 0, 8.6),
        "num_scale": (625, 625, 1),
        "final_location": (40, 30, 0),
        "number_height": 4,
        "rotations":
        [
            # {"number": "underscore", "x": 0, "y": 0, "z": 0},
            {"number": "1", "x": 0, "y": 0, "z": -90},
            {"number": "", "x": 180, "y": 90, "z": 0},
            {"number": "2", "x": 0, "y": 0, "z": -90},
            {"number": "", "x": 180, "y": 90, "z": 0},
            {"number": "3", "x": 0, "y": 180, "z": 0},
            {"number": "", "x": 0, "y": 0, "z": 90},
            {"number": "4", "x": 90, "y": 0, "z": 0},
            {"number": "", "x": 0, "y": 0, "z": 90},
            {"number": "5", "x": 90, "y": 0, "z": 0},
            {"number": "", "x": 0, "y": 0, "z": 90},
            {"number": "6", "x": 0, "y": 0, "z": 0}
        ]
    },
    # {
    #     "name": "d6", # Format: Mid section all have same orientation, with 1&6 either end
    #     "num_location": (0, 0, 8.6),
    #     "num_scale": (625, 625, 1),
    #     "final_location": (40, 30, 0),
    #     "rotations":
    #     [
    #         # {"number": "underscore", "x": 0, "y": 0, "z": 0},
    #         {"number": "6", "x": 180, "y": 0, "z": 0},
    #         {"number": "1", "x": 90, "y": 0, "z": 0},
    #         {"number": "2", "x": 0, "y": 180, "z": 0},
    #         {"number": "5", "x": 0, "y": -90, "z": 0},
    #         {"number": "4", "x": 0, "y": 180, "z": 0},
    #         {"number": "3", "x": 90, "y": 0, "z": -90}
    #     ],
    # },
    # {
    #     "name": "d6", # cly-faker standard
    #     "rotations":
    #     [
    #         # {"number": "underscore", "x": 0, "y": 0, "z": 0},
    #         {"number": "6", "x": 0, "y": 0, "z": -90},
    #         {"number": "", "x": 0, "y": 90, "z": 0},
    #         {"number": "2", "x": 0, "y": 0, "z": -90},
    #         {"number": "", "x": 0, "y": 90, "z": 0},
    #         {"number": "4", "x": 180, "y": 0, "z": 0},
    #         {"number": "3", "x": 0, "y": 0, "z": 90},
    #         {"number": "", "x": 0, "y": -90, "z": 0},
    #         {"number": "1", "x": 0, "y": 0, "z": 90},
    #         {"number": "", "x": 0, "y": -90, "z": 0},
    #         {"number": "5", "x": 0, "y": 0, "z": -90},
    #         {"number": "", "x": 0, "y": 90, "z": 0}
    #     ],
    #     "num_location": (0, 0, 8.6),
    #     "num_scale": (625, 625, 1),
    #     "final_location": (40, 30, 0)
    # },
    {
        "name": "d4",
        "rotations": [
            {"number": "4", "x": 19.47, "y": -120, "z": 0},
            {"number": "", "x": -19.47, "y": 0, "z": 0},
            {"number": "4", "x": 19.47, "y": -120, "z": 0},
            {"number": "", "x": -19.47, "y": 0, "z": 0},
            {"number": "4", "x": 0, "y": 0, "z": -120},
            {"number": "3", "x": 19.47, "y": -120, "z": 0},
            {"number": "", "x": -19.47, "y": 0, "z": 0},
            {"number": "3", "x": 19.47, "y": -120, "z": 0},
            {"number": "", "x": -19.47, "y": 0, "z": 0},
            {"number": "3", "x": 0, "y": 0, "z": 120},
            {"number": "2", "x": 19.47, "y": -120, "z": 0},
            {"number": "", "x": -19.47, "y": 0, "z": 0},
            {"number": "2", "x": 19.47, "y": -120, "z": 0},
            {"number": "", "x": -19.47, "y": 0, "z": 0},
            {"number": "2", "x": 19.47, "y": -120, "z": 0},
            {"number": "", "x": -19.47, "y": 0, "z": 120},
            {"number": "1", "x": 19.47, "y": -120, "z": 0},
            {"number": "", "x": -19.47, "y": 0, "z": 0},
            {"number": "1", "x": 19.47, "y": -120, "z": 0},
            {"number": "", "x": -19.47, "y": 0, "z": 0},
            {"number": "1", "x": 19.47, "y": -120, "z": 0},
            {"number": "", "x": -19.47, "y": 0, "z": 0}
        ],
        "num_location": (0, 6, 5.6),
        "num_scale": (400, 400, 1),
        "final_location": (0, 60, 0),
        "number_height": 4
    },
    {
        "name": "d8",
        "rotations": [
            {"number": "8", "x": 35.265, "y": 90, "z": 0},
            {"number": "", "x": -35.265, "y": 0, "z": 0},
            {"number": "2", "x": 35.265, "y": 90, "z": 0},
            {"number": "", "x": -35.265, "y": 0, "z": 0},

            # {"number": "underscore", "x": 0, "y": 0, "z": 0},
            {"number": "6", "x": 35.265, "y": 90, "z": 0},
            {"number": "", "x": -35.265, "y": 0, "z": 0},

            {"number": "4", "x": 180, "y": 0, "z": 0},

            {"number": "5", "x": 35.265, "y": 90, "z": 0},
            {"number": "", "x": -35.265, "y": 0, "z": 0},

            {"number": "3", "x": 35.265, "y": 90, "z": 0},
            {"number": "", "x": -35.265, "y": 0, "z": 0},

            {"number": "7", "x": 35.265, "y": 90, "z": 0},
            {"number": "", "x": -35.265, "y": 0, "z": 0},

            {"number": "1", "x": 35.265, "y": 90, "z": 0},
            {"number": "", "x": -35.265, "y": 0, "z": 0}
        ],
        "num_location": (0, 0, 8.6),
        "num_scale": (500, 500, 1),
        "final_location": (40, -30, 0),
        "number_height": 4
    },
    {
        "name": "d10-single",
        "rotations": [
            # {"number": "underscore", "x": 0, "y": 0, "z": 0},
            {"number": "6", "x": 35.7, "y": 72, "z": 0},
            {"number": "", "x": -35.7, "y": 0, "z": 0},

            {"number": "4", "x": 35.7, "y": 72, "z": 0},
            {"number": "", "x": -35.7, "y": 0, "z": 0},

            {"number": "8", "x": 35.7, "y": 72, "z": 0},
            {"number": "", "x": -35.7, "y": 0, "z": 0},

            {"number": "2", "x": 35.7, "y": 72, "z": 0},
            {"number": "", "x": -35.7, "y": 0, "z": 0},

            {"number": "0", "x": -180, "y": 0, "z": 0},

            {"number": "1", "x": 35.7, "y": 72, "z": 0},
            {"number": "", "x": -35.7, "y": 0, "z": 0},

            # {"number": "underscore", "x": 0, "y": 0, "z": 0},
            {"number": "9", "x": 35.7, "y": 72, "z": 0},
            {"number": "", "x": -35.7, "y": 0, "z": 0},

            {"number": "3", "x": 35.7, "y": 72, "z": 0},
            {"number": "", "x": -35.7, "y": 0, "z": 0},

            {"number": "7", "x": 35.7, "y": 72, "z": 0},
            {"number": "", "x": -35.7, "y": 0, "z": 0},

            {"number": "5", "x": 35.7, "y": 72, "z": 0},
            {"number": "", "x": -35.7, "y": 0, "z": 0}
        ],
        "num_location": (0, -0.75, 9),
        "num_scale": (500, 500, 1),
        "final_location": (0, -60, 0),
        "number_height": 4
    },
    {
        "name": "d10-double-vertical",  # Numbers face the opposing end of the dice
        "rotations": [
            {"number": "60", "x": 35.7, "y": 72, "z": 0},
            {"number": "", "x": -35.7, "y": 0, "z": 0},

            {"number": "40", "x": 35.7, "y": 72, "z": 0},
            {"number": "", "x": -35.7, "y": 0, "z": 0},

            {"number": "80", "x": 35.7, "y": 72, "z": 0},
            {"number": "", "x": -35.7, "y": 0, "z": 0},

            {"number": "20", "x": 35.7, "y": 72, "z": 0},
            {"number": "", "x": -35.7, "y": 0, "z": 0},

            {"number": "00", "x": -180, "y": 0, "z": 0},

            {"number": "10", "x": 35.7, "y": 72, "z": 0},
            {"number": "", "x": -35.7, "y": 0, "z": 0},

            # {"number": "underscore", "x": 0, "y": 0, "z": 0},
            {"number": "90", "x": 35.7, "y": 72, "z": 0},
            {"number": "", "x": -35.7, "y": 0, "z": 0},

            {"number": "30", "x": 35.7, "y": 72, "z": 0},
            {"number": "", "x": -35.7, "y": 0, "z": 0},

            {"number": "70", "x": 35.7, "y": 72, "z": 0},
            {"number": "", "x": -35.7, "y": 0, "z": 0},

            {"number": "50", "x": 35.7, "y": 72, "z": 0},
            {"number": "", "x": -35.7, "y": 0, "z": 0}
        ],
        "num_location": (0, -1.5, 9),  # (0, -2.5, 9),
        "num_scale": (375, 375, 1),
        "final_location": (-40, -30, 0),
        "number_height": 4
    },
    # {
    #     "name": "d10-double-horizontal", # Numbers face the next face around on the same side
    #     "rotations": [
    #         {"number": "", "x": 0, "y": 0, "z": 90},
    #         {"number": "60", "x": 0, "y": 0, "z": -90},
    #         {"number": "", "x": 35.7, "y": 72, "z": 0},
    #         {"number": "", "x": -35.7, "y": 0, "z": 0},

    #         {"number": "", "x": 0, "y": 0, "z": 90},
    #         {"number": "40", "x": 0, "y": 0, "z": -90},
    #         {"number": "", "x": 35.7, "y": 72, "z": 0},
    #         {"number": "", "x": -35.7, "y": 0, "z": 0},

    #         {"number": "", "x": 0, "y": 0, "z": 90},
    #         {"number": "80", "x": 0, "y": 0, "z": -90},
    #         {"number": "", "x": 35.7, "y": 72, "z": 0},
    #         {"number": "", "x": -35.7, "y": 0, "z": 0},

    #         {"number": "", "x": 0, "y": 0, "z": 90},
    #         {"number": "20", "x": 0, "y": 0, "z": -90},
    #         {"number": "", "x": 35.7, "y": 72, "z": 0},
    #         {"number": "", "x": -35.7, "y": 0, "z": 0},

    #         {"number": "", "x": 0, "y": 0, "z": 90},
    #         {"number": "00", "x": 00, "y":0, "z": -90},
    #         {"number": "", "x": -180, "y": 0, "z": 0},

    #         {"number": "", "x": 0, "y": 0, "z": 90},
    #         {"number": "10", "x": 0, "y": 0, "z": -90},
    #         {"number": "", "x": 35.7, "y": 72, "z": 0},
    #         {"number": "", "x": -35.7, "y": 0, "z": 0},

    #         # {"number": "underscore", "x": 0, "y": 0, "z": 0},
    #         {"number": "", "x": 0, "y": 0, "z": 90},
    #         {"number": "90", "x": 0, "y": 0, "z": -90},
    #         {"number": "", "x": 35.7, "y": 72, "z": 0},
    #         {"number": "", "x": -35.7, "y": 0, "z": 0},

    #         {"number": "", "x": 0, "y": 0, "z": 90},
    #         {"number": "30", "x": 0, "y": 0, "z": -90},
    #         {"number": "", "x": 35.7, "y": 72, "z": 0},
    #         {"number": "", "x": -35.7, "y": 0, "z": 0},

    #         {"number": "", "x": 0, "y": 0, "z": 90},
    #         {"number": "70", "x": 0, "y": 0, "z": -90},
    #         {"number": "", "x": 35.7, "y": 72, "z": 0},
    #         {"number": "", "x": -35.7, "y": 0, "z": 0},

    #         {"number": "", "x": 0, "y": 0, "z": 90},
    #         {"number": "50", "x": 0, "y": 0, "z": -90},
    #         {"number": "", "x": 35.7, "y": 72, "z": 0},
    #         {"number": "", "x": -35.7, "y": 0, "z": 0}
    #     ],
    #     "num_location": (-1, 0, 9), # (0, -2.5, 9),
    #     "num_scale": (375, 375, 1),
    #     "final_location": (-40, -30, 0)
    # },
    {
        "name": "d12",
        "rotations": [
            {"number": "12", "x": 0, "y": 0, "z": -36},
            {"number": "", "x": -63.43, "y": 0, "z": 0},
            {"number": "8", "x": 63.43, "y": 0, "z": -72},
            {"number": "", "x": -63.43, "y": 0, "z": 0},
            # {"number": "underscore", "x": 0, "y": 0, "z": -0},
            {"number": "6", "x": 63.43, "y": 0, "z": -72},
            {"number": "", "x": -63.43, "y": 0, "z": 0},
            {"number": "4", "x": 63.43, "y": 0, "z": -72},
            {"number": "", "x": -63.43, "y": 0, "z": 0},
            {"number": "2", "x": 63.43, "y": 0, "z": -72},
            {"number": "", "x": -63.43, "y": 0, "z": 0},
            {"number": "10", "x": 63.43, "y": 0, "z": -72},

            {"number": "", "x": -180, "y": 0, "z": -36},

            {"number": "1", "x": 0, "y": 0, "z": -36},
            {"number": "", "x": -63.43, "y": 0, "z": 0},
            {"number": "3", "x": 63.43, "y": 0, "z": -72},
            {"number": "", "x": -63.43, "y": 0, "z": 0},
            {"number": "11", "x": 63.43, "y": 0, "z": -72},
            {"number": "", "x": -63.43, "y": 0, "z": 0},
            # {"number": "underscore", "x": 0, "y": 0, "z": -0},
            {"number": "9", "x": 63.43, "y": 0, "z": -72},
            {"number": "", "x": -63.43, "y": 0, "z": 0},
            {"number": "7", "x": 63.43, "y": 0, "z": -72},
            {"number": "", "x": -63.43, "y": 0, "z": 0},
            {"number": "5", "x": 63.43, "y": 0, "z": -72},
        ],
        "num_location": (0, 0, 9.75),
        "num_scale": (500, 500, 1),
        "final_location": (-40, 30, 0),
        "number_height": 4
    },
    {
        "name": "d20",
        "rotations": [
            # Using 20 as a hub, apply 3 numbers then come back up to 20 and twist
            {"number": "20", "x": 0, "y": 0, "z": -60},

            {"number": "", "x": -41.81, "y": 0, "z": 0},
            {"number": "14", "x": 0, "y": 0, "z": -60},
            {"number": "", "x": -41.81, "y": 0, "z": 0},
            # {"number": "underscore", "x": 0, "y": 0, "z": -0},
            {"number": "6", "x": 41.81, "y": 0, "z": 0},
            {"number": "", "x": 0, "y": 0, "z": 120},
            {"number": "", "x": -41.81, "y": 0, "z": 0},
            {"number": "4", "x": 41.81, "y": 0, "z": 0},
            {"number": "", "x": 0, "y": 0, "z": -60},
            {"number": "", "x": 41.81, "y": 0, "z": 0},
            {"number": "", "x": 0, "y": 0, "z": -120},

            {"number": "", "x": -41.81, "y": 0, "z": 0},
            {"number": "8", "x": 0, "y": 0, "z": -60},
            {"number": "", "x": -41.81, "y": 0, "z": 0},
            # {"number": "underscore", "x": 0, "y": 0, "z": -0},
            {"number": "10", "x": 41.81, "y": 0, "z": 0},
            {"number": "", "x": 0, "y": 0, "z": 120},
            {"number": "", "x": -41.81, "y": 0, "z": 0},
            {"number": "16", "x": 41.81, "y": 0, "z": 0},
            {"number": "", "x": 0, "y": 0, "z": -60},
            {"number": "", "x": 41.81, "y": 0, "z": 0},
            {"number": "", "x": 0, "y": 0, "z": -120},

            {"number": "", "x": -41.81, "y": 0, "z": 0},
            {"number": "2", "x": 0, "y": 0, "z": -60},
            {"number": "", "x": -41.81, "y": 0, "z": 0},
            # {"number": "underscore", "x": 0, "y": 0, "z": -0},
            {"number": "18", "x": 41.81, "y": 0, "z": 0},
            {"number": "", "x": 0, "y": 0, "z": 120},
            {"number": "", "x": -41.81, "y": 0, "z": 0},
            {"number": "12", "x": 41.81, "y": 0, "z": 0},
            {"number": "", "x": 0, "y": 0, "z": -60},
            {"number": "", "x": 41.81, "y": 0, "z": 0},
            {"number": "", "x": 0, "y": 0, "z": -120},

            # Flip the Dice
            {"number": "", "x": 0, "y": 0, "z": 60},
            {"number": "", "x": -180, "y": 0, "z": 0},

            # Repeat the same pattern with 1 as a hub
            {"number": "1", "x": 0, "y": 0, "z": -60},

            {"number": "", "x": -41.81, "y": 0, "z": 0},
            {"number": "19", "x": 0, "y": 0, "z": -60},
            {"number": "", "x": -41.81, "y": 0, "z": 0},
            # {"number": "underscore", "x": 0, "y": 0, "z": -0},
            {"number": "9", "x": 41.81, "y": 0, "z": 0},
            {"number": "", "x": 0, "y": 0, "z": 120},
            {"number": "", "x": -41.81, "y": 0, "z": 0},
            {"number": "3", "x": 41.81, "y": 0, "z": 0},
            {"number": "", "x": 0, "y": 0, "z": -60},
            {"number": "", "x": 41.81, "y": 0, "z": 0},
            {"number": "", "x": 0, "y": 0, "z": -120},

            {"number": "", "x": -41.81, "y": 0, "z": 0},
            {"number": "13", "x": 0, "y": 0, "z": -60},
            {"number": "", "x": -41.81, "y": 0, "z": 0},
            # {"number": "underscore", "x": 0, "y": 0, "z": -0},
            {"number": "5", "x": 41.81, "y": 0, "z": 0},
            {"number": "", "x": 0, "y": 0, "z": 120},
            {"number": "", "x": -41.81, "y": 0, "z": 0},
            {"number": "11", "x": 41.81, "y": 0, "z": 0},
            {"number": "", "x": 0, "y": 0, "z": -60},
            {"number": "", "x": 41.81, "y": 0, "z": 0},
            {"number": "", "x": 0, "y": 0, "z": -120},

            {"number": "", "x": -41.81, "y": 0, "z": 0},
            {"number": "7", "x": 0, "y": 0, "z": -60},
            {"number": "", "x": -41.81, "y": 0, "z": 0},
            # {"number": "underscore", "x": 0, "y": 0, "z": -0},
            {"number": "17", "x": 41.81, "y": 0, "z": 0},
            {"number": "", "x": 0, "y": 0, "z": 120},
            {"number": "", "x": -41.81, "y": 0, "z": 0},
            {"number": "15", "x": 41.81, "y": 0, "z": 0},
            {"number": "", "x": 0, "y": 0, "z": -60},
            {"number": "", "x": 41.81, "y": 0, "z": 0},
            {"number": "", "x": 0, "y": 0, "z": -120},

            {"number": "", "x": 0, "y": 0, "z": -60},
            {"number": "", "x": -180, "y": 0, "z": 0}
        ],
        "num_location": (0, 0, 11),
        "num_scale": (280, 280, 000),
        "final_location": (0, 0, 0),
        "number_height": 4
    }
]


# Set up file names
files_in_output_folder = []
for output_file in listdir(output_folderpath):
    if isfile(join(output_folderpath, output_file)):
        files_in_output_folder.append(output_file)


for new_dice in dice_list:
    possible_version_found = False
    version_number = 1
    while not possible_version_found:
        new_file_name = new_dice["name"] + "-v" + str(version_number)
        new_stl_file = new_file_name + ".stl"
        new_blend_file = new_file_name + ".blend"
        if new_stl_file in files_in_output_folder or new_blend_file in files_in_output_folder:
            version_number += 1
        else:
            possible_version_found = True
    new_dice["output_path"] = join(output_folderpath, new_file_name)


# Helper Functions

def select_object(obj):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = obj


def rotate_object(dice_object, xyz_degrees, reverse=False, order="xyz"):
    if reverse:
        xyz_degrees['x'] = -xyz_degrees['x']
        xyz_degrees['y'] = -xyz_degrees['y']
        xyz_degrees['z'] = -xyz_degrees['z']
    bpy.ops.object.select_all(action='DESELECT')
    dice_object.select_set(True)

    for axis in order:
        if xyz_degrees[axis] != 0:
            bpy.ops.transform.rotate(value=radians(xyz_degrees[axis]), orient_axis=axis.upper())
            bpy.ops.object.transform_apply(rotation=True)


def apply_bool_mod(main_object, secondary_object, modifier='DIFFERENCE'):
    # Create a boolean modifier named 'bool_mod' for the main_object.
    mod_bool = main_object.modifiers.new('bool_mod', 'BOOLEAN')
    # Set the mode of the modifier to DIFFERENCE.
    mod_bool.operation = modifier
    # Set the number to be used by the modifier.
    mod_bool.object = secondary_object

    # The modifier_apply function only works on the active object.
    # Set the main_object as the active object.
    select_object(main_object)
    res = bpy.ops.object.modifier_apply(modifier='bool_mod')


def create_d10_shape():
    # Create two cones with 5 vertices
    bpy.ops.mesh.primitive_cone_add(vertices=5, radius1=2, radius2=0, depth=2.25)
    d10_shape = bpy.context.object
    bpy.ops.mesh.primitive_cone_add(vertices=5, radius1=2, radius2=0, depth=2.25)
    d10_intersect = bpy.context.object
    # Rotate one of those by 180 on thew X-axis
    bpy.ops.object.select_all(action='DESELECT')
    d10_intersect.select_set(True)
    bpy.ops.transform.rotate(value=radians(180), orient_axis='X')
    # Apply an intersect modifier on the two cones
    apply_bool_mod(d10_shape, d10_intersect, 'INTERSECT')
    # Delete the spare full cone
    bpy.ops.object.select_all(action='DESELECT')
    d10_intersect.select_set(True)
    bpy.ops.object.delete()
    return d10_shape


def create_object(dice_name):
    if dice_name.startswith("d4-") or dice_name == "d4":
        bpy.ops.mesh.primitive_solid_add(source='4')

    elif dice_name.startswith("d6-") or dice_name == "d6":
        bpy.ops.mesh.primitive_solid_add(source='6')

    elif dice_name.startswith("d8-") or dice_name == "d8":
        bpy.ops.mesh.primitive_solid_add(source='8')

    elif dice_name.startswith("d10-") or dice_name == "d10":
        d10_single = create_d10_shape()
        bpy.ops.object.select_all(action='DESELECT')
        d10_single.select_set(True)

    elif dice_name.startswith("d12-") or dice_name == "d12":
        bpy.ops.mesh.primitive_solid_add(source='12')

    elif dice_name.startswith("d20-") or dice_name == "d20":
        bpy.ops.mesh.primitive_solid_add(source='20')

    if tweaks_for_font.get("num_version"):
        dice_name += "-" + tweaks_for_font["num_version"]
    # Get the object and rename it.
    dice = bpy.context.object
    dice.name = dice_name
    return dice


def resize_dice(dice_object):
    if dice_object.name.startswith("d4"):
        rotate_object(dice_object, {"x": 0, "y": 180, "z": -30})
        dice_object.dimensions[2] = 20
        scale_factor = dice_object.scale[2]
        dice_object.scale = scale_factor, scale_factor, scale_factor
        bpy.ops.object.transform_apply(scale=True)

    elif dice_object.name.startswith("d6"):
        dice_object.dimensions = 16, 16, 16

    elif dice_object.name.startswith("d8"):
        rotate_object(dice_object, {"x": 0, "y": 45, "z": 0, "order": "yxz"})
        rotate_object(dice_object, {"x": -35.265, "y": 0, "z": 0, "order": "yxz"})
        dice_object.dimensions[2] = 16.4
        scale_factor = dice_object.scale[2]
        dice_object.scale = scale_factor, scale_factor, scale_factor
        bpy.ops.object.transform_apply(scale=True)

    elif dice_object.name.startswith("d10-single"):
        rotate_object(dice_object, {"x": 54.3, "y": 0, "z": 0})
        dice_object.dimensions[2] = 17
        scale_factor = dice_object.scale[2]
        dice_object.scale = scale_factor, scale_factor, scale_factor
        bpy.ops.object.transform_apply(scale=True)

    elif dice_object.name.startswith("d10-double"):
        rotate_object(dice_object, {"x": 54.3, "y": 0, "z": 0})
        dice_object.dimensions[2] = 17
        scale_factor = dice_object.scale[2]
        dice_object.scale = scale_factor, scale_factor, scale_factor
        bpy.ops.object.transform_apply(scale=True)

    elif dice_object.name.startswith("d12"):
        rotate_object(dice_object, {"x": 58.285, "y": 0, "z": 0})
        dice_object.dimensions[2] = 18.5
        scale_factor = dice_object.scale[2]
        dice_object.scale = scale_factor, scale_factor, scale_factor
        bpy.ops.object.transform_apply(scale=True)

    elif dice_object.name.startswith("d20"):
        rotate_object(dice_object, {"x": -20.905, "y": 0, "z": 0})
        dice_object.dimensions[2] = 20.7
        scale_factor = dice_object.scale[2]
        dice_object.scale = scale_factor, scale_factor, scale_factor
        bpy.ops.object.transform_apply(scale=True)


def gen_numbers_required(rotations_info):
    numbers_required = []
    for rotation in rotations_info:
        if rotation.get("number", "") != "":
            if rotation["number"] not in numbers_required:
                numbers_required.append(rotation["number"])
    return numbers_required


def scale_for_font(vector_1, dice_name):
    for dice, scale_tweaks in tweaks_for_font["num_scale"].items():
        if dice_name.startswith(dice) or dice_name == dice:
            new_vector = (vector_1[0] * (scale_tweaks[0] or 1),
                          vector_1[1] * (scale_tweaks[1] or 1),
                          vector_1[2] * (scale_tweaks[2] or 1)
                          )
            return new_vector
    return vector_1


def save_dice(object_to_save, file_path):
    select_object(object_to_save)
    if file_path.endswith(".stl"):
        bpy.ops.export_mesh.stl(filepath=file_path)
    elif file_path.endswith(".blend"):
        bpy.ops.wm.save_as_mainfile(filepath=file_path)
    else:
        msg = "Invalid file type: " + file_path
        raise Exception(msg)


def wipe_slate():
    col = bpy.data.collections.get("Master Collection")
    if col:
        for obj in col.objects:
            obj.select_set(True)
    bpy.ops.object.delete()


# Main Script:
objs = bpy.data.objects


for dice_info in dice_list:
    # Create the Dice shape
    dice_obj = create_object(dice_info["name"])
    # Resize and prepare the location of the dice shape
    resize_dice(dice_obj)

    numbers_required = gen_numbers_required(dice_info["rotations"])
    # append all objects from the numbers file that are in the "numbers_required" list
    with bpy.data.libraries.load(str(numbers_filepath)) as (data_from, data_to):
        objects_to_pull = []
        for name in data_from.objects:
            if name in numbers_required:
                objects_to_pull.append(name)
        data_to.objects = objects_to_pull

    # link them to scene
    scene = bpy.context.scene
    for obj in data_to.objects:
        if obj is not None:
            scene.collection.objects.link(obj)

    # Create a dictionary for each number face so we don't
    #   resize it twice, primarily for the d4
    resized_numbers = {}
    for number in numbers_required:
        resized_numbers[number] = 0

    for rotation in dice_info["rotations"]:
        # rotation = dice_info["rotations"][0]
        if rotation["number"]:
            # Select the face
            # print("Face selected: ", rotation['number'])
            num_obj = bpy.data.objects[rotation['number']]
            select_object(num_obj)

            # Move and resize the face
            num_obj.location = dice_info["num_location"]
            if resized_numbers[rotation["number"]] == 0:
                select_object(num_obj)

                num_obj.scale = scale_for_font(dice_info["num_scale"], dice_obj.name)
                bpy.ops.object.transform_apply(scale=True)

                num_obj.dimensions[2] = dice_info.get("number_height", 2)
                resized_numbers[rotation["number"]] = 1

            # Apply the Difference Bool mod to the cube & number
            # print("Applying Bool")
            apply_bool_mod(dice_obj, num_obj)
            # print("Bool applied")
            num_obj.location = (20, 20, 20)

        # Rotate the cube.
        # This works for d4 & d6:
        rotate_object(dice_obj,
                      {"x": rotation['x'],
                       "y": rotation['y'],
                       "z": rotation['z']},
                      reverse=False)

    # Delete the numbers
    for number in numbers_required:
        objs.remove(objs[number], do_unlink=True)

    if save_files == True:
        save_dice(object_to_save=dice_obj, file_path=str(dice_info['output_path'])+".blend")
        save_dice(object_to_save=dice_obj, file_path=str(dice_info['output_path'])+".stl")
        objs.remove(objs[dice_info["name"]], do_unlink=True)
    else:
        dice_obj.location = dice_info["final_location"]
        bpy.ops.object.transform_apply(location=True)
