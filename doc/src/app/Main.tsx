'use client'

import { useEffect } from 'react'
import { Header } from './Header'
import { Provider } from './Provider'
import { View } from '@adobe/react-spectrum'

interface MainProps {
  children: React.ReactNode
}

export function Main(props: MainProps) {
  useEffect(() => {
    const scrollbar = window.innerWidth - document.documentElement.clientWidth + 'px';
    document.documentElement.style.setProperty('--scrollbar', scrollbar);
  }, [])

  return (
    <Provider>
      <View minHeight="100vh">
        <View maxWidth="1200px" margin="0 auto">
          <Header />
        </View>
        {props.children}
      </View>
    </Provider>
  )
}
