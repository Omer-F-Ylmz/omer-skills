# context7 /mrdoob/three.js — renderer dispose, setPixelRatio, instancing, performance tips

### dispose()

Source: https://github.com/mrdoob/three.js/blob/dev/docs/pages/GPUComputationRenderer.html.md

Frees all internal resources allocated by the renderer when it is no longer needed.

```APIDOC
## Method: `dispose`

### Description
Frees all internal resources. Call this method if you don't need the renderer anymore.

### Signature
`dispose() : void`
```

--------------------------------

### .[dispose](#dispose)() (async)

Source: https://github.com/mrdoob/three.js/blob/dev/docs/pages/Renderer.html

Frees all internal resources of the renderer. Call this method if the renderer is no longer in use by your app.

--------------------------------

### WebGLRenderer powerPreference and antialias configuration

Source: https://github.com/mrdoob/three.js/blob/dev/src/renderers/WebGLRenderer.js

Constructor destructuring shows antialias defaults to false and powerPreference is passed to the WebGL context. The JSDoc documents 'high-performance' as a valid powerPreference value for maximum GPU performance.

```typescript
constructor( parameters = {} ) {

	const {
		canvas = createCanvasElement(),
		context = null,
		depth = true,
		stencil = false,
		alpha = false,
		antialias = false,
		premultipliedAlpha = true,
		preserveDrawingBuffer = false,
		powerPreference = 'default',
		failIfMajorPerformanceCaveat = false,
		reversedDepthBuffer = false,
		outputBufferType = UnsignedByteType,
	} = parameters;

// ...

const contextAttributes = {
	alpha: true,
	depth,
	stencil,
	antialias,
	premultipliedAlpha,
	preserveDrawingBuffer,
	powerPreference,
	failIfMajorPerformanceCaveat,
};
```

--------------------------------

### Initialize scene and test ShaderMaterial memory disposal

Source: https://github.com/mrdoob/three.js/blob/dev/examples/webgl_test_memory2.html

Creates 100 sphere meshes and continuously reallocates new ShaderMaterial instances during render, logging renderer.info.programs.length before and after calling dispose().

```javascript
import \* as THREE from 'three'; const N = 100; let container; let camera, scene, renderer; let geometry; const meshes = \[\]; let fragmentShader, vertexShader; init(); setInterval( render, 1000 / 60 ); function init() { container = document.createElement( 'div' ); document.body.appendChild( container ); vertexShader = document.getElementById( 'vertexShader' ).textContent; fragmentShader = document.getElementById( 'fragmentShader' ).textContent; camera = new THREE.PerspectiveCamera( 40, window.innerWidth / window.innerHeight, 1, 10000 ); camera.position.z = 2000; scene = new THREE.Scene(); scene.background = new THREE.Color( 0xffffff ); geometry = new THREE.SphereGeometry( 15, 64, 32 ); for ( let i = 0; i < N; i ++ ) { const material = new THREE.ShaderMaterial( { vertexShader: vertexShader, fragmentShader: generateFragmentShader() } ); const mesh = new THREE.Mesh( geometry, material ); mesh.position.x = ( 0.5 - Math.random() ) \* 1000; mesh.position.y = ( 0.5 - Math.random() ) \* 1000; mesh.position.z = ( 0.5 - Math.random() ) \* 1000; scene.add( mesh ); meshes.push( mesh ); } renderer = new THREE.WebGLRenderer(); renderer.setPixelRatio( window.devicePixelRatio ); renderer.setSize( window.innerWidth, window.innerHeight ); container.appendChild( renderer.domElement ); } // function generateFragmentShader() { return fragmentShader.replace( 'XXX', Math.random() + ',' + Math.random() + ',' + Math.random() ); } function render() { for ( let i = 0; i < N; i ++ ) { const mesh = meshes\[ i \]; mesh.material = new THREE.ShaderMaterial( { vertexShader: vertexShader, fragmentShader: generateFragmentShader() } ); } renderer.render( scene, camera ); console.log( 'before', renderer.info.programs.length ); for ( let i = 0; i < N; i ++ ) { const mesh = meshes\[ i \]; mesh.material.dispose(); } console.log( 'after', renderer.info.programs.length ); }
```

--------------------------------

### IntersectionObserver pauses rendering when offscreen

Source: https://github.com/mrdoob/three.js/blob/dev/manual/examples/resources/lessons-helper.js

A helper that stops requestAnimationFrame when the page body scrolls offscreen. While not in the core renderer, this pattern is used in official Three.js examples to pause rendering and save GPU resources when the viewport is not visible.

```typescript
function initIntersectionObserver() {

	const intersectionObserver = new IntersectionObserver( ( entries ) => {

		entries.forEach( entry => {

			isBodyOnScreen = entry.isIntersecting;

		} );
		if ( isBodyOnScreen ) {

			startRAFIfIntersectingAndNeeded();

		} else {

			stopRAF();

		}

	} );
	intersectionObserver.observe( document.body );

}
```