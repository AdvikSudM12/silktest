import * as fs from 'fs'
import { pathResolver } from '../configs/path-resolver'

export const generateJSONBuckup = ({
  fileName = null,
  data
}: {
  fileName?: string | null
  data: any
}) => {
  const filePath = pathResolver.getResultsFilePath(`backups/${fileName}.json`)

  try {
    const stream = fs.createWriteStream(filePath)
  
    stream.once('open', () => {
      stream.write(JSON.stringify(data))
      stream.end()
  
      console.log(`Backup is saved successful to path '${filePath}' file  ✅`)
    })
  } catch (err) {
    console.error(`Failed saving backup on path '${filePath}' ❌`)
  }
}