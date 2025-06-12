// ** Modules Imports
require('dotenv').config()
import fs from 'fs'
import path from 'path'

// ** Source code Imports
import { getTableRows, upsertTableRow } from 'src/tools/table'
import { tableFlowIterations  } from 'src/tools/flow'
import apiConfig from 'src/configs/api'
import countryCodes from 'src/configs/countries-codes'
import releaseConfig from 'src/configs/release'
import { getReleasesDataJson } from 'src/apps/release-parser-5/utils/releases-data'
import { uploadingFile, testFilePath } from 'src/apps/release-parser-5/utils/uploading'

// Функция для получения путей из paths.json или стандартных путей
const getPaths = (): { excelPath: string, filesDirectory: string } => {
  try {
    // Путь к файлу paths.json
    const pathsFile = path.join(__dirname, '../../../pyqt_app/data/paths.json')
    
    if (fs.existsSync(pathsFile)) {
      const pathsData = JSON.parse(fs.readFileSync(pathsFile, 'utf-8'))
      const excelPath = pathsData.excel_file_path
      const directoryPath = pathsData.directory_path
      
      if (excelPath && directoryPath) {
        console.log('📁 Пути загружены из paths.json')
        console.log(`📄 Excel файл: ${excelPath}`)
        console.log(`📂 Директория файлов: ${directoryPath}`)
        return {
          excelPath: excelPath,
          filesDirectory: directoryPath
        }
      }
    }
  } catch (error) {
    console.log('⚠️ Ошибка чтения paths.json, используем стандартные пути')
  }
  
  // Стандартные пути для тестового скрипта
  console.log('📁 Используем стандартные пути')
  const defaultExcelPath = 'src/apps/test/release-parser-5_test/files/releases.xlsx'
  const defaultFilesDirectory = 'src/apps/test/release-parser-5_test/files'
  
  console.log(`📄 Excel файл: ${defaultExcelPath}`)
  console.log(`📂 Директория файлов: ${defaultFilesDirectory}`)
  
  return {
    excelPath: defaultExcelPath,
    filesDirectory: defaultFilesDirectory
  }
}

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
  // Получаем пути к файлам
  const { excelPath, filesDirectory } = getPaths()

  const audioPlatformsList: any = await getTableRows({
    tableName: 'audioPlatformsOptions',
  })

  const releasesData = getReleasesDataJson({
    sourceFile: excelPath,
    allCountries: countryCodes.map((item) => item.country),
    allAudioPlatformsList: audioPlatformsList?.data.map(({ data }: any) => data.value)
  })

  // Test files paths
  for await (const data of releasesData) {
    // Test tracks files
    for await (const track of data?.tracks) {
      await testFilePath(`${filesDirectory}/${track.src}`)
    }

    // Test cover file
    await testFilePath(`${filesDirectory}/${data.cover}`)
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
          `${filesDirectory}/${item.src}`
        )
  
        tracks.push({
          ...item,
          src: track?.source || ''
        })
      }

      const cover = await getFile(
        data.name,
        `${filesDirectory}/${data.cover}`
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
