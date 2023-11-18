'use client'

import { Provider as RSProvider, defaultTheme } from "@adobe/react-spectrum"

interface ProviderProps {
  children: React.ReactNode
}

export function Provider(props: ProviderProps) {
  return (
    <RSProvider theme={defaultTheme}>
      {props.children}
    </RSProvider>
  )
}
