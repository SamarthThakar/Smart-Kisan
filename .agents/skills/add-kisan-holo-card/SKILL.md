---
name: add-kisan-holo-card
description: "Build an interactive 3D Kisan Holographic Trading Card for Smart-Kisan using Three.js r180, custom holographic foil GLSL shaders, drifting golden pollen/ember particles, pointer-reactive specular lighting, and tactile 3D tilt, rotation, and flip controls. Use when creating or embedding premium agricultural badge, crop mastery, or farmer achievement cards."
---

# Build Kisan Holographic Card (Smart-Kisan)

## Description

The **Kisan Ratna / Golden Harvest** holographic trading card stands beside a sunlit field altar, featuring engraved golden wheat borders, iridescent rainbow foil reflection, drifting sunlight dust and pollen embers, pointer-reactive dynamic lighting, and tactile tilt, 3D rotation, and flip controls (revealing soil health metrics, crop mastery stats, and government scheme verification badges on the reverse side).

Recreate the high-fidelity interactive 3D effect tailored specifically for the Smart-Kisan agricultural platform without requiring heavy external UI dependencies.

---

## Thematic Mapping: From Dark Souls to Smart-Kisan

| Dark Souls Concept | Smart-Kisan Farming Equivalent |
|---|---|
| **Ashen One / Warrior Hero** | **Kisan Ratna / Farmer Hero** (featuring heritage crops: Sharbati Wheat, Kashmiri Saffron, Alphonso King) |
| **Candlelit Sword Shrine** | **Sunlit Harvest Altar / Fertile Soil Pedestal** with sprouts and golden wheat sheaves |
| **Drifting Ash & Embers** | **Drifting Golden Pollen, Sunlight Dust Motes & Seed Spores** |
| **Engraved Gold Borders** | **Intricate Filigree of Wheat Ears, Vine Shoots & Ashok Chakra / Kisan Emblems** |
| **Dark Ash & Iron Palette** | **Emerald Green, Terracotta Earth, and Radiant Harvest Gold Palette** |
| **Card Back: Dark Sigil** | **Smart-Kisan Soil Health Score, Farmer ID QR, and Scheme Verification Badges** |

---

## Technologies

- **React iframe / Component host**: Clean container boundary inside Smart-Kisan (Profile, Dashboard, or Scheme modal)
- **Three.js r180** (via CDN / jsDelivr or npm) + custom WebGL / GLSL shaders
- **Holographic Foil Shader**: Custom fragment shader calculating view angle, normal perturbation, and iridescent rainbow diffraction matrix
- **Particle System**: Instanced drifting pollen/sunlight motes with turbulent wind vectors
- **Embedded Assets**: Self-contained SVG vector badges, WebP textures, and typography (Outfit / Inter / Samarkan / Noto Sans)
- **Full Touch & Mouse Controls**: Pointer tilt, drag rotation, double-click or `F` to flip, wheel zoom, arrow navigation, and `R` to reset

---

## Verified Source Architecture in Smart-Kisan

- `frontend/public/effects/kisan-holo-card.html` — Self-contained interactive 3D scene with embedded shaders and assets
- `frontend/src/components/effects/KisanHoloCard.jsx` — React iframe host component with lazy loading, lifecycle management, and fallback
- Variants:
  - `variant="golden-wheat"` (Default: Golden Harvest Wheat Master)
  - `variant="saffron-royal"` (Kashmiri Saffron & Orchid Bloom)
  - `variant="soil-sentinel"` (Bio-Organic Soil Health & Moisture Mastery)

---

## Implementation Steps

1. **Standalone 3D Document**:
   - Create `frontend/public/effects/kisan-holo-card.html` containing the complete Three.js r180 canvas, holographic GLSL shaders, camera controls, and lighting pipeline.
   - Embed agricultural artwork (golden wheat sheaf motifs, holographic rainbow diffraction map, embossed metallic foil bump maps).
2. **Holographic Shader Pipeline**:
   - Implement custom vertex and fragment shaders for the card face combining diffuse crop texture, specular shine, and rainbow diffraction fresnel:
     ```glsl
     // Iridescent holographic foil dispersion
     vec3 viewDir = normalize(vViewPosition);
     float fresnel = dot(viewDir, vNormal);
     vec3 rainbow = 0.5 + 0.5 * cos(6.28318 * (fresnel * 2.0 + vec3(0.0, 0.33, 0.67) + uTime * 0.1));
     ```
3. **Pollen & Sunlight Particle Ambience**:
   - Add a GPU-accelerated particle system representing drifting golden spores and pollen motes gently swirling around the card.
4. **Interactive Controls & Gestures**:
   - Pointer move: Smooth spring-damped tilt and directional glare movement.
   - Drag: Full 3D inspection orbit.
   - Double-click or `F` key: 180° flip animation displaying the reverse side (Farmer Stats: N-P-K balance, Land Area, Scheme ID).
   - `R` key: Smoothly springs back to front-facing idle pose.
5. **React Host Integration**:
   - Host inside `frontend/src/components/effects/KisanHoloCard.jsx` with responsive aspect ratio, dark/light theme awareness, and WebGL context-loss recovery.

---

## Component Integration Example

```jsx
import React from 'react';
import { KisanHoloCard } from '../components/effects/KisanHoloCard';

export function FarmerProfileBadge({ farmerData }) {
  return (
    <div className="kisan-card-wrapper">
      <h3 className="text-xl font-bold text-amber-400">Verified Farmer Trophy Card</h3>
      <div className="aspect-[3/4] w-full max-w-sm mx-auto overflow-hidden rounded-2xl shadow-2xl border border-amber-500/30">
        <KisanHoloCard 
          variant="golden-wheat" 
          title="Master Cultivator"
          farmerName={farmerData?.full_name || "Kisan Mitr"}
          score="98/100 Soil Health"
        />
      </div>
    </div>
  );
}
```

---

## Behavior Contract

- **Runtime**: Self-contained HTML + Three.js r180 + custom GLSL + procedural particle emitter
- **Visual Passes**: Main scene render, subtle bloom/sunlight glare pass, chromatic foil shimmer
- **Card Front**: Golden embossed wheat sheaf artwork, holographic foil coating, tier gem badge
- **Card Back**: Smart-Kisan digital land record card, QR code, N-P-K nutrient metrics, and verified subsidy badges
- **Interactions**:
  - Pointer hover: Subtle dynamic tilt (±15°) + holographic specular highlight follow
  - Click & Drag: 360° rotational orbit
  - Double Click / `F`: 180° smooth flip to inspect card back
  - Mouse Wheel: Zoom in / zoom out
  - `R` Key: Reset camera and card orientation
  - Reduced Motion: Respects `prefers-reduced-motion` by disabling ambient particle drift and auto-tilt

---

## Guardrails

- **Agricultural Identity**: Preserve warm agrarian aesthetics (harvest gold, lush canopy greens, rich soil browns, solar radiance) — avoid bleak or apocalyptic tones.
- **Self-Contained**: Do not require heavy external 3D libraries or npm build complications; load Three.js via standard modules or pinned CDN.
- **Performance**: Cap pixel ratio at `Math.min(window.devicePixelRatio, 2)` and pause render loops when off-screen via `IntersectionObserver`.
