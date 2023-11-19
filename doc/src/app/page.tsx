'use client'

import { Flex, Heading, View, Grid } from "@adobe/react-spectrum";
import { Highlight } from "./Highlight";
import { Open_Sans } from 'next/font/google'

const open_sans = Open_Sans({weight: "300", subsets: ['latin']})

export default function Home() {
  const sample_code = `\
import grance

app = grance.Grance()

@app.query("hello")
def hello() -> str:
    return "world"

print(app.execute("{ hello }"))
`

  return (
    <Flex direction="column" gap="size-500">
      <View>
        <Highlight>
          <Flex direction="column" justifyContent="center" alignItems="center" flexGrow={1}>
            <View height="7rem"></View>
            <Flex direction="row" justifyContent="center" alignItems="center" gap="size-1000">
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
            <pre style={{marginTop: "2rem", fontSize: "1.5rem"}}>pip install grance</pre>
          </Flex>
        </Highlight>
      </View>
      <Grid
        columns={['1fr', '1fr']}
        width="100%"
      >
        <View>
          <Heading level={2}>Straightfoward to <strong>Define</strong> GraphQL field</Heading>
        </View>
        <View>
          <pre>{sample_code}</pre>
        </View>
      </Grid>
    </Flex>
  )
}
