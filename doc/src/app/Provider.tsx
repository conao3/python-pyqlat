'use client'

import { Provider as RSProvider, darkTheme } from "@adobe/react-spectrum"

interface ProviderProps {
  children: React.ReactNode
}

export function Provider(props: ProviderProps) {
  return (
    <RSProvider theme={darkTheme} colorScheme="dark" scale='medium'>
      {props.children}
    </RSProvider>
  )
}
