'use client'

import { Flex, Heading, View, Text, Grid } from "@adobe/react-spectrum";
import { Header } from "./Header";
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
    <Flex direction="column" minHeight="100vh" gap="size-500">
      <Highlight>
        <Flex direction="column" maxWidth="1200px" margin="0 auto" height="100%">
          <div style={{position: 'relative'}}>
            <div style={{position: 'absolute'}}>
              <Header />
            </div>
          </div>
          <Flex direction="column" justifyContent="center" alignItems="center" flexGrow={1}>
            <View height="5rem"></View>
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
        </Flex>
      </Highlight>
      <Flex direction="column" width="100%" maxWidth="1200px" margin="0 auto">
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
    </Flex>
  )
}
