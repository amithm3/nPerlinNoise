import Head from 'next/head'
import Image from 'next/image'
import img1 from '@/images/img(1).png'
import img2 from '@/images/img(2).png'
import img3 from '@/images/img(3).png'
import img4 from '@/images/img(4).png'
import img5 from '@/images/img(5).png'
import img6 from '@/images/img(6).png'
import img7 from '@/images/img(7).png'
import img8 from '@/images/img(8).png'
import img9 from '@/images/img(9).png'

const image = [img1, img2, img3, img4, img5, img6, img7, img8, img9]

export default function Snap() {
  return (
    <>
      <Head>
        <title>Screenshots - nPerlinNoise</title>
        <meta
          name="description"
          content="Screenshots of - A robust open source implementation of Perlin Noise Algorithm for N-Dimensions."
        />
      </Head>
      <div className="flex min-h-screen flex-col items-center justify-center py-2">
        <h1 className="text-4xl font-bold">Screenshots</h1>
        <div className="mt-4 grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
          {image.map((img, i) => (
            <Image
              key={i}
              src={img}
              alt="nPerlinNoise"
              className="h-full w-full rounded-md object-contain"
            />
          ))}
        </div>
      </div>
    </>
  )
}
