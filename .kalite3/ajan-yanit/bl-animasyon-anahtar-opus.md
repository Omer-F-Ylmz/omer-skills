Subagent `bl-animasyon-anahtar` report, verbatim:

I didn't open any scene; this is a plan only. It assumes 24 fps and a single product object named "Product". Nothing has been run or rendered.

1. Timing: 4 s × 24 fps = 96 frames. Set fps = 24, frame_start = 1 and frame_end = 96.
2. Rotation: around Z only, 0° to 360°, which is 3.75° per frame. Keep X and Y at 0.
3. Keyframes (just 2): frame 1 has Z = 0°, and frame 97 (N+1) has Z = 360°. Frame 97 is never rendered, so the last frame (96, at 356.25°) runs straight back into frame 1 (0°) with no repeated pose and no stutter.
4. Easing: none. Use Linear interpolation so the speed stays constant. Ease-in/out would slow down at the loop seam. Only use Bezier or ease in the Graph Editor if you want a single spin that doesn't loop.
5. Pivot: put the origin at the product's centre with Set Origin > Origin to Geometry, and place the product at world (0,0,0). If the product has several parts, parent them to an Empty at the product's centre and put the keyframes on the Empty only. Leave the camera and lights still and don't parent them to it.
6. bpy (keys "Product", or the Empty if you used one):
   ```
   import bpy, math; s=bpy.context.scene; s.render.fps=24; s.frame_start,s.frame_end=1,96
   o=bpy.data.objects["Product"]; o.rotation_euler.z=0; o.keyframe_insert("rotation_euler",index=2,frame=1)
   o.rotation_euler.z=math.radians(360); o.keyframe_insert("rotation_euler",index=2,frame=97)
   for k in o.animation_data.action.fcurves[0].keyframe_points: k.interpolation='LINEAR'
   ```
7. Checks to run: read rotation_euler.z after s.frame_set(f). Frame 1 should be 0°, frame 49 should be 180° and frame 96 should be 356.25°. Then render frames 96 and 1 and look at them side by side: the step between them should look the same size as every other step. Finally, play the 1–96 range on loop and watch for a hitch.

Not checked: the code hasn't been run. In Blender 5.0 and later, `action.fcurves` may need to be changed to `action.layers[0].strips[0].channelbags[0].fcurves`. The subagent also did not open the `departman-diger` skill, which your CLAUDE.md asks for before a task; it said that was because this was plan-only.