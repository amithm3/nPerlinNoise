<a href="https://github.com/Amith225/nPerlinNoise/blob/master/LICENSE">![LICENSE](https://img.shields.io/github/license/Amith225/NPerlinNoise)</a>
<a href="https://github.com/Amith225/nPerlinNoise">![GitHub last commit](https://img.shields.io/github/last-commit/Amith225/NPerlinNoise?label=GitHub)</a>
<a href="https://pypi.org/project/nPerlinNoise">![PyPI](https://img.shields.io/pypi/v/NPerlinNoise)</a>
<a href="https://github.com/Amith225/nPerlinNoise/releases/latest">![GitHub release (latest by date)](https://img.shields.io/github/v/release/Amith225/NPerlinNoise)</a>
<a href="https://github.com/Amith225/nPerlinNoise/releases">![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/Amith225/NPerlinNoise?include_prereleases)</a>
<a href="https://www.python.org/downloads/">![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nPerlinNoise)</a>
<a href="#">![PyPI - Wheel](https://img.shields.io/pypi/wheel/nPerlinNoise)</a>

[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/open-source.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/contains-tasty-spaghetti-code.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/powered-by-coffee.svg)](https://forthebadge.com)

# nPerlinNoise

#### indexed on PyPI - [nPerlinNoise](https://pypi.org/project/nPerlinNoise)

#### repo on GitHub - [nPerlinNoise](https://github.com/Amith225/nPerlinNoise)

#### docs on ReadTheDocs - [](https://readthedocs.org/)

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
  > **Status**: **`v0.1.4-alpha`** focusing on all issues [Getting Involved](https://github.com/Amith225/nPerlinNoise/blob/master/#contribute), follows PEP440<br>
  > **All Packages**: [releases](https://github.com/Amith225/nPerlinNoise/releases)<br>
  > [CHANGELOG](https://github.com/Amith225/nPerlinNoise/blob/master/docs/CHANGELOG.md)<br>
  > ###### _Tested on Python 3.10, Windows 10_
- **Future work**:
  > **optimization** for octave noise<br>
  > writing **unit tests**<br>
  > writing **API docs**<br>
  > writing **pending docs**<br>
  > writing **ReadTheDocs**<br>
  > **blogging**<br>
  > finishing left **in-code docs**<br>
  > dimensional **octaves**<br>

---

**Screenshots**:

<div align="center">

![](https://raw.github.com/Amith225/nPerlinNoise/master/snaps/img_587383161.png)
![](https://raw.github.com/Amith225/nPerlinNoise/master/snaps/img_1410614909.png)
![](https://raw.github.com/Amith225/nPerlinNoise/master/snaps/img_1742083597.png)
![](https://raw.github.com/Amith225/nPerlinNoise/master/snaps/img_2580891136.png)
![](https://raw.github.com/Amith225/nPerlinNoise/master/snaps/img_3001325707.png)
![](https://raw.github.com/Amith225/nPerlinNoise/master/snaps/img_3403505649.png)
![](https://raw.github.com/Amith225/nPerlinNoise/master/snaps/img_4183221855.png)
![](https://raw.github.com/Amith225/nPerlinNoise/master/snaps/img_4237425687.png)
![](https://raw.github.com/Amith225/nPerlinNoise/master/snaps/img_4246716738.png)

</div>

---

## Dependencies

- `Python>=3.10.0`

for production dependencies see [Requirements](https://raw.github.com/Amith225/nPerlinNoise/master/requirements/requirements.txt)<br>
for development dependencies see [Dev-Requirements](https://raw.github.com/Amith225/nPerlinNoise/master/requirements/dev_requirements.txt)

## Installation

```shell
$ pip install nPerlinNoise
```

for detailed instruction on installation see [INSTALLATION](https://github.com/Amith225/nPerlinNoise/blob/master/docs/INSTALL.md).

<a id="usage"></a>

## Usage

**Setup**

```pycon
>>> import nPerlinNoise as nPN
>>> noise = nPN.Noise(seed=69420)
```

**Basic usage**

Get noise values at given n-dimensional coordinates by calling ```noise(...)```,<br>
coordinates can be single value, or an iterable

- ###### single value

  > noise(..., l, m, n, ...)<br>
  > where l, m, n, ..., are single values

    ```pycon
    >>> noise(73)
    array(0.5207113, dtype=float32)
    >>> noise(73, 11, 7)
    array(0.5700986, dtype=float32)
    >>> noise(0, 73, 7, 11, 0, 3)
    array(0.5222712, dtype=float32)
    ```

- ###### iterable

  > noise(...., [l1, l2, ..., lx], [m1, m2, ..., mx], [n1, n2, ..., nx], ....)<br>
  > where ...., are iterable of homogeneous-dimensions and lx, mx, nx, ..., are single values
  > the output will be of same shape of input homogeneous-dimensions

  ```pycon
  >>> noise([73, 49])
  array([0.52071124, 0.6402224 ], dtype=float32)
  >>> noise([73, 49], [2, 2])
  array([0.4563121 , 0.63378346], dtype=float32)
  >>> noise([[73], [49], [0]],
  ...       [[2 ], [2 ], [2]],
  ...       [[0 ], [1 ], [2]])
  array([[0.4563121 ],
         [0.6571784 ],
         [0.16369209]], dtype=float32)
  >>> noise([[1, 2], [2, 3]],
  ...       [[1, 1], [1, 1]],
  ...       [[2, 2], [2, 2]])
  array([[0.08666219, 0.09778494],
         [0.09778494, 0.14886124]], dtype=float32)
  ```

`noise(..., l, m, n, ...)` has same values with trailing dimensions having zero as coordinate

- ###### n-dimensionality

  > noise(..., l, m, n) = noise(..., l, m, n, 0) = noise(..., l, m, n, 0, 0) = noise(..., l, m, n, 0, 0, ...)

  ```pycon
  >>> noise(73)
  array(0.5207113, dtype=float32)
  >>> noise(73, 0)
  array(0.5207113, dtype=float32)
  >>> noise(73, 0, 0)
  array(0.5207113, dtype=float32)
  >>> noise(73, 0, 0, 0, 0)
  array(0.5207113, dtype=float32)
  ```

grid mode allows for computing noise for every combination of coords<br>
use `noise(..., gridMode=True)` gridMode is key-word only argument, default=False<br>
the output will be of shape equal to the length(s) of coords in that order

- ###### gridMode
  ```pycon
  >>> noise([73, 49], [2, 2], [0, 1], gridMode=True)
  array([[[0.4563121 , 0.63378346],
          [0.4563121 , 0.63378346]],
  
         [[0.44594935, 0.6571784 ],
          [0.44594935, 0.6571784 ]]], dtype=float32)
  >>> noise([1, 20, 32, 64], [1, 1, 2], 0, [1, 2], gridMode=True)
  array([[[[0.06459193, 0.5110498 , 0.669962  , 0.47636804],
           [0.06459193, 0.5110498 , 0.669962  , 0.47636804],
           [0.09864856, 0.5013973 , 0.62935597, 0.47954425]]],
  
  
         [[[0.07678645, 0.50853723, 0.6778991 , 0.4679888 ],
           [0.07678645, 0.50853723, 0.6778991 , 0.4679888 ],
           [0.14069612, 0.47582665, 0.6663638 , 0.48764956]]]],
        dtype=float32)
  ```

for detailed usage see [EXAMPLE](https://github.com/Amith225/nPerlinNoise/blob/master/scripts/main.py)

## API

- docs pending

## How to test the software

- To test Logical consistency run [testLogic](https://github.com/Amith225/nPerlinNoise/blob/master/tests/testLogic.py)
- To test Profile Benchmarking run [testProfile](https://github.com/Amith225/nPerlinNoise/blob/master/tests/testProfile.py)
- To test Visuals run [testVisuals](https://github.com/Amith225/nPerlinNoise/blob/master/tests/testVisuals.py)
- To test Colors run [testCol](https://github.com/Amith225/nPerlinNoise/blob/master/tests/testCol.py)

to see all tests see [Tests](https://github.com/Amith225/nPerlinNoise/blob/master/tests)

## Known issues

- **_`No Known Bugs`_**
- **_`NPerlin.findBounds is bottleneck`_**
- **_`noise(a, b, c, d, e, f, ...) is slow for single value coordinates`_**

## Getting help

- Check [main.py](https://github.com/Amith225/nPerlinNoise/blob/master/scripts/main.py) for detailed usage
- Check [docs](https://github.com/Amith225/nPerlinNoise/blob/master/docs) for all documentations
- Check [Usage](#usage) Section

If you have questions, concerns, bug reports, etc.
please file an [issue](https://github.com/Amith225/nPerlinNoise/issues) in this repository's Issue Tracker or
open a [discussion](https://github.com/Amith225/nPerlinNoise/discussions/7) in this repository's Discussion section.

## Getting involved

<a id="contribute"></a>
- `Looking for Contributors for feature additions`
- `Looking for Contributors for optimization` [#11](https://github.com/Amith225/nPerlinNoise/issues/11)
- `Looking for Contributors for unit testing` [#12](https://github.com/Amith225/nPerlinNoise/issues/12)
- `Looking for Contributors for ReadTheDocs` [#13](https://github.com/Amith225/nPerlinNoise/issues/13)
- `Looking for Contributors for WebApp` [#14](https://github.com/Amith225/nPerlinNoise/issues/14) 
- `Looking for Contributors for API docs` [#15](https://github.com/Amith225/nPerlinNoise/issues/15) 
- [Fork](https://github.com/Amith225/nPerlinNoise/fork) the repository
  and issue a [PR](https://github.com/Amith225/nPerlinNoise/pulls) to contribute

General instructions on _how_ to contribute [CONTRIBUTING](https://github.com/Amith225/nPerlinNoise/blob/master/docs/CONTRIBUTING.md)
and [CODE OF CONDUCT](https://github.com/Amith225/nPerlinNoise/blob/master/CODE_OF_CONDUCT.md)

----

## Open source licensing info

1. [TERMS](https://github.com/Amith225/nPerlinNoise/blob/master/docs/TERMS.md)
2. [LICENSE](https://github.com/Amith225/nPerlinNoise/blob/master/LICENSE)
3. [CFPB Source Code Policy](https://github.com/cfpb/source-code-policy/)

----

## Credits and references

1. Inspired from [The Coding Train](https://www.youtube.com/channel/UCvjgXvBlbQiydffZU7m1_aw)
   -> [perlin noise](https://thecodingtrain.com/challenges/24-perlin-noise-flow-field)
2. hash function by [xxhash](https://github.com/Cyan4973/xxHash)
   inspired the [rand3](https://github.com/Amith225/nPerlinNoise/blob/master/src/nPerlinNoise/tools.py) algo
   and ultimately helped for O(1) time complexity n-dimensional random generator [NPrng](https://github.com/Amith225/nPerlinNoise/blob/master/src/nPerlinNoise/tools.py)
3. [StackOverflow](https://stackoverflow.com/) for helping on various occasions throughout the development
4. [vnoise](https://github.com/plottertools/vnoise) and [opensimplex](https://github.com/lmas/opensimplex)
   for ideas for README.md
5. docs derivative from [open-source-project-template](https://github.com/cfpb/open-source-project-template)
6. packaging help from [realpython](https://realpython.com/pypi-publish-python-package/)

**Maintainer**:

|        <a href="https://github.com/Amith225"><img src="https://avatars.githubusercontent.com/u/75326634?v=4" height=250></a>        |
|:-----------------------------------------------------------------------------------------------------------------------------------:|
|                                    **[Amith M](https://www.linkedin.com/in/amith-m-17088b246/)**                                    |
| [![Instagram](https://img.shields.io/badge/Instagram-%23E4405F.svg?logo=Instagram&logoColor=white)](https://instagram.com/amithm3 ) |
