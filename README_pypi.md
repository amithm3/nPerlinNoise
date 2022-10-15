# N Perlin Noise

### A robust open source implementation of Perlin Noise Algorithm for N-Dimensions in Python.
- A _powerful_ and _fast_ API for _n-dimensional_ noise.
- Easy hyper-parameters selection of _octaves_, _lacunarity_ and _persistence_
  as well as complex and customizable hyper-parameters for n-dimension
  _frequency_, _waveLength_, _warp_(interpolation) and _range_.
- Includes various helpful tools for noise generation and for procedural generation tasks
  such as customizable _Gradient_, _Color Gradients_, _Warp_ classes.
- Implements custom _PRNG_ generator for n-dimension and can be easily tuned.

**Details**:
- **Technology stack**:
  > **Status**: **`v0.1.2-alpha9`** Packaging Trails<br>
  > **All Packages**: [releases](https://github.com/Amith225/NPerlinNoise/releases)<br>
  > **PyPI**: [](https://github.com/Amith225/NPerlinNoise/blob/master/)<br>
  > [CHANGELOG](https://github.com/Amith225/NPerlinNoise/blob/master/docs/CHANGELOG.md)<br>

**Screenshots**:
- raw
  - ![raw](https://raw.github.com/Amith225/NPerlinNoise/master/snaps/raw.png)
- wood
  - ![wood](https://raw.github.com/Amith225/NPerlinNoise/master/snaps/wood.png)
- hot nebula
  - ![hot nebula](https://raw.github.com/Amith225/NPerlinNoise/master/snaps/hot_nebula.png)
- island
  - ![island](https://raw.github.com/Amith225/NPerlinNoise/master/snaps/island.png)
- land
  - ![land](https://raw.github.com/Amith225/NPerlinNoise/master/snaps/land.png)
- marble fractal
  - ![marble fractal](https://raw.github.com/Amith225/NPerlinNoise/master/snaps/marble_fractal.png)
- patch
  - ![patch](https://raw.github.com/Amith225/NPerlinNoise/master/snaps/patch.png)
- ply1
  - ![ply1](https://raw.github.com/Amith225/NPerlinNoise/master/snaps/ply1.png)
- ply2
  - ![ply2](https://raw.github.com/Amith225/NPerlinNoise/master/snaps/ply2.png)
- stripes
  - ![stripes](https://raw.github.com/Amith225/NPerlinNoise/master/snaps/stripes.png)
- warp
  - ![warp](https://raw.github.com/Amith225/NPerlinNoise/master/snaps/warp.png)

---

## Dependencies
- `Python>=3.10.0`

for production dependencies see [Requirements](https://raw.github.com/Amith225/NPerlinNoise/master/requirements.txt)<br>
for development dependencies see [Dev-Requirements](https://raw.github.com/Amith225/NPerlinNoise/master/requirements_dev.txt)

## Installation
for detailed instruction on installation see [INSTALLATION](https://github.com/Amith225/NPerlinNoise/blob/master/docs/INSTALL.md).

<a id="usage"></a>
## Usage
for detailed usage see [EXAMPLE](https://github.com/Amith225/NPerlinNoise/blob/master/tests/main.py)

## How to test the software
- To test overalls run [main](https://github.com/Amith225/NPerlinNoise/blob/master/tests/main.py)
- To test Logical consistency run [testLogic](https://github.com/Amith225/NPerlinNoise/blob/master/tests/testLogic.py)
- To test Profile Benchmarking run [testProfile](https://github.com/Amith225/NPerlinNoise/blob/master/tests/testProfile.py)
- To test Visuals run [testVisuals](https://github.com/Amith225/NPerlinNoise/blob/master/tests/testVisuals.py)
- To test Colors run [testCol](https://github.com/Amith225/NPerlinNoise/blob/master/tests/testCol.py)

to see all tests see [Tests](https://github.com/Amith225/NPerlinNoise/blob/master/tests)

## Known issues
- **_`No Known Bugs`_**
- **_`NPerlin.findBounds is bottleneck`_**

## Getting help
- Check [main.py](https://github.com/Amith225/NPerlinNoise/blob/master/tests/main.py) for detailed usage
- Check [docs](https://github.com/Amith225/NPerlinNoise/blob/master/docs) for all documentations
- Check [Usage](#usage) Section

If you have questions, concerns, bug reports, etc,
please file an [issue](https://github.com/Amith225/NPerlinNoise/issues) in this repository's Issue Tracker or
open a [discussion](https://github.com/Amith225/NPerlinNoise/discussions/7) in this repository's Discussion section.


## Getting involved
- `Looking for Contributors for WebApps`
- [Fork](https://github.com/Amith225/NPerlinNoise/fork) the repository
  and issue a [PR](https://github.com/Amith225/NPerlinNoise/pulls) to contribute

General instructions on _how_ to contribute  [CONTRIBUTING](https://github.com/Amith225/NPerlinNoise/blob/master/docs/CONTRIBUTING.md).

----

## Open source licensing info
1. [TERMS](https://github.com/Amith225/NPerlinNoise/blob/master/docs/TERMS.md)
2. [LICENSE](https://github.com/Amith225/NPerlinNoise/blob/master/LICENSE)
3. [CFPB Source Code Policy](https://github.com/cfpb/source-code-policy/)

----

## Credits and references
1. Inspired from [The Coding Train](https://www.youtube.com/channel/UCvjgXvBlbQiydffZU7m1_aw) -> [perlin noise](https://thecodingtrain.com/challenges/24-perlin-noise-flow-field)
2. hash function by [xxhash](https://github.com/Cyan4973/xxHash)
   inspired the [rand3](https://github.com/Amith225/NPerlinNoise/blob/master/src/NPerlinNoise/tools.py) algo
   and ultimately helped for O(1) time complexity n-dimensional random generator [NPrng](https://github.com/Amith225/NPerlinNoise/blob/master/src/NPerlinNoise/tools.py)
3. [StackOverflow](https://stackoverflow.com/) for helping on various occasions throughout the development
