'use client'

import MdxContent from './source.mdx'

import 'prismjs/themes/prism-tomorrow.css';
import 'prismjs/plugins/line-numbers/prism-line-numbers.css'
import 'prismjs/plugins/treeview/prism-treeview.js'
import 'prismjs/plugins/treeview/prism-treeview.css'

export default function Docs() {
  return (
    <article>
      <MdxContent />
    </article>
  )
}
