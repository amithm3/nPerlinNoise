# N Perlin Noise

### A robust open source implementation of Perlin Noise Algorithm for N-Dimensions in Python.
- A powerful and fast API for n-dimensional noise.
- Easy hyper-parameters selection of octaves, lacunarity and persistence
  as well as complex and customizable hyper-parameters for n-dimension
  frequency, waveLength, warp(interpolation) and range.
- Includes various helpful tools for noise generation and for procedural generation tasks
  such as customizable Gradient, Warp classes.
- Implements custom PRNG generator for n-dimension and can be easily tuned.

**Details**:
- **Technology stack**:
  - **Status**: [v0.1.2-alpha](https://github.com/Amith225/NPerlinNoise/releases/tag/v0.1.2-alpha)
  - [CHANGELOG](docs/CHANGELOG.md)

**Screenshots**:
- raw
  - ![raw](snaps/raw.png)
- wood
  - ![wood](snaps/wood.png)
- hot nebula
  - ![hot nebula](snaps/hot_nebula.png)
- island
  - ![island](snaps/island.png)
- land
  - ![land](snaps/land.png)
- marble fractal
  - ![marble fractal](snaps/marble_fractal.png)
- patch
  - ![patch](snaps/patch.png)
- ply1
  - ![ply1](snaps/ply1.png)
- ply2
  - ![ply2](snaps/ply2.png)
- stripes
  - ![stripes](snaps/stripes.png)
- warp
  - ![warp](snaps/warp.png)

---

## Dependencies
- Python>=3.10.0

for production dependencies see [Requirements](requirements.txt)<br>
for development dependencies see [Dev-Requirements](requirements_dev.txt)

## Installation
for detailed instruction on installation see [INSTALLATION](docs/INSTALL.md).

## Usage
for detailed usage see [EXAMPLE](tests/main.py)

## How to test the software
- To test overalls run [main](tests/main.py)
- To test Logical consistency run [testLogic](tests/testLogic.py)
- To test Profile Benchmarking run [testProfile](tests/testProfile.py)
- To test Visuals run [testVisuals](tests/testVisuals.py)
- To test Colors run [testCol](tests/testCol.py)

to see all tests see [Tests](tests)

## Known issues
- **_`No Known Bugs`_**
- **_`NPerlin.findBounds is bottleneck`_**

## Getting help
- Check [main.py](tests/main.py) for detailed usage
- Check [docs](docs) for all documentations
- Check [Usage](#usage) Section

If you have questions, concerns, bug reports, etc,
please file an [issue](https://github.com/Amith225/NPerlinNoise/issues) in this repository's Issue Tracker or
open a [discussion](https://github.com/Amith225/NPerlinNoise/discussions/7) in this repository's Discussion section.


## Getting involved
- Looking for Contributors for WebApps
- [Fork](https://github.com/Amith225/NPerlinNoise/fork) the repository
  and issue a [PR](https://github.com/Amith225/NPerlinNoise/pulls) to contribute

General instructions on _how_ to contribute  [CONTRIBUTING](docs/CONTRIBUTING.md).

----

## Open source licensing info
1. [TERMS](docs/TERMS.md)
2. [LICENSE](LICENSE)
3. [CFPB Source Code Policy](https://github.com/cfpb/source-code-policy/)

----

## Credits and references
1. Inspired from [The Coding Train](https://www.youtube.com/channel/UCvjgXvBlbQiydffZU7m1_aw) -> [perlin noise](https://thecodingtrain.com/challenges/24-perlin-noise-flow-field)
2. hash function by [xxhash](https://github.com/Cyan4973/xxHash)
   inspired the [rand3](src/NPerlinNoise/tools.py) algo
   and ultimately helped for O(1) time complexity n-dimensional random generator [NPrng](src/NPerlinNoise/tools.py)
3. [StackOverflow](https://stackoverflow.com/) for helping on various occasions throughout the development
