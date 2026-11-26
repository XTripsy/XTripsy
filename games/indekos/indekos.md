[← cd ~/portfolio](../README.md)

# `$ cat ~/games/indekos.md`

```yaml
Project          : Indekos
Status           : Commercial Rebuild
Context          : Professional Work (@RoleplayStudio)
Platform         : PC (Windows)
Engine           : Unity (Adventure Creator Integration)
Language         : C#
Role             : [Lead] Gameplay Systems Developer
Version Control  : Git
Timeline         : April 2024 – November 2024
```

### Visual Showcase
![Gameplay GIF Indekos](indekos-gif.gif)

```yaml
Showcase      : Narrative life-sim & adventure game re-architected for scalable quest & daily-life loops
Highlights    : Scene-per-location architecture, dynamic prefab quest spawner, custom Singleton/State framework
```

<details>
<summary><b>📸 View Screenshot Gallery (1)</b></summary>
<br>

![Screenshot Indekos 1](indekos-credits.png)

</details>

---

### Architecture & Gameplay Systems
```yaml
Core Patterns : Custom Singleton & Unified State Manager (16+ GameStates) with InputBridge & Encryption
World & Quest : Re-architected from scene-per-quest to scene-per-location + dynamic prefab quest spawning
Plugin Bridge : Seamless C# integration with Adventure Creator, NPC crowds, Day/Time cycle & SaveLoadManager
Sub-Systems   : Modular mini-game state handlers, daily activity loops & custom Unity Editor tooling
```

<details>
<summary><b>📂 Inspect Script Architecture (<code>$ tree Assets/Scripts</code>)</b></summary>

```text
├───core
│   ├───Managers (Audio, Character, Component, DateTime, Game, Input, Level, Quest, SaveLoad, Story, UI)
│   ├───additional (Encryption, TriggerManager, BaseTriggers: Action, Dialogue, Door, Input, Rest)
│   └───pattern
│       │   singleton.cs
│       ├───input (InputBridge)
│       └───state (GameState, stateinterface -> Gameplay, Cutscene, MiniGameStates, ActivityStates, NextDay, Pause)
├───editor (ComponentSaveListWindow, GranularApplyWindow, HierarchyHighlighter, PlayModeSave)
└───system
    ├───audio & loading (BGM, SFX, LoadingController)
    ├───MiniGames (Modular Rhythm & Interactive Mini-Game Controllers)
    ├───NPC & World (Crowd, NpcController, MiniMapController, DayCycleController)
    ├───Quest (Quest, QuestController, questcontrollerinterface, UiQuestSystem)
    └───UI (ButtonHover, UIBindSystem)
```

</details>

---

### Technical Challenges & Solutions
```yaml
Challenge     : Severe performance bottlenecks and bloat caused by the legacy 'scene-per-quest' structure
Solution      : Re-architected into a 'scene-per-location' model with dynamic script-driven prefab/quest spawning
Result        : Eliminated scene-loading spikes, unified single-player state flow, and streamlined team workflow
```

---

### Links & Media
<pre>
Steam Page     : <a href="https://store.steampowered.com/app/3161550/Indekos/">Steam Store (Indekos)</a>
Full Video     : -
</pre>

<br>

[← cd ~/portfolio](../README.md)
