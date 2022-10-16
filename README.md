![GitHub](https://img.shields.io/github/license/Amith225/NPerlinNoise)
![PyPI](https://img.shields.io/pypi/v/NPerlinNoise)
![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/Amith225/NPerlinNoise)
![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/Amith225/NPerlinNoise?include_prereleases)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/NPerlinNoise)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/NPerlinNoise)

# N Perlin Noise

## active dev @[v0.1.3-alpha_dev](https://github.com/Amith225/nPerlinNoise/tree/v0.1.3-alpha_dev)

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
  > **Status**: **`v0.1.3-alpha`** Ready for public PyPI release<br>
  > **All Packages**: [releases](https://github.com/Amith225/NPerlinNoise/releases)<br>
  > **PyPI**: [v0.1.3a0](https://pypi.org/project/NPerlinNoise/0.1.3a0/)<br>
  > [CHANGELOG](docs/CHANGELOG.md)<br>

**Screenshots**:
- raw<br>
  ![raw](snaps/raw.png)
- wood<br>
  ![wood](snaps/wood.png)
- hot nebula<br>
  ![hot nebula](snaps/hot_nebula.png)
- island<br>
  ![island](snaps/island.png)
- land<br>
  ![land](snaps/land.png)
- marble fractal<br>
  ![marble fractal](snaps/marble_fractal.png)
- patch<br>
  ![patch](snaps/patch.png)
- color patch<br>
  ![color patch](snaps/color_patch.png)
- ply1<br>
  ![ply1](snaps/ply1.png)
- ply2<br>
  ![ply2](snaps/ply2.png)
- stripes<br>
  ![stripes](snaps/stripes.png)
- warp<br>
  ![warp](snaps/warp.png)

---

## Dependencies
- `Python>=3.10.0`

for production dependencies see [Requirements](requirements.txt)<br>
for development dependencies see [Dev-Requirements](requirements_dev.txt)

## Installation
for detailed instruction on installation see [INSTALLATION](docs/INSTALL.md).

<a id="usage"></a>
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
- `Looking for Contributors for WebApps`
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
