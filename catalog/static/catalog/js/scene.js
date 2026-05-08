import * as THREE from 'three';

const canvas = document.getElementById('space-canvas');
if (canvas && window.ASSETS) {
  initScene(canvas, window.ASSETS);
}

function initScene(canvas, ASSETS) {
  const isMobile = window.matchMedia('(max-width: 820px)').matches;
  // На десктопе Юпитер сдвинут вправо, на мобиле — по центру
  const jupiterX = isMobile ? 0 : 14;

  // ----- Renderer -----
  const renderer = new THREE.WebGLRenderer({
    canvas,
    antialias: !isMobile,
    alpha: false,
    powerPreference: 'high-performance',
  });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, isMobile ? 1.5 : 2));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 0.95;

  // ----- Scene & camera -----
  const scene = new THREE.Scene();

  const camera = new THREE.PerspectiveCamera(50, 1, 0.1, 2000);
  camera.position.set(0, 1.2, 28);

  // ----- Loader -----
  const loader = new THREE.TextureLoader();
  const load = (url) => new Promise((res, rej) => loader.load(url, res, undefined, rej));

  // ----- Lights -----
  // Ambient — лёгкая заливка, чтобы Луна не была чёрной
  scene.add(new THREE.AmbientLight(0x4a5468, 0.55));
  // Солнце — направленный свет сбоку, даёт серп тени на Юпитере
  const sun = new THREE.DirectionalLight(0xfff1d6, 1.6);
  sun.position.set(-50, 30, 25);
  scene.add(sun);
  // Тёплый рим-свет от Юпитера на поверхность Луны
  const rim = new THREE.PointLight(0xf4a85a, 1.6, 220, 1.5);
  rim.position.set(0, 18, -25);
  scene.add(rim);

  // ----- Build -----
  Promise.all([
    load(ASSETS.stars),
    load(ASSETS.jupiter),
    load(ASSETS.moon),
  ]).then(([starsTex, jupiterTex, moonTex]) => {
    starsTex.colorSpace   = THREE.SRGBColorSpace;
    jupiterTex.colorSpace = THREE.SRGBColorSpace;
    moonTex.colorSpace    = THREE.SRGBColorSpace;

    // Звёздное небо (skybox-сфера изнутри) — звёзды плотнее
    starsTex.wrapS = starsTex.wrapT = THREE.RepeatWrapping;
    starsTex.repeat.set(3, 2);
    const sky = new THREE.Mesh(
      new THREE.SphereGeometry(900, 64, 32),
      new THREE.MeshBasicMaterial({
        map: starsTex,
        side: THREE.BackSide,
        color: 0xb8c0d4, // чуть приглушаем, чтобы не пересвечивало
      })
    );
    scene.add(sky);

    // Юпитер — поднимается из-за горизонта
    const jupiter = new THREE.Mesh(
      new THREE.SphereGeometry(25, 128, 128),
      new THREE.MeshStandardMaterial({
        map: jupiterTex,
        roughness: 0.9,
        metalness: 0,
      })
    );
    jupiter.position.set(jupiterX, 2, -62);
    // Заметный наклон оси (как у настоящего Сатурна — для драматичности)
    jupiter.rotation.z = THREE.MathUtils.degToRad(18);
    jupiter.rotation.x = THREE.MathUtils.degToRad(-8);
    scene.add(jupiter);

    // Слабая «атмосфера» вокруг Юпитера — тёплое свечение
    const halo = new THREE.Mesh(
      new THREE.SphereGeometry(27, 64, 64),
      new THREE.MeshBasicMaterial({
        color: 0xf4a85a,
        transparent: true,
        opacity: 0.14,
        side: THREE.BackSide,
      })
    );
    halo.position.copy(jupiter.position);
    scene.add(halo);

    // Поверхность Луны — плоскость с рельефом, прячет нижнюю половину Юпитера
    moonTex.wrapS = moonTex.wrapT = THREE.RepeatWrapping;
    moonTex.repeat.set(8, 8);
    const ground = new THREE.Mesh(
      new THREE.PlaneGeometry(600, 600, 256, 256),
      new THREE.MeshStandardMaterial({
        map: moonTex,
        displacementMap: moonTex,
        displacementScale: 5,
        roughness: 1,
        metalness: 0,
      })
    );
    ground.rotation.x = -Math.PI / 2;
    ground.position.y = -1; // поднята так, чтобы нижняя половина Юпитера ушла за горизонт
    scene.add(ground);

    // Камера смотрит на сторону Юпитера — горизонт по центру кадра
    const lookTarget = new THREE.Vector3(jupiterX * 0.5, 5, jupiter.position.z);
    camera.lookAt(lookTarget);

    // ----- Drag-to-rotate: пользователь крутит сам Юпитер мышкой/пальцем -----
    canvas.style.cursor = 'grab';
    let dragging = false;
    let lastX = 0, lastY = 0;
    let velX = 0, velY = 0;     // инерция после отпускания
    let userInteracting = false;
    let resumeTimeout = null;

    function onPointerDown(e) {
      dragging = true;
      userInteracting = true;
      clearTimeout(resumeTimeout);
      lastX = e.clientX;
      lastY = e.clientY;
      velX = velY = 0;
      canvas.style.cursor = 'grabbing';
      canvas.setPointerCapture?.(e.pointerId);
    }
    function onPointerMove(e) {
      if (!dragging) return;
      const dx = (e.clientX - lastX) / canvas.clientWidth;
      const dy = (e.clientY - lastY) / canvas.clientHeight;
      lastX = e.clientX;
      lastY = e.clientY;
      // Крутим сам Юпитер, а не камеру
      jupiter.rotation.y += dx * Math.PI * 1.4;
      jupiter.rotation.x = THREE.MathUtils.clamp(
        jupiter.rotation.x + dy * Math.PI * 1.0,
        THREE.MathUtils.degToRad(-35),
        THREE.MathUtils.degToRad(20)
      );
      // Сохраняем скорость для инерции
      velX = dx * Math.PI * 1.4;
      velY = dy * Math.PI * 1.0;
    }
    function onPointerUp(e) {
      if (!dragging) return;
      dragging = false;
      canvas.style.cursor = 'grab';
      canvas.releasePointerCapture?.(e.pointerId);
      // Через 2с авто-вращение снова включается
      resumeTimeout = setTimeout(() => { userInteracting = false; }, 2000);
    }

    canvas.addEventListener('pointerdown', onPointerDown);
    canvas.addEventListener('pointermove', onPointerMove);
    window.addEventListener('pointerup', onPointerUp);
    window.addEventListener('pointercancel', onPointerUp);

    // ----- Resize -----
    function resize() {
      const w = canvas.clientWidth;
      const h = canvas.clientHeight;
      renderer.setSize(w, h, false);
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
    }
    resize();
    window.addEventListener('resize', resize);

    // ----- Animate -----
    let raf;
    const clock = new THREE.Clock();
    function tick() {
      const dt = clock.getDelta();
      if (dragging) {
        // во время перетаскивания вращение задаётся курсором, авто-крутим не нужно
      } else if (Math.abs(velX) > 0.0005 || Math.abs(velY) > 0.0005) {
        // инерция после отпускания — плавно гасим скорость
        jupiter.rotation.y += velX;
        jupiter.rotation.x = THREE.MathUtils.clamp(
          jupiter.rotation.x + velY,
          THREE.MathUtils.degToRad(-35),
          THREE.MathUtils.degToRad(20)
        );
        velX *= 0.93;
        velY *= 0.93;
      } else if (!userInteracting) {
        jupiter.rotation.y += dt * 0.05; // медленное авто-вращение
      }
      renderer.render(scene, camera);
      raf = requestAnimationFrame(tick);
    }
    tick();

    // Останавливаем рендер, когда вкладка скрыта
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) cancelAnimationFrame(raf);
      else tick();
    });
  }).catch((err) => {
    console.error('AstroBook scene: не удалось загрузить текстуры', err);
    canvas.style.background =
      'radial-gradient(ellipse at 50% 30%, #2a1810 0%, #05060d 70%)';
  });
}
