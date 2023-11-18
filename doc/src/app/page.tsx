'use client'

import { Flex, Heading, View } from "@adobe/react-spectrum";
import { Header } from "./Header";

export default function Home() {
  return (
    <View minHeight="100vh" paddingTop="size-200">
      <Flex direction="column" maxWidth="1000px" margin="0 auto">
        <Header />
        <Heading level={1} UNSAFE_style={{fontSize: "3em", textAlign: "center"}}>
          A Brand New GraphQL Library Based on Pydantic
        </Heading>
      </Flex>
    </View>
  )
}
