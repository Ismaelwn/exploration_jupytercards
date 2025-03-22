import fs from 'node:fs/promises'
import rehypeStringify from 'rehype-stringify'
import remarkParse from 'remark-parse'
import remarkRehype from 'remark-rehype'
import {unified} from 'unified'


const document = await fs.readFile('example.md', 'utf8')

const file = await unified()
  .use(remarkParse)
  .use(remarkRehype)
  .use(rehypeStringify).process(document)

console.log(String(file))


/*
const document = await fs.readFile("test5.json", "utf-8")
const json = JSON.parse(document)


const file = await unified()
  .use(remarkRehype)
  .use(rehypeStringify)
  .processJson(json)

console.log(file)
*/