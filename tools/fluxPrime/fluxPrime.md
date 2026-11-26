[← cd ~/portfolio](../README.md)

# `$ cat ~/tools/fluxPrime.md`

```yaml
Tool             : fluxPrime
Version          : v0.2.1 (Experimental)
Category         : Engine Plugin / Crowd Simulation Framework
Context          : Personal Project / Engine R&D
Platform         : PC (Windows)
Engine           : Unreal Engine 5.6
Language         : C++ (DOD, SoA, StructUtils, GameplayTags)
Role             : Engine & Systems Programmer
Version Control  : Git
Timeline         : July 2026 - Now
```

### Editor & Runtime Showcase
<!-- SERET & LEPAS (DRAG & DROP) GIF / VIDEO .MP4 SIMULASI RIBUAN AGENT ATAU PROFILER DI BARIS BAWAH INI -->


```yaml
Showcase      : High-performance, ECS-inspired crowd simulation plugin for Unreal Engine 5.6
Highlights    : Tag-addressed SoA memory pools, AnimToTexture (VAT), ISMC batching & Dumb Client netcode
```

<details>
<summary><b>📸 View Screenshot Gallery (0)</b></summary>
<br>

</details>

---

### Problem & Workflow Impact
```yaml
The Bottleneck : Per-agent AActor/UObject ticking, SkeletalMesh evaluation & Chaos Physics collapse frame times at scale
The Solution   : Built a Data-Oriented Design (DOD) runtime using contiguous SoA buffers, VAT & batched ISMC rendering
Designer Flow  : Modular UPrimaryDataAsset & FInstancedStruct presets allow swapping systems/FSM states without C++ edits
Impact         : O(1) swap-based pool compaction, physics-free grid raycasts & 10 Hz quantized batched replication
```

---

### Core Features & Architecture
```yaml
Memory & Data  : Contiguous archetype Structure-of-Arrays (SoA) mapped via FGameplayTag with O(1) SwapManualBuffer
Rendering      : Zero skeletal evaluation via Unreal AnimToTexture (VAT), Animation Notifies & batched ISMC updates
Spatial & Nav  : Prefix-sum dense spatial grid (Boids, hit queries, relevancy), Recast/Detour corridors & 2.5D baked terrain
Combat & VFX   : Grid-accelerated segment-to-point raycast, sphere-sweep melee & batched Niagara Data Channel projectiles
Networking     : Server-authoritative "Dumb Client" replication using 10 Hz FVector_NetQuantize10 batches (128/batch)
```

<details>
<summary><b>📂 Inspect Plugin Architecture (<code>$ tree Source/fluxPrime</code>)</b></summary>

```text
├───Authoring Layer (UPrimaryDataAsset + FInstancedStruct)
│       UFluxPrimeEntityCatalogIdentity   (Archetype mesh, stats, pool capacity)
│       UFluxPrimeDataStoreIdentity       (SoA GameplayTag -> Component type schema)
│       UFluxPrimeStateIdentity           (FSM states & transition fragments)
│       UManagerConfiguration             (Runtime module fragments)
│       USystemsConfiguration             (Runtime system fragments & mesh orientation)
├───Orchestration & Networking Layer
│       AFluxPrimeCrowdsController        (Level host actor & authority delegate wiring)
│       UFluxPrimeCrowdsManager           (Owns archetype DataStores, module/system ticks)
│       UFluxPrimeNetManager              (Server-to-client Unreliable Multicast snapshots)
│       UFluxPrimeCrowdsTargetManager     (Player-owned component for Server Reliable RPCs)
│       UFluxPrimeCrowdsWorldSubsystem    (External gameplay facade via FInstancedStruct payloads)
└───Simulation & Rendering Pipeline (USTRUCT Systems over SoA Buffers)
    ├───Core / Generic Systems
    │       FFluxPrimeSpatialGridSystem         (Prefix-sum dense spatial partitioning)
    │       FFluxPrimeNavigationSystem          (Recast/Detour pathfinding & corridors)
    │       FFluxPrimeBoidsSystem               (Spatial-grid neighbor separation)
    │       FFluxPrimeMovementSystem            (Kinematic steering & velocity integration)
    │       FFluxPrimeGroundHeightSystem        (2.5D multi-layer baked terrain height)
    │       FFluxPrimeRaycastSystem             (Grid-accelerated segment-to-point hit query)
    │       FFluxPrimeHealthSystem              (Contiguous damage accumulation & health)
    │       FFluxPrimeAnimationSystem           (VAT frame playback & notify dispatching)
    │       FFluxPrimeVisualInterpolationSystem (Client-side VInterpTo / FInterpTo smoothing)
    │       FFluxPrimeRenderSystem              (Batched ISMC transform updates)
    └───Crowds Domain Systems
            FFluxPrimeCrowdsStateMachineSystem  (Integer-indexed FSM & transition evaluation)
            FFluxPrimeCrowdsTargetSystem        (Priority, load balancing & target stickiness)
            FFluxPrimeCrowdsAbilitySystem       (Melee sweep & Niagara projectile abilities)
            FFluxPrimeCrowdsSnapshotSystem      (10 Hz quantized batched network snapshots)
            FFluxPrimeCrowdsKillEventSystem     (Player kill tracking via FUniqueNetIdRepl)
            FFluxPrimeCrowdsCompactSystem       (Swap-based pool recycling)
```

</details>

---

### Technical Challenges & Solutions
```yaml
Challenge     : Simulating, networking, and rendering massive crowds in UE5 without per-agent Actor/Physics overhead
Solution      : Replaced AActor lifecycles & Chaos bodies with tag-addressed SoA pools, prefix-sum grid & VAT/ISMC
Result        : Eliminated heap fragmentation and skeletal/physics bottlenecks while keeping Editor authoring modular
```

---

### Documentation & Access
<pre>
Source / Package : Proprietary / Engine Plugin (Unreal Engine 5.6)
Video Demo       : -
</pre>

<br>

[← cd ~/portfolio](../README.md)
