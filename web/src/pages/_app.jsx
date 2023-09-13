import Head from 'next/head'
import { slugifyWithCounter } from '@sindresorhus/slugify'

import { Layout } from '@/components/Layout'

import 'focus-visible'
import '@/styles/tailwind.css'

function getNodeText(node) {
  let text = ''
  for (let child of node.children ?? []) {
    if (typeof child === 'string') {
      text += child
    }
    text += getNodeText(child)
  }
  return text
}

function collectHeadings(nodes, slugify = slugifyWithCounter()) {
  let sections = []

  for (let node of nodes) {
    if (node.name === 'h2' || node.name === 'h3') {
      let title = getNodeText(node)
      if (title) {
        let id = slugify(title)
        node.attributes.id = id
        if (node.name === 'h3') {
          if (!sections[sections.length - 1]) {
            throw new Error(
              'Cannot add `h3` to table of contents without a preceding `h2`'
            )
          }
          sections[sections.length - 1].children.push({
            ...node.attributes,
            title,
          })
        } else {
          sections.push({ ...node.attributes, title, children: [] })
        }
      }
    }

    sections.push(...collectHeadings(node.children ?? [], slugify))
  }

  return sections
}

export default function App({ Component, pageProps }) {
  let title = pageProps.markdoc?.frontmatter.title

  let pageTitle =
    pageProps.markdoc?.frontmatter.pageTitle ||
    `${pageProps.markdoc?.frontmatter.title} - Docs`

  let description = pageProps.markdoc?.frontmatter.description

  let tableOfContents = pageProps.markdoc?.content
    ? collectHeadings(pageProps.markdoc.content)
    : []

  return (
    <>
      <Head>
        <title>{pageTitle}</title>
        {description && <meta name="description" content={description} />}
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta
          name="keywords"
          content="nPerlinNoise, perlin noise python, noise generation, procedural generation, n-dimensional noise, perlin noise algorithm, perlin noise library, generate noise, random noise generation, open source perlin noise python, procedural terrain generation with perlin noise, python noise generation, generating textures with perlin noise, game terrain perlin noise, PRNG generator, n-dimensional PRNG, gradient noise, perlin noise python, perlin noise implementation, multi-dimensional perlin noise, generative art perlin noise, procedural content generation, open source noise library, texture synthesis perlin noise, simplex noise, value noise, coherent noise, pseudorandom noise, fractal noise, spatial coherence, animate noise, warp noise, smooth noise, seamless noise, tileable noise, octaves noise, fractal brownian motion, diamond-square algorithm, ocean waves noise, lava texture noise,wood texture noise,marble texture noise,colormap noise,gradient map noise,flow noise,curl noise,divergence noise,vector noise,scalar noise,gradient descent noise,cellular noise,worley noise,radial basis functions,noise periods,anisotropic noise,isotropic noise,heterogeneous noise,homogeneous noise,stationary noise,non-stationary noise,ergodic noise,non-ergodic noise,stochastic noise,deterministic noise,band-limited noise,blue noise,pink noise,brown noise,white noise,gaussian noise,poisson noise,uniform noise,sparse noise,dense noise,point noise,solid noise,gas noise,plasma noise,fluid noise,fractal noise dimension"
        />
        <meta name="author" content="Amith M" />
      </Head>
      <Layout title={title} tableOfContents={tableOfContents}>
        <Component {...pageProps} />
      </Layout>
    </>
  )
}
