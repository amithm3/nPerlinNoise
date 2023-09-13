---
title: Getting started
pageTitle: nPerlinNoise - A robust open source implementation of Perlin Noise Algorithm for N-Dimensions.
description: A robust open source implementation of Perlin Noise Algorithm for N-Dimensions.
---

Learn how to use nPerlinNoise {% .lead %}

- A _powerful_ and _fast_ API for _n-dimensional_ noise.
- Easy hyper-parameters selection of _octaves_, _lacunarity_ and _persistence_
  as well as complex and customizable hyper-parameters for n-dimension
  _frequency_, _waveLength_, _warp_(interpolation) and _range_.
- Includes various helpful tools for noise generation and for procedural generation tasks
  such as customizable _Gradient_, _Color Gradients_, _Warp_ classes.
- Implements custom _PRNG_ generator for n-dimension and can be easily tuned.

## Details

- **Technology stack**:
  - **Status**: `v0.1.4-alpha` focusing on all issues [Getting Involved](#open-source-licensing-info), follows PEP440
  - **All Packages**: [Releases](https://github.com/Amith225/nPerlinNoise/releases)
  - [CHANGELOG](changelog)
  
Tested on Python 3.10, Windows 10

- **Future work**:
  - **Optimization** for octave noise
  - Writing **unit tests**
  - Writing **API docs**
  - Writing **pending docs**
  - Writing **ReadTheDocs**
  - **Blogging**
  - Finishing left **in-code docs**
  - Dimensional **octaves**

---

## Screenshots

![example2](https://user-images.githubusercontent.com/75326634/196452679-7bcf8b50-357d-409f-9485-8b9fdffd86f0.gif)

Link to [Gallery](snaps)

---

## Quick Start

If you're eager to get started with nPerlinNoise, follow these simple steps to set up and start using the library:

## Dependencies

- `Python>=3.10.0`

For production dependencies

- `numexpr>=2.8.3`
- `numpy>=1.23.3`

For development dependencies

- `matplotlib>=3.6.1`
- `plotly>=5.10.0`
- `PyQt5>=5.15.7`
- `PyQt5-stubs>=5.15.6.0`
- `build>=0.8.0`
- `twine>=4.0.1`

## Installation

Begin by installing nPerlinNoise using pip. Open your terminal or command prompt and run the following command:

```shell
pip install nPerlinNoise
```

For detailed instructions on installation, see [Installation](#installation).

### Setup

**Import nPerlinNoise**: In your Python script or interactive session, import nPerlinNoise as follows:

   ```python
   import nPerlinNoise as nPN
   ```

**Create a Noise Instance**: Next, create a `Noise` instance, specifying any desired parameters. For example:

   ```python
   noise = nPN.Noise(seed=69420)
   ```

### Basic Usage

You're now ready to generate Perlin noise! You can use the `noise` instance to obtain noise values at specific n-dimensional coordinates. Here are some basic usage examples:

- #### Single Value

  - `noise(..., l, m, n, ...)`
  
    ```python
    >>> noise(73)
    array(0.5207113, dtype=float32)
    >>> noise(73, 11, 7)
    array(0.5700986, dtype=float32)
    >>> noise(0, 73, 7, 11, 0, 3)
    array(0.5222712, dtype=float32)
    ```

- #### Iterable

  - `noise(...., [l1, l2, ..., lx], [m1, m2, ..., mx], [n1, n2, ..., nx], ....)`
  
    ```python
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

  `noise(..., l, m, n, ...)` has the same values with trailing dimensions having zero as coordinates.

- #### n-Dimensionality

  `noise(..., l, m, n)` is equivalent to `noise(..., l, m, n, 0)` and so on.

  ```python
  >>> noise(73)
  array(0.5207113, dtype=float32)
  >>> noise(73, 0)
  array(0.5207113, dtype=float32)
  >>> noise(73, 0, 0)
  array(0.5207113, dtype=float32)
  >>> noise(73, 0, 0, 0, 0)
  array(0.5207113, dtype=float32)
  ```

Grid mode allows for computing noise for every combination of coordinates.
Use `noise(..., gridMode=True)`; `gridMode` is a keyword-only argument, default is `False`.
The output will be of the same shape as the length(s) of coordinates in that order.

- #### Grid Mode

  ```python
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

For detailed usage, see [Example](https://github.com/amithm3/nPerlinNoise/blob/master/scripts/main.py).

## How to Test the Software

- To test Logical consistency, run [testLogic](https://github.com/amithm3/nPerlinNoise/blob/master/tests/testLogic.py)
- To test Profile Benchmarking, run [testProfile](https://github.com/amithm3/nPerlinNoise/blob/master/tests/testProfile.py)
- To test Visuals, run [testVisuals](https://github.com/amithm3/nPerlinNoise/blob/master/tests/testVisuals.py)
- To test Colors, run [testCol](https://github.com/amithm3/nPerlinNoise/blob/master/tests/testCol.py)

To see all tests, refer to [Tests](https://github.com/amithm3/nPerlinNoise/tree/master/tests) directory.

## Known Issues

- **_No Known Bugs_**
- **_NPerlin.findBounds is bottleneck_**
- **_noise(a, b, c, d, e, f, ...) is slow for single value coordinates_**

## Getting Help

- Check [main.py](https://github.com/amithm3/nPerlinNoise/blob/master/scripts/main.py) for detailed usage
- Check [docs](https://nperlin-noise.vercel.app) for all documentations
- Check [Usage](#basic-usage) Section
- Check [Setup](#setup) for all tests

If you have questions, concerns, bug reports, etc., please file an [issue](https://github.com/Amith225/nPerlinNoise/issues) in this repository's Issue Tracker or open a [discussion](https://github.com/Amith225/nPerlinNoise/discussions/7) in this repository's Discussion section.

## Getting involved

- `Looking for Contributors for feature additions`
- `Looking for Contributors for optimization` [#11](https://github.com/Amith225/nPerlinNoise/issues/11)
- `Looking for Contributors for unit testing` [#12](https://github.com/Amith225/nPerlinNoise/issues/12)
- `Looking for Contributors for ReadTheDocs` [#13](https://github.com/Amith225/nPerlinNoise/issues/13)
- `Looking for Contributors for WebApp` [#14](https://github.com/Amith225/nPerlinNoise/issues/14)
- `Looking for Contributors for API docs` [#15](https://github.com/Amith225/nPerlinNoise/issues/15)
- [Fork](https://github.com/Amith225/nPerlinNoise/fork) the repository
  and issue a [PR](https://github.com/Amith225/nPerlinNoise/pulls) to contribute

General instructions on how to contribute [CONTRIBUTING](#getting-involved)
and [CODE OF CONDUCT](coc)

## Open source licensing info

1. [Terms](terms)
2. [LICENSE](license)
3. [CFPB Source Code Policy](https://github.com/cfpb/source-code-policy/)

## Credits and references

1. Inspired from [The Coding Train](https://www.youtube.com/channel/UCvjgXvBlbQiydffZU7m1_aw)
   -> [perlin noise](https://thecodingtrain.com/challenges/24-perlin-noise-flow-field)
2. hash function by [xxhash](https://github.com/Cyan4973/xxHash)
   inspired the [rand3](src/nPerlinNoise/tools.py) algo
   and ultimately helped for O(1) time complexity n-dimensional random generator [NPrng](src/nPerlinNoise/tools.py)
3. [StackOverflow](https://stackoverflow.com/) for helping on various occasions throughout the development
4. [vnoise](https://github.com/plottertools/vnoise) and [opensimplex](https://github.com/lmas/opensimplex)
   for ideas for README.md
5. docs derivative from [open-source-project-template](https://github.com/cfpb/open-source-project-template)
6. packaging help from [realpython](https://realpython.com/pypi-publish-python-package/)

## Project Badges

[![LICENSE](https://img.shields.io/github/license/Amith225/NPerlinNoise)](licience)
[![GitHub last commit](https://img.shields.io/github/last-commit/Amith225/NPerlinNoise?label=GitHub)](https://github.com/Amith225/nPerlinNoise)
[![PyPI](https://img.shields.io/pypi/v/NPerlinNoise)](https://pypi.org/project/nPerlinNoise)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/Amith225/NPerlinNoise)](https://github.com/Amith225/nPerlinNoise/releases/latest)
[![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/Amith225/NPerlinNoise?include_prereleases)](https://github.com/Amith225/nPerlinNoise/releases)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nPerlinNoise)]("https://www.python.org/downloads/)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/nPerlinNoise)
