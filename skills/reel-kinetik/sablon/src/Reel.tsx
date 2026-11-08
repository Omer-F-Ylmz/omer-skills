// Kinetik altyazı + ses şablonu. Girdi reel.json: {words:[{t,start,end}], audio:"ses.wav"|null, fps, durationInFrames}. Süreler saniye.
import {AbsoluteFill, Audio, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
export type Word = {t: string; start: number; end: number};
export type ReelProps = {words: Word[]; audio: string | null; fps: number; durationInFrames: number};
const COLORS = ['#ffd400', '#ffffff', '#ff4d6d', '#4dd2ff'];
export const Reel = ({words, audio}: ReelProps) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  // Aktif kelime + önceki 2 kelime (3'lü kayan pencere); aktif olan büyür ve renk alır.
  const idx = Math.max(0, words.findIndex((w) => t >= w.start && t < w.end));
  const cur = words.findIndex((w) => t >= w.start && t < w.end);
  const win = cur < 0 ? [] : words.slice(Math.max(0, cur - 2), cur + 1).map((w, i, a) => ({w, aktif: i === a.length - 1, k: Math.max(0, cur - 2) + i}));
  return (
    <AbsoluteFill style={{background: 'linear-gradient(160deg,#10131f,#2a1b3d)', alignItems: 'center', justifyContent: 'center', fontFamily: 'Arial Black, Impact, sans-serif'}}>
      {audio ? <Audio src={staticFile(audio)} /> : null}
      <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 28, padding: 60}}>
        {win.map(({w, aktif, k}) => {
          const s = spring({frame: frame - Math.round(w.start * fps), fps, config: {damping: 12, stiffness: 180}});
          const sc = aktif ? interpolate(s, [0, 1], [0.6, 1.15]) : 0.8;
          return (
            <div key={k} style={{fontSize: aktif ? 150 : 90, color: aktif ? COLORS[k % COLORS.length] : '#ffffff88', transform: `scale(${sc})`, textTransform: 'uppercase', textAlign: 'center', lineHeight: 1.05, textShadow: '0 8px 30px #0008'}}>
              {w.t}
            </div>
          );
        })}
      </div>
      <div style={{position: 'absolute', bottom: 0, left: 0, height: 14, width: `${(frame / Math.max(1, words.length ? words[words.length - 1].end * fps : 1)) * 100}%`, background: '#ffd400'}} />
    </AbsoluteFill>
  );
};
