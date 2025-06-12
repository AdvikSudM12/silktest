import { Upload } from 'tus-js-client'
import path from 'path'
import * as fs from 'fs'
import mime from 'mime-type/with-db'
import ProgressBarConsole from 'src/tools/progress-bar-console'
import apiConfig from 'src/configs/api'

export const testFilePath = (filePath: string) => {
  try {
    fs.lstatSync(path.resolve(filePath)).isDirectory()
    console.log(`File from "${filePath}" is exist`)
  } catch {
    throw new Error(`No such file or directory "${filePath}"`)
  }
}

const progressBarLog = new ProgressBarConsole()

export const uploadingFile = ({
  fileName,
  filePath,
  logging = false
}: {
  fileName: string
  filePath: string
  logging: boolean
}): Promise<{ name: string, source: string }> => new Promise((resolve, reject) => {
  try {
    // Get the selected file from the input element
    const file = fs.createReadStream(path.resolve(filePath))

    const mimeType = mime.lookup(filePath)
    const filetype = (Array.isArray(mimeType) ? mimeType[0] : mimeType) || 'application/octet-stream'
    const ext = filePath.split('.').pop()
    const filename = `${fileName}.${ext}`

    // Start logging uploading progress
    if (logging) console.log('Uploading file "%s" started', fileName)
    progressBarLog.start()

    // Create a new tus upload
    const upload = new Upload(file, {
      endpoint: apiConfig.tus.endpoint,
      chunkSize: apiConfig.tus.chunkSize,
      removeFingerprintOnSuccess: true,
      headers: {
        Authorization: `${apiConfig.headerTokenKeyName} ${apiConfig.token}`
      },
      retryDelays: [0, 3000, 5000, 10000, 20000],
      metadata: {
        name: encodeURIComponent(filename),
        filename,
        filetype,
      },
      onError: (error) => {
        progressBarLog.end()
        if (logging) console.error('Uploading file "%s" failed because: %s', fileName, error)
        reject(`Uploading file "${fileName}" failed because: ${error}`)
      },
      onProgress: (bytesUploaded, bytesTotal) => {
        const percentage = ((bytesUploaded / bytesTotal) * 100)
        progressBarLog.write(percentage, `${bytesUploaded}x${bytesTotal}bytes`)
      },
      onSuccess: () => {
        progressBarLog.end()

        if (upload.url) {
          if (logging) console.log('Uploading file "%s" completed', fileName)

          const name = upload.url.split('/').pop() as string

          resolve({ name, source: `${apiConfig.tus.staticUrl}/${name}` })
        } else {
          if (logging) console.error('TUS server is not return link for "%s" file', fileName)
          reject('TUS server is not return link')
        }
      },
    })

    // Check if there are any previous uploads to continue.
    upload.findPreviousUploads().then((previousUploads) => {
      // Found previous uploads so we select the first one.
      if (previousUploads.length) upload.resumeFromPreviousUpload(previousUploads[0])

      // Start the upload
      upload.start()
    })
  } catch (error) {
    if (logging) console.error('Unexpected error by uploading "%s" file: %s', fileName, error)
    reject(`Unexpected error by uploading "${fileName}" file: ${error}`)
  }
})
