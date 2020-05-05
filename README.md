# py_blender

This is currently still in development as I mess around with creating objects in Blender using Python scripts.

This has been built using:
- version 2.82a of Blender ([Blender downloads](https://www.blender.org/download/)).
- Ubuntu 18.04 (This will be relevant writing your filepath)

Credit to @cly_faker for the process from [this video](https://www.youtube.com/watch?v=nCowrvfOr3Q)

## To use:

Assuming you have the correct version of blender (The API changes quickly so it may not work with other versions):
1. Open Blender
2. Remove all the default objects
3. Click on "scripting" [In the top bar, to the far right]
4. If you've saved the file:
	- Click "Open" [Which should now be just below "scripting" at the bottom of the large blank area]
	- Navigate to where you have saved the "create_polyhedral_dice"
4. If you don't want to save the file:
	- Click "New" [Which should now be just below "scripting" at the bottom of the large blank area]
	- Paste the code in the newly created file
5. Click "Run Script" [In the same bar as the open/new file was, to the right]

### If you want to edit the dice information:

Firstly, I suggest you save the code somewhere and slowly tweak it.

Secondly, comment out all the other dice info you don't want to edit which will save time in running. If you're unfamiliar with code, many text editors allow you to select a large section of code and the keyboard shortcut `CTRL+/` will comment it out meaning it doesn't get used.

Thirdly, don't try and edit it in Blender as the text editor is slow to change, edit it in another text editor (Like notepad, or personally I suggest Sublime Text 3), save the file there and in Blender, to the left of where the "open" file was a flashing orange book symbol appears, click that and select `reload from disk` and it will update.