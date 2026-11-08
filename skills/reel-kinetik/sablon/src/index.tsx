import {registerRoot, Composition} from 'remotion';
import {Reel, ReelProps} from './Reel';
const defaults: ReelProps = {words: [], audio: null, fps: 30, durationInFrames: 150};
const Root = () => (
  <Composition id="Reel" component={Reel} width={1080} height={1920} fps={30} durationInFrames={150}
    defaultProps={defaults}
    calculateMetadata={({props}) => ({durationInFrames: (props as ReelProps).durationInFrames, fps: (props as ReelProps).fps})} />
);
registerRoot(Root);
