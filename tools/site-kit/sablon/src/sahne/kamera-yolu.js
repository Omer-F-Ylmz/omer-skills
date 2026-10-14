// Sürekli kamera yolu: t (0..1, scroll) → konum ve bakış eğrisi (CatmullRom centripetal, sabit hızlı getPointAt). Bölüm pozları yerine tek yol.
import { CatmullRomCurve3, Vector3 } from 'three';

export function kameraYolu(kam, konumlar, hedefler) {
  const egri = (d) => new CatmullRomCurve3(d.map((v) => new Vector3(...v)), false, 'centripetal');
  const yol = egri(konumlar);
  const bak = egri(hedefler);
  const h = new Vector3();
  return (t) => {
    yol.getPointAt(t, kam.position);
    kam.lookAt(bak.getPointAt(t, h));
  };
}
