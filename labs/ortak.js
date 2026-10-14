// Lab ortak: renderer + kendi varlıklarımızla kahve dünyası (tornalanmış cezve/fincan, köz halkası, sis) + Lenis/ST + window.lab sözleşmesi (kare.py okur).
import * as THREE from 'three';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import Lenis from 'lenis';

gsap.registerPlugin(ScrollTrigger);
export const lab = (window.lab = { kare: 0, hazir: false, git: async () => {} });
export const bekle = (ms) => new Promise((r) => setTimeout(r, ms));

export function kur(cv, dpr = 2) {
  const r = new THREE.WebGLRenderer({ canvas: cv, antialias: true, alpha: true, powerPreference: 'high-performance' });
  r.setPixelRatio(Math.min(devicePixelRatio, dpr));
  r.toneMapping = THREE.ACESFilmicToneMapping;
  const kam = new THREE.PerspectiveCamera(35, 1, 0.1, 100);
  const boyut = () => {
    r.setSize(innerWidth, innerHeight, false);
    kam.aspect = innerWidth / innerHeight;
    kam.updateProjectionMatrix();
  };
  addEventListener('resize', boyut);
  boyut();
  return { r, kam };
}

const lt = (p) => p.map(([x, y]) => new THREE.Vector2(x, y));

// arka: null → saydam sahne (DOM tipografi arkada kalsın), sis ve zemin yok.
export function dunya(r, { arka = 0x1a120c, isik = 0xffb070, sis = 0.05 } = {}) {
  const s = new THREE.Scene();
  s.environment = new THREE.PMREMGenerator(r).fromScene(new RoomEnvironment(), 0.04).texture;
  s.environmentIntensity = 0.6;
  const bakir = new THREE.MeshPhysicalMaterial({ color: 0xb87333, metalness: 1, roughness: 0.3, clearcoat: 0.5, side: THREE.DoubleSide, dithering: true });
  const seramik = new THREE.MeshPhysicalMaterial({ color: 0xf2ebe1, roughness: 0.4, clearcoat: 1, side: THREE.DoubleSide, dithering: true });
  const kahve = new THREE.MeshPhysicalMaterial({ color: 0x3b2314, roughness: 0.15, clearcoat: 1, dithering: true });
  const cezve = new THREE.Mesh(new THREE.LatheGeometry(lt([[0, 0], [0.55, 0], [0.6, 0.08], [0.46, 0.75], [0.56, 1]]), 64), bakir);
  const sap = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.05, 1.4, 12), bakir);
  sap.rotation.z = Math.PI / 2.4;
  sap.position.set(1.15, 0.95, 0);
  cezve.add(sap);
  const koz = new THREE.Mesh(new THREE.TorusGeometry(0.7, 0.06, 16, 64), new THREE.MeshBasicMaterial({ color: new THREE.Color(isik).multiplyScalar(6) }));
  koz.rotation.x = -Math.PI / 2;
  koz.position.y = 0.02;
  const fincanG = new THREE.LatheGeometry(lt([[0, 0], [0.22, 0], [0.26, 0.04], [0.34, 0.42], [0.36, 0.44]]), 48);
  const yuz = new THREE.CircleGeometry(0.33, 48);
  const fincanlar = [-3, -6, -9, -12, -13.5].map((z, i) => {
    const g = new THREE.Group();
    const k = new THREE.Mesh(yuz, kahve);
    k.rotation.x = -Math.PI / 2;
    k.position.y = 0.38;
    g.add(new THREE.Mesh(fincanG, seramik), k);
    const son = i === 4;
    g.position.set(son ? 0 : i % 2 ? 1.3 : -1.3, son ? 0 : 0.5 + i * 0.15, z);
    g.rotation.z = son ? 0 : i % 2 ? -0.3 : 0.3;
    s.add(g);
    return g;
  });
  const gunes = new THREE.DirectionalLight(isik, 2.5);
  gunes.position.set(3, 6, 4);
  const nokta = new THREE.PointLight(isik, 8, 6);
  nokta.position.set(0, 0.3, 0);
  s.add(cezve, koz, gunes, nokta, new THREE.HemisphereLight(0xffffff, arka ?? 0x000000, 0.4));
  if (arka !== null) {
    s.background = new THREE.Color(arka);
    s.fog = new THREE.FogExp2(arka, sis);
    const zemin = new THREE.Mesh(new THREE.PlaneGeometry(80, 80), new THREE.MeshStandardMaterial({ color: 0x24170e, roughness: 0.85, dithering: true }));
    zemin.rotation.x = -Math.PI / 2;
    s.add(zemin);
  }
  return { s, cezve, fincanlar };
}

// Lenis + ScrollTrigger tek saat; lab.git(p) sayfayı p'ye atlatır, scrub yetişsin diye bekler.
export function kaydir() {
  const lenis = new Lenis();
  lenis.on('scroll', ScrollTrigger.update);
  gsap.ticker.add((t) => lenis.raf(t * 1000));
  gsap.ticker.lagSmoothing(0);
  lab.git = async (p) => {
    lenis.scrollTo(p * (document.documentElement.scrollHeight - innerHeight), { immediate: true, force: true });
    await bekle(1800);
  };
  return lenis;
}

export const kosu = (to) => ({ trigger: document.body, start: 'top top', end: 'bottom bottom', scrub: 1, ...to });
