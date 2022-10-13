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
- **Status**: [v0.1.0@alpha](https://github.com/Amith225/NPerlinNoise/releases/tag/v0.1.0%40alpha), in documentation and bug fixes stage [CHANGELOG](docs/CHANGELOG.md).
- **[Links]()**
- **Additional Description**

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
- Python~=3.10.0
- [Requirements](requirements.txt)

## Installation
- [INSTALLATION](docs/INSTALL.md) document.

## Usage
- [EXAMPLE](main.py)
- Noise functions
  - >**NPerlin**(<br>
      seed: int = None,<br>
      frequency: Union[int, tuple[int, ...]] = 8,<br>
      waveLength: Union[float, tuple[float]] = 128,<br>
      warp: Union['Warp', tuple['Warp']] = None,<br>
      _range: tuple[float, float] = None<br>
    )
  - >**Noise**(<br>
      seed: int = None,<br>
      frequency: frequencyHint = 8,<br>
      waveLength: waveLengthHint = 128,<br>
      warp: warpHint = None,<br>
      _range: rangeHint = None,<br>
      octaves: int = 8,<br>
      persistence: float = 0.5,<br>
      lacunarity: float = 2<br>
    )
  - :param **seed**: seed for prng values, default random value
  - :param **frequency**: number of random values in one unit respect to dimension, default 8
  - :param **waveLength**: length of one unit respect to dimension, default 128
  - :param **warp**: the interpolation function used between random value nodes, default selectionTools.Warp.improved()
  - :param **_range**: bound for noise values, output will be within the give range, default (0, 1)
  - :param **fwm**: **key word only** - frequency, waveLength multiplier
  - :param **octaves**: number(s) of additive overlapping noise wave(s), default 8
  - :param **lacunarity**: frequency multiplier for successive noise octave, default 2
  - :param **persistence**: amplitude modulator for successive noise octave, default 0.5
- >**perlinGenerator**(<br>
      noise: 'NPerlin',<br>
      *lineSpace: Union[tuple[float, float, float], tuple[float, float]])<br>
)
  - generates noise values from given noise instance for given line space
  - :param **noise**: the noise instance to use for generating noise values
  - :param **lineSpace**: (start, stop) | (start, stop, resolution) for each dimension, 
    - _start_: minimum value for nth dimension coordinate 
    - _stop_: maximum value for nth dimension coordinate 
    - _resolution_: number of coordinates between start and stop (both included)
  - :return: tuple of noise values and coordinate mesh for each nth dimension of n-dimension depth

## How to test the software
- [Tests](tests)
- To test Logical consistency run [testLogic](tests/testLogic.py)
- To test Profile Benchmarking run [testProfile](tests/testProfile.py)
- To test Visuals run [testVisuals](tests/testVisuals.py)
- To test Colors run [testCol](tests/testCol.py)

## Known issues
- **_`No Known Bugs`_**
- **_`NPerlin.findBounds is bottleneck`_**

## Getting help
- Check [main.py](main.py) for usage
- Check [docs](docs)
- Check Usage Section

If you have questions, concerns, bug reports, etc, please file an [issue]() in this repository's Issue Tracker or
open a [discussion]() in this repository's Discussion section.


## Getting involved
- [Fork]() the repository and issue a [PR]() to contribute

General instructions on _how_ to contribute  [CONTRIBUTING](docs/CONTRIBUTING.md).

----

## Open source licensing info
1. [TERMS](docs/TERMS.md)
2. [LICENSE](LICENSE)
3. [CFPB Source Code Policy](https://github.com/cfpb/source-code-policy/)


----

## Credits and references
1. Projects that inspired you
2. Related projects
3. Books, papers, talks, or other sources that have meaningful impact or influence on this project
