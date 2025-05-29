// ** Modules Imports
require('dotenv').config()

// ** Source code Imports
import { getTableRows, upsertTableRow } from 'src/tools/table'
import { tableFlowIterations  } from 'src/tools/flow'
import apiConfig from 'src/configs/api'
import countryCodes from 'src/configs/countries-codes'
import releaseConfig from 'src/configs/release'
import { getReleasesDataJson } from 'src/apps/release-parser-5/utils/releases-data'
import { uploadingFile, testFilePath } from 'src/apps/release-parser-5/utils/uploading'

const getFile = async (fileName: string, filePath: string): Promise<{ name: string, source: string } | null> => {
  if (!fileName) return null

  try {
    return await uploadingFile({
      fileName,
      filePath,
      logging: true
    })
  } catch {
    return null
  }
}

(async () => {
  const audioPlatformsList: any = await getTableRows({
    tableName: 'audioPlatformsOptions',
  })

  const releasesData = getReleasesDataJson({
    sourceFile: `src/apps/release-parser-5/files/releases.xlsx`,
    allCountries: countryCodes.map((item) => item.country),
    allAudioPlatformsList: audioPlatformsList?.data.map(({ data }: any) => data.value)
  })

  // Test files paths
  for await (const data of releasesData) {
    // Test tracks files
    for await (const track of data?.tracks) {
      await testFilePath(`src/apps/release-parser-5/files/${track.src}`)
    }

    // Test cover file
    await testFilePath(`src/apps/release-parser-5/files/${data.cover}`)
  }

  const iterations = releasesData.length

  // Uploading releases
  tableFlowIterations(
    async (iteration: number) => {
      const data = releasesData[iteration]

      const tracks = []
      for await (const item of data?.tracks) {
        const track = await getFile(
          item.name,
          `src/apps/release-parser-5/files/${item.src}`
        )
  
        tracks.push({
          ...item,
          src: track?.source || ''
        })
      }

      const cover = await getFile(
        data.name,
        `src/apps/release-parser-5/files/${data.cover}`
      )
  
      const payload = {
        ...releaseConfig,
        ...data,
        tracks,
        cover: { name: cover?.name || '', url: cover?.source || '' }
      }

      await upsertTableRow({
        tableName: 'releases',
        payload,
        notice: 'automated generate silk',
        user: apiConfig.user_id
      })
    },
    { iterations, interval: 1000 }
  )
})()
