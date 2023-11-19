import { Flex, View } from "@adobe/react-spectrum";
import Link from "next/link";

export function Header() {
  return (
    <Flex gap="size-200" minHeight="size-600">
      <Link href="/">
        <View>
          Grance
        </View>
      </Link>
      <Link href="/docs">
        <View>
          docs
        </View>
      </Link>
    </Flex>
  )
}
