# Blender Lipsync Addon

This addon does not do any lipsyncing by itself, but applies existing phoneme data generated with Allosaurus, a wonderful Python module. It is presently targeted at the MecaFace facial animation rig but may be useful for other rigs, and may be expanded to be general-purpose in the future.

For our purposes I've written a Discord bot for this, but pasting the output of:

`python -m allosaurus.run -i <your WAV file> --model eng2102 --lang eng --timestamp=True`

into a new file with the extension `.sync` should also give you what you need.
