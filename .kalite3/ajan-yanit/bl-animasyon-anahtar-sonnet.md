Turntable plan (4 s). I did not scan any scene or file, and nothing has been run in Blender. Assumptions: 24 fps, one product object (named "Product"), origin at its center.

1. Time and frames: N = 4 s x 24 fps = 96 frames. Set frame_start=1, frame_end=96, fps=24.
2. Keyframes (2 only), rotation_euler Z:
   - Frame 1: 0 deg (0 rad).
   - Frame 97 (N+1): 360 deg (6.283185 rad).
   - X and Y stay untouched.
3. Loop handling: frame 97 is outside the range (frame_end=96), so it is never rendered. Frame 96 is 354.4 deg (360 x 95/96), and the next frame, 1, is 0 deg, so the step into the loop is the same 3.75 deg as every other step. This avoids a duplicated frame (0 deg and 360 deg are the same pose) and the stutter it would cause.
4. Easing: set Linear interpolation on both keys, and Linear extrapolation as a fallback. Speed is constant at 90 deg/s (3.75 deg per frame). Bezier would make the spin slow down at the ends.
5. Pivot: the object origin at the product center (Object > Set Origin > Origin to Geometry). For a multi-part product, parent the parts to an Empty at the center and rotate the Empty instead.
6. Camera and light: both static and not parented to the product. The camera is at roughly 35-50 deg FOV, framed so the product fits at every angle, aimed at the pivot. Lighting is a fixed 3-point setup or an HDRI. Because the product rotates, the reflections and shadows change over the loop, which is normal for a turntable.
7. Code (bpy):
```
import bpy, math
s = bpy.context.scene
s.render.fps = 24; s.frame_start = 1; s.frame_end = 96
o = bpy.data.objects["Product"]
o.rotation_euler = (0, 0, 0); o.keyframe_insert("rotation_euler", index=2, frame=1)
o.rotation_euler[2] = math.radians(360); o.keyframe_insert("rotation_euler", index=2, frame=97)
for fc in o.animation_data.action.fcurves:
    for k in fc.keyframe_points: k.interpolation = 'LINEAR'
```
   Newer Blender versions (4.4+ with layered actions) may need a different way to reach the fcurves. Check this on your version.
8. Verification (to run):
   - At frames 1, 25, 49, 73 and 96, read rotation_euler.z. Expected: 0, 90, 180, 270 deg, and 354.375 deg at frame 96. At frame 97 it should read 360 deg.
   - In the Graph Editor, the Z curve should be a straight line with no handles.
   - Render a still at frame 1 and one at frame 49. They should differ by a 180 deg turn.
   - Play it as a loop. There should be no hitch at the wrap from 96 to 1.

Skipped: render settings (engine, resolution, output format), the real object name, and the camera and light placement. They are not covered because no scene was read. Risk: if the real project is not 24 fps or the object has a different name, N and the object name change, but the rule stays the same (keys at 1 and N+1, frame_end=N).