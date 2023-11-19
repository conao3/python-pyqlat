'use client'

import { Flex, Heading, View, Text } from "@adobe/react-spectrum";
import { Header } from "./Header";
import { Highlight } from "./Highlight";
import { Open_Sans } from 'next/font/google'

const open_sans = Open_Sans({weight: "300", subsets: ['latin']})

export default function Home() {
  return (
    <Flex direction="column" minHeight="100vh">
      <Highlight>
        <Flex direction="column" maxWidth="1200px" margin="0 auto" height="100%">
          <div style={{position: 'relative'}}>
            <div style={{position: 'absolute'}}>
              <Header />
            </div>
          </div>
          <Flex justifyContent="center" alignItems="center" flexGrow={1} gap="size-1000">
            <View>
              <Heading level={1} UNSAFE_style={{fontSize: "5rem"}}>
                <div className={open_sans.className}>Grance</div>
              </Heading>
            </View>
            <View>
              <Heading level={2} UNSAFE_style={{fontSize: "3rem"}}>
                <div className={open_sans.className}>
                  A Brand<br />
                  New GraphQL Library<br />
                  Based on Pydantic
                </div>
              </Heading>
            </View>
          </Flex>
        </Flex>
      </Highlight>
      <Flex direction="column" maxWidth="1200px" margin="0 auto">
        a
      </Flex>
    </Flex>
  )
}
