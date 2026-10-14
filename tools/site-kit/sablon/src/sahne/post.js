// Post yığını (pmndrs postprocessing, Zlib): DoF + bloom | kromatik + gren + vinyet + ACES. İki konvolüsyon (DoF, kromatik) tek geçişte birleşemez → 2 EffectPass.
// 'dusuk' kademe: yalnız bloom + vinyet, MSAA yok.
import {
  EffectComposer, RenderPass, EffectPass, BloomEffect, DepthOfFieldEffect, ChromaticAberrationEffect,
  NoiseEffect, VignetteEffect, ToneMappingEffect, ToneMappingMode, BlendFunction,
} from 'postprocessing';
import { HalfFloatType, Vector2 } from 'three';

export function postYigini(r, sahne, kam, kademe = 'yuksek') {
  const c = new EffectComposer(r, { frameBufferType: HalfFloatType, multisampling: kademe === 'yuksek' ? 4 : 0 });
  c.addPass(new RenderPass(sahne, kam));
  const bloom = new BloomEffect({ intensity: 1.4, luminanceThreshold: 0.7, luminanceSmoothing: 0.2, mipmapBlur: true });
  const vinyet = new VignetteEffect({ offset: 0.3, darkness: 0.65 });
  const ton = new ToneMappingEffect({ mode: ToneMappingMode.ACES_FILMIC });
  let dof = null;
  if (kademe === 'dusuk') {
    c.addPass(new EffectPass(kam, bloom, vinyet, ton));
  } else {
    dof = new DepthOfFieldEffect(kam, { worldFocusRange: 2.5, bokehScale: 4, resolutionScale: 0.5 });
    const kromatik = new ChromaticAberrationEffect({ offset: new Vector2(0.0015, 0.0015), radialModulation: true, modulationOffset: 0.25 });
    const gren = new NoiseEffect({ blendFunction: BlendFunction.OVERLAY, premultiply: true });
    gren.blendMode.opacity.value = 0.35;
    c.addPass(new EffectPass(kam, dof, bloom));
    c.addPass(new EffectPass(kam, kromatik, gren, vinyet, ton));
  }
  return { c, dof, bloom };
}
