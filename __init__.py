bl_info = {
    "name": "Automated Lipsync",
    "description" : "Automates lipsyncing for MecaFace facial animation rigs.",
    "version" : (0, 0, 5),
    "blender": (2, 80, 0),
    "category": "Animation",
}

import bpy
from bpy.types import (Panel, Operator)
from bpy_extras.io_utils import ImportHelper
from bpy.props import (StringProperty, IntProperty, EnumProperty, BoolProperty)
from bpy.utils import (register_class, unregister_class)
import json

phones = {
    "a" : "A",
    "aː" : "A",
    "b" : "L",
    "d" : "L",
    "d̠" : "L",
    "e" : "E",
    "eː" : "E",
    "e̞" : "E",
    "f" : "F",
    "h" : "A",
    "i" : "A",
    "iː" : "A",
    "j" : "L",
    "k" : "S",
    "kʰ" : "S",
    "l" : "L",
    "m" : "M",
    "n" : "S",
    "o" : "O",
    "oː" : "O",
    "p" : "F",
    "pʰ" : "F",
    "r" : "R",
    "s" : "S",
    "t" : "S",
    "tʰ" : "TH",
    "t̠" : "L",
    "u" : "O",
    "uː" : "O",
    "v" : "F",
    "w" : "W",
    "x" : "S",
    "z" : "S",
    "æ" : "A",
    "ð" : "TH",
    "øː" : "O",
    "ŋ" : "N",
    "ɐ" : "O",
    "ɐː" : "O",
    "ɑ" : "O",
    "ɑː" : "O",
    "ɒ" : "A",
    "ɒː" : "A",
    "ɔ" : "O",
    "ɔː" : "O",
    "ɘ" : "E",
    "ə" : "E",
    "əː" : "E",
    "ɛ" : "E",
    "ɛː" : "E",
    "ɜː" : "E",
    "ɡ" : "O",
    "ɪ" : "A",
    "ɪ̯" : "A",
    "ɯ" : "E",
    "ɵː" : "A",
    "ɹ" : "R",
    "ɻ" : "R",
    "ʃ" : "S",
    "ʉ" : "O",
    "ʉː" : "O",
    "ʊ" : "O",
    "ʌ" : "O",
    "ʍ" : "W",
    "ʒ" : "S",
    "ʔ" : "O",
    "θ" : "TH",
    "d͡ʒ" : "L"
}

class Lipsync():

    def get_pose_from_phone(self, phone):
        return phones[phone]

    def get_phones(self, syncfile):
        with open(syncfile, "r") as f:
            result = []
            for line in f.readlines():
                data = line.split()
                phone = data[2]
                start = float(data[0])
                duration = float(data[1])
                result.append((phone, start, duration))
            return result

    def get_poses(self, syncfile):
        framerate = bpy.context.scene.render.fps
        allophones = self.get_phones(syncfile)
        result = []
        for p in allophones:
            pose = self.get_pose_from_phone(p[0])
            frame = round(p[1] / (1/framerate))
            result.append((pose, frame, p[2]))
        return result

    def get_pose_index(self, name):
        for i, pose in enumerate([pose.name for pose in bpy.context.object.pose_library.pose_markers]):
            if name == pose:
                return i

    def apply_pose(self, name):
        idx = self.get_pose_index(name)
        bpy.ops.poselib.apply_pose(pose_index=idx)
        [b.keyframe_insert("location") for b in bpy.context.selected_pose_bones]

    def set_frame(self, frame):
        bpy.context.scene.frame_set(frame)

    def apply_pose_data(self, data):
        pose = data[0]
        frame = data[1]
        self.set_frame(frame+bpy.context.object.frame_start)
        self.apply_pose(pose)

    def apply_lipsync(self, lipsync):
        frame = bpy.data.scenes[0].frame_current
        base_pose = bpy.context.object.base_pose
        self.apply_pose_data((base_pose, lipsync[0][1]-1, 0))
        for i, pose in enumerate(lipsync):
            self.apply_pose_data(pose)
            if i < len(lipsync)-1:
                if lipsync[i+1][1]-pose[1] > 4:
                    self.apply_pose_data((base_pose, i+2, 0))
                    self.apply_pose_data((base_pose, lipsync[i+1][1]-1, 0))
            else:
                self.apply_pose_data((base_pose, pose[1]+3, 0))
        self.set_frame(frame)
        
# Much of the following code was taken from various blogs and Stack Overflow tutorials

class ApplyLipsyncing(Operator):
    """Applies lipsyncing data"""
    bl_idname = "object.apply_lipsyncing"
    bl_label = "Apply Lipsyncing"

    def execute(self, context):
        sync = context.object.sync_file
        test = Lipsync()
        poses = test.get_poses(sync)
        test.apply_lipsync(poses)
        return {'FINISHED'}

class ProcessAudio(Operator):
    """Processes lipsync audio"""
    bl_idname = "object.process_audio"
    bl_label = "Process Audio"
    
    def execute(self, context):
        if context.object.wav_file == "":
            return {'FINISHED'}
        #insert Allosaurus processing here
        result = [('F', 16, 0.025), ('O', 18, 0.025), ('R', 21, 0.025), ('S', 22, 0.025), ('E', 23, 0.025), ('L', 24, 0.025), ('S', 26, 0.025), ('O', 27, 0.025), ('L', 40, 0.025), ('A', 42, 0.025), ('L', 42, 0.025), ('O', 46, 0.025), ('S', 48, 0.025), ('A', 49, 0.025), ('S', 51, 0.025), ('S', 53, 0.025), ('A', 54, 0.025), ('L', 54, 0.025), ('S', 58, 0.025), ('S', 60, 0.025), ('R', 61, 0.025), ('A', 62, 0.025), ('F', 66, 0.025), ('E', 67, 0.025), ('L', 69, 0.025)]
        context.object.phones = json.dumps(result)
        
        return {'FINISHED'}
    
class OpenFile(Operator, ImportHelper):
    """Opens a lipsync file for processing"""
    bl_idname = 'test.open_file'
    bl_label = 'Open SYNC File'
    bl_options = {'PRESET', 'UNDO'}
 
    filename_ext = '.sync'
    
    filter_glob: StringProperty(
        default='*.sync',
        options={'HIDDEN'}
    )
 
    def execute(self, context):
        print(self.properties.filepath)
        context.object.sync_file = self.properties.filepath
        return {'FINISHED'}
    

class LipsyncPanel(Panel):
    bl_idname = "object.custom_panel"
    bl_label = "Automated Lipsync"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "Lipsync"
    bl_context = "posemode"   


    @classmethod
    def poll(self,context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        obj = context.object

        layout.label(text="Select the entire MecaFace rig.")
        layout.label(text="Then, select a lipsync file below.")
        
        col = layout.column(align=True)
        col.operator(OpenFile.bl_idname, text="Choose lipsync file", icon="FILE_FOLDER")
        layout.separator()

        col = layout.column(align=True)
        col.prop(obj, "frame_start")
        col.label(text="Base pose for the start and end:")
        col.prop(obj, "base_pose")
        col.operator(ApplyLipsyncing.bl_idname, text="Apply Lipsyncing", icon="FORWARD")

        layout.separator()

def register():
    register_class(LipsyncPanel)
    register_class(ApplyLipsyncing)
    register_class(OpenFile)
    register_class(ProcessAudio)
    bpy.types.Object.frame_start = bpy.props.IntProperty(name="Start Frame",
                                                            description="The frame to start the lipsync at",     
                                                            min=0,
                                                            default=0)
    
    def get_items(self, context):
        return [(pose.name, pose.name, "Use this pose as the base pose") for pose in context.object.pose_library.pose_markers]
    bpy.types.Object.base_pose = bpy.props.EnumProperty(name="",
                                                            description="The pose to use at the start, end, and between words",
                                                            options={'ANIMATABLE'},
                                                            items=get_items)
    bpy.types.Object.sync_file = bpy.props.StringProperty()

def unregister():
    unregister_class(LipsyncPanel)
    unregister_class(ApplyLipsyncing)
    unregister_class(OpenFile)
    unregister_class(ProcessAudio)
    del bpy.types.Object.frame_start
    del bpy.types.Object.base_pose
    del bpy.types.Object.sync_file

if __name__ == "__main__":
    register()