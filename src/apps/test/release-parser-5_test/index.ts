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

// Интерфейсы для типизации
interface UploadStats {
  totalReleases: number
  successfulUploads: number
  failedUploads: number
  totalTracks: number
  successfulTracks: number
  failedTracks: number
  startTime: Date
  endTime?: Date
}

interface PathsConfig {
  excelPath: string
  filesDirectory: string
}

// Функция для логирования с временными метками
const log = (message: string, type: 'info' | 'success' | 'error' | 'warning' = 'info') => {
  const timestamp = new Date().toLocaleTimeString('ru-RU')
  const icons = {
    info: '🔍',
    success: '✅',
    error: '❌',
    warning: '⚠️'
  }
  console.log(`[${timestamp}] ${icons[type]} ${message}`)
}

// Функция для получения путей из paths.json или стандартных путей
const getPaths = (): PathsConfig => {
  try {
    log('Загрузка конфигурации путей...', 'info')
    
    // Путь к файлу paths.json
    const pathsFile = path.join(__dirname, '../../../pyqt_app/data/paths.json')
    
    if (fs.existsSync(pathsFile)) {
      const pathsData = JSON.parse(fs.readFileSync(pathsFile, 'utf-8'))
      const excelPath = pathsData.excel_file_path
      const directoryPath = pathsData.directory_path
      
      if (excelPath && directoryPath) {
        log('Пути успешно загружены из paths.json', 'success')
        log(`Excel файл: ${path.basename(excelPath)}`, 'info')
        log(`Директория файлов: ${path.basename(directoryPath)}`, 'info')
        return {
          excelPath: excelPath,
          filesDirectory: directoryPath
        }
      } else {
        log('Пути в paths.json неполные', 'warning')
      }
    } else {
      log('Файл paths.json не найден', 'warning')
    }
  } catch (error) {
    log(`Ошибка чтения paths.json: ${error}`, 'error')
  }
  
  // Стандартные пути для тестового скрипта
  log('Используем стандартные пути для тестирования', 'warning')
  const defaultExcelPath = 'src/apps/test/release-parser-5_test/files/releases.xlsx'
  const defaultFilesDirectory = 'src/apps/test/release-parser-5_test/files'
  
  log(`Excel файл: ${defaultExcelPath}`, 'info')
  log(`Директория файлов: ${defaultFilesDirectory}`, 'info')
  
  return {
    excelPath: defaultExcelPath,
    filesDirectory: defaultFilesDirectory
  }
}

// Функция для валидации окружения
const validateEnvironment = (): boolean => {
  log('Проверка переменных окружения...', 'info')
  
  const requiredVars = ['USER_ID', 'JWT']
  const missingVars = requiredVars.filter(varName => !process.env[varName])
  
  if (missingVars.length > 0) {
    log(`Отсутствуют переменные окружения: ${missingVars.join(', ')}`, 'error')
    return false
  }
  
  log('Все переменные окружения настроены', 'success')
  return true
}

// Функция для валидации файлов
const validateFiles = async (releasesData: any[], filesDirectory: string): Promise<boolean> => {
  log('Проверка существования файлов...', 'info')
  
  let allFilesExist = true
  let totalFiles = 0
  let existingFiles = 0
  
  for (const data of releasesData) {
    // Проверяем файлы треков
    for (const track of data?.tracks || []) {
      totalFiles++
      const trackPath = `${filesDirectory}/${track.src}`
      if (fs.existsSync(trackPath)) {
        existingFiles++
      } else {
        log(`Файл трека не найден: ${track.src}`, 'error')
        allFilesExist = false
      }
    }

    // Проверяем файл обложки
    if (data.cover) {
      totalFiles++
      const coverPath = `${filesDirectory}/${data.cover}`
      if (fs.existsSync(coverPath)) {
        existingFiles++
      } else {
        log(`Файл обложки не найден: ${data.cover}`, 'error')
        allFilesExist = false
      }
    }
  }
  
  log(`Проверено файлов: ${existingFiles}/${totalFiles}`, existingFiles === totalFiles ? 'success' : 'warning')
  return allFilesExist
}

const getFile = async (fileName: string, filePath: string): Promise<{ name: string, source: string } | null> => {
  if (!fileName) return null

  try {
    const result = await uploadingFile({
      fileName,
      filePath,
      logging: false // Отключаем внутреннее логирование
    })
    
    if (result) {
      log(`Файл загружен: ${fileName}`, 'success')
    }
    
    return result
  } catch (error) {
    log(`Ошибка загрузки файла ${fileName}: ${error}`, 'error')
    return null
  }
}

// Функция для отображения прогресса
const showProgress = (current: number, total: number, item: string) => {
  const percentage = Math.round((current / total) * 100)
  const progressBar = '█'.repeat(Math.floor(percentage / 5)) + '░'.repeat(20 - Math.floor(percentage / 5))
  log(`Прогресс: [${progressBar}] ${percentage}% (${current}/${total}) - ${item}`, 'info')
}

// Функция для отображения финального отчета
const showFinalReport = (stats: UploadStats) => {
  const duration = stats.endTime ? Math.round((stats.endTime.getTime() - stats.startTime.getTime()) / 1000) : 0
  
  console.log('\n' + '='.repeat(60))
  log('ОТЧЕТ О ЗАГРУЗКЕ РЕЛИЗОВ', 'info')
  console.log('='.repeat(60))
  
  log(`Общее время выполнения: ${duration} секунд`, 'info')
  log(`Всего релизов для загрузки: ${stats.totalReleases}`, 'info')
  log(`Успешно загружено релизов: ${stats.successfulUploads}`, 'success')
  log(`Ошибок при загрузке релизов: ${stats.failedUploads}`, stats.failedUploads > 0 ? 'error' : 'info')
  log(`Всего треков: ${stats.totalTracks}`, 'info')
  log(`Успешно загружено треков: ${stats.successfulTracks}`, 'success')
  log(`Ошибок при загрузке треков: ${stats.failedTracks}`, stats.failedTracks > 0 ? 'error' : 'info')
  
  const successRate = Math.round((stats.successfulUploads / stats.totalReleases) * 100)
  log(`Процент успешных загрузок: ${successRate}%`, successRate === 100 ? 'success' : 'warning')
  
  console.log('='.repeat(60) + '\n')
}

(async () => {
  const stats: UploadStats = {
    totalReleases: 0,
    successfulUploads: 0,
    failedUploads: 0,
    totalTracks: 0,
    successfulTracks: 0,
    failedTracks: 0,
    startTime: new Date()
  }

  try {
    log('🚀 ЗАПУСК ЗАГРУЗКИ РЕЛИЗОВ', 'info')
    log('Инициализация системы загрузки...', 'info')

    // Валидация окружения
    if (!validateEnvironment()) {
      log('Загрузка прервана из-за неправильной конфигурации', 'error')
      process.exit(1)
    }

    // Получаем пути к файлам
    const { excelPath, filesDirectory } = getPaths()

    // Проверяем существование файлов
    if (!fs.existsSync(excelPath)) {
      log(`Excel файл не найден: ${excelPath}`, 'error')
      process.exit(1)
    }

    if (!fs.existsSync(filesDirectory)) {
      log(`Директория файлов не найдена: ${filesDirectory}`, 'error')
      process.exit(1)
    }

    log('Получение списка аудиоплатформ...', 'info')
    const audioPlatformsList: any = await getTableRows({
      tableName: 'audioPlatformsOptions',
    })

    if (!audioPlatformsList?.data) {
      log('Не удалось получить список аудиоплатформ', 'error')
      process.exit(1)
    }

    log(`Загружено аудиоплатформ: ${audioPlatformsList.data.length}`, 'success')

    log('Парсинг данных релизов из Excel...', 'info')
    const releasesData = getReleasesDataJson({
      sourceFile: excelPath,
      allCountries: countryCodes.map((item) => item.country),
      allAudioPlatformsList: audioPlatformsList?.data.map(({ data }: any) => data.value)
    })

    stats.totalReleases = releasesData.length
    stats.totalTracks = releasesData.reduce((sum, release) => sum + (release?.tracks?.length || 0), 0)

    log(`Найдено релизов для загрузки: ${stats.totalReleases}`, 'success')
    log(`Общее количество треков: ${stats.totalTracks}`, 'info')

    // Валидация файлов
    const filesValid = await validateFiles(releasesData, filesDirectory)
    if (!filesValid) {
      log('Некоторые файлы отсутствуют. Продолжить загрузку? (y/N)', 'warning')
      // В автоматическом режиме продолжаем
      log('Продолжаем загрузку с доступными файлами...', 'warning')
    }

    log('Начинаем загрузку релизов...', 'info')

    // Загрузка релизов
    await tableFlowIterations(
      async (iteration: number) => {
        const data = releasesData[iteration]
        
        try {
          showProgress(iteration + 1, stats.totalReleases, `Релиз: ${data.name || 'Без названия'}`)

          const tracks = []
          for (const item of data?.tracks || []) {
            const track = await getFile(
              item.name,
              `${filesDirectory}/${item.src}`
            )
      
            if (track) {
              stats.successfulTracks++
            } else {
              stats.failedTracks++
            }

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

          stats.successfulUploads++
          log(`Релиз успешно загружен: ${data.name}`, 'success')

        } catch (error) {
          stats.failedUploads++
          log(`Ошибка загрузки релиза ${data.name}: ${error}`, 'error')
        }
      },
      { iterations: stats.totalReleases, interval: 1000 }
    )

    stats.endTime = new Date()
    log('🎉 ЗАГРУЗКА РЕЛИЗОВ ЗАВЕРШЕНА', 'success')
    showFinalReport(stats)

  } catch (error) {
    stats.endTime = new Date()
    log(`💥 Критическая ошибка: ${error}`, 'error')
    showFinalReport(stats)
    process.exit(1)
  }
})()
