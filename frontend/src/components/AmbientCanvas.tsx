import { useRef, useMemo } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import * as THREE from 'three'

const COUNT = 45

function DustMotes() {
  const mesh = useRef<THREE.Points>(null)

  const { positions, speeds, drift } = useMemo(() => {
    const positions = new Float32Array(COUNT * 3)
    const speeds    = new Float32Array(COUNT)
    const drift     = new Float32Array(COUNT)
    for (let i = 0; i < COUNT; i++) {
      positions[i * 3]     = (Math.random() - 0.5) * 22
      positions[i * 3 + 1] = (Math.random() - 0.5) * 14
      positions[i * 3 + 2] = (Math.random() - 0.5) * 6
      speeds[i] = 0.0008 + Math.random() * 0.0018   // very slow
      drift[i]  = (Math.random() - 0.5) * 0.0006    // gentle horizontal sway
    }
    return { positions, speeds, drift }
  }, [])

  useFrame(({ clock }) => {
    if (!mesh.current) return
    const pos = mesh.current.geometry.attributes.position.array as Float32Array
    const t = clock.elapsedTime
    for (let i = 0; i < COUNT; i++) {
      pos[i * 3 + 1] += speeds[i]
      pos[i * 3]     += Math.sin(t * 0.3 + i) * 0.0003 + drift[i]
      if (pos[i * 3 + 1] > 7) {
        pos[i * 3 + 1] = -7
        pos[i * 3]     = (Math.random() - 0.5) * 22
      }
    }
    mesh.current.geometry.attributes.position.needsUpdate = true
  })

  return (
    <points ref={mesh}>
      <bufferGeometry>
        <bufferAttribute attach="attributes-position" args={[positions, 3]} />
      </bufferGeometry>
      {/* Terracotta dust — warm and earthy */}
      <pointsMaterial size={0.05} color="#c4623a" transparent opacity={0.22} sizeAttenuation />
    </points>
  )
}

function SageOrbs() {
  const mesh = useRef<THREE.Points>(null)
  const ORB_COUNT = 18

  const positions = useMemo(() => {
    const arr = new Float32Array(ORB_COUNT * 3)
    for (let i = 0; i < ORB_COUNT; i++) {
      arr[i * 3]     = (Math.random() - 0.5) * 20
      arr[i * 3 + 1] = (Math.random() - 0.5) * 12
      arr[i * 3 + 2] = (Math.random() - 0.5) * 4
    }
    return arr
  }, [])

  useFrame(({ clock }) => {
    if (!mesh.current) return
    // Very slow breathing rotation
    mesh.current.rotation.z = Math.sin(clock.elapsedTime * 0.04) * 0.06
    mesh.current.rotation.x = Math.cos(clock.elapsedTime * 0.03) * 0.03
  })

  return (
    <points ref={mesh}>
      <bufferGeometry>
        <bufferAttribute attach="attributes-position" args={[positions, 3]} />
      </bufferGeometry>
      {/* Sage green orbs — contemplative, slow */}
      <pointsMaterial size={0.12} color="#5f7a6b" transparent opacity={0.18} sizeAttenuation />
    </points>
  )
}

export default function AmbientCanvas() {
  return (
    <div style={{ position: 'fixed', inset: 0, zIndex: 0, pointerEvents: 'none' }}>
      <Canvas
        camera={{ position: [0, 0, 8], fov: 60 }}
        style={{ background: 'transparent' }}
        gl={{ alpha: true, antialias: false }}
      >
        <DustMotes />
        <SageOrbs />
      </Canvas>
    </div>
  )
}
