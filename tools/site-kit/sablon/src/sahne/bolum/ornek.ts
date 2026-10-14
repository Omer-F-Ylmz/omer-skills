// Örnek bölüm sahnesi: kur(canvas) → { ilerle(p 0..1), calis(görünür mü) }. Yeni bölüm = bu dosyanın kopyası, adı bölüm id'si.
import * as THREE from 'three';

export async function kur(cv: HTMLCanvasElement) {
  const r = new THREE.WebGLRenderer({ canvas: cv, antialias: true, alpha: true });
  r.setPixelRatio(Math.min(devicePixelRatio, 2));
  const sahne = new THREE.Scene();
  const kam = new THREE.PerspectiveCamera(35, 1, 0.1, 50);
  kam.position.z = 6;
  const m = new THREE.Mesh(new THREE.IcosahedronGeometry(1, 3), new THREE.MeshNormalMaterial({ flatShading: true }));
  sahne.add(m);
  const boyut = () => {
    r.setSize(cv.clientWidth, cv.clientHeight, false);
    kam.aspect = cv.clientWidth / cv.clientHeight;
    kam.updateProjectionMatrix();
  };
  addEventListener('resize', boyut);
  boyut();
  let p = 0;
  let kare = 0;
  const ciz = () => {
    m.rotation.set(p * Math.PI, p * Math.PI * 2, 0);
    r.render(sahne, kam);
    kare = requestAnimationFrame(ciz);
  };
  return {
    ilerle: (x: number) => void (p = x),
    calis: (acik: boolean) => {
      cancelAnimationFrame(kare);
      if (acik) ciz();
    },
  };
}
