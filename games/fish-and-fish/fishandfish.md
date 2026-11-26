[← cd ~/portfolio](../../README.md)

# `$ cat ~/games/shooter.md`

```yaml
Project          : Shooter (Networked OpenGL Game)
Status           : Prototype / Academic Project
Context          : 3-Person Team Project
Platform         : PC (Windows)
Engine           : Custom Engine (OpenGL | GLM | GLFW | ImGui)
Language         : C++ & JSON
Role             : Engine & Core Loop Programmer
Version Control  : Git
Timeline         : October 2025 - November 2025
```

### Visual Showcase
![Gameplay GIF Shooter](shooter-gif.gif)

```yaml
Showcase      : Custom C++ OpenGL shooter decoupled from a backend GameAPI for networked state sync
Highlights    : OpenGL graphics pipeline, ECS & design-pattern core loop, JSON data-driven levels
```

<details>
<summary><b>📸 View Screenshot Gallery (0)</b></summary>
<br>
  
</details>

---

### Architecture & Gameplay Systems
```yaml
Core Engine   : Custom C++ game loop built on ECS, Singleton, State, Factory & core design patterns
Graphics      : Low-level OpenGL pipeline (Shaders, VAO/VBO/EBO, Textures), GLM math & ImGui debug UI
Gameplay      : Entity components/systems, Raycast logic, Enemy/Timer behaviors & JSON data_levels
Net Boundary  : Decoupled engine/game loop cleanly isolated from Integration/ & ASP.NET GameAPI backend
```

<details>
<summary><b>📂 Inspect Engine & Game Architecture (<code>$ tree Source</code>)</b></summary>

```text
├───Shooter (C++ OpenGL Client — Core Loop & Rendering)
│   ├───core
│   │   ├───engine
│   │   │   ├───factory
│   │   │   ├───input
│   │   │   ├───singleton
│   │   │   └───state (states)
│   │   ├───graphics_pipeline (shaders)
│   │   └───patterns
│   ├───game
│   │   ├───entity (components, systems)
│   │   ├───level (JSON data_levels loader)
│   │   ├───logic
│   │   ├───personal (awan, enemy, manuk, timer)
│   │   └───ray
│   ├───Integration (Client-side API & network bridge)
│   └───assets (ai, character, data_levels, environment, font, prefabs, ui)
└───GameAPI (Backend Server — Teammate Scope)
    └───Controllers, Data, DTOs, Migrations, Models
```

</details>

---

### Technical Challenges & Solutions
```yaml
Challenge     : Keeping the OpenGL rendering and gameplay loop responsive while syncing state with a web API
Solution      : Engineered a decoupled C++ core loop & ECS layer isolated from the Integration/ network module
Result        : Clean separation of concerns between graphics/gameplay execution and external API communication
```

---

### Links & Media
<pre>
Full Video     : <a href="https://youtu.be/LINK_VIDEO_SHOOTER">https://youtu.be/LINK_VIDEO_SHOOTER</a>
Playable Build : -
</pre>

<br>

[← cd ~/portfolio](../../README.md)
