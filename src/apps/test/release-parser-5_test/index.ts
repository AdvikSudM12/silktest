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
import { getReleasesDataJson } from 'src/apps/test/release-parser-5_test/utils/releases-data'
import { uploadingFile, testFilePath } from 'src/apps/test/release-parser-5_test/utils/uploading'

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
    
    // Диагностика путей
    log(`🔍 Текущая рабочая директория: ${process.cwd()}`, 'info')
    log(`🔍 __dirname: ${__dirname}`, 'info')
    
    // Попробуем несколько вариантов путей к paths.json
    const possiblePaths = [
      // Из текущей директории скрипта вверх к корню проекта
      path.join(__dirname, '../../../../pyqt_app/data/paths.json'),
      // Из рабочей директории (если запускаем из silk/)
      path.join(process.cwd(), '../pyqt_app/data/paths.json'),
      // Прямой путь от корня проекта
      path.resolve('P:/emd/silk/silk/pyqt_app/data/paths.json'),
      // Относительные пути
      '../../../pyqt_app/data/paths.json',
      '../../../../pyqt_app/data/paths.json'
    ]
    
    log('🔍 Проверяем возможные пути к paths.json:', 'info')
    let pathsFile = null
    
    for (const testPath of possiblePaths) {
      const resolvedPath = path.resolve(testPath)
      log(`   Проверяем: ${resolvedPath}`, 'info')
      if (fs.existsSync(resolvedPath)) {
        log(`   ✅ Найден!`, 'success')
        pathsFile = resolvedPath
        break
      } else {
        log(`   ❌ Не найден`, 'warning')
      }
    }
    
    if (pathsFile && fs.existsSync(pathsFile)) {
      log(`📄 Читаем paths.json из: ${pathsFile}`, 'success')
      const pathsData = JSON.parse(fs.readFileSync(pathsFile, 'utf-8'))
      log(`📋 Содержимое paths.json: ${JSON.stringify(pathsData, null, 2)}`, 'info')
      
      const excelPath = pathsData.excel_file_path
      const directoryPath = pathsData.directory_path
      
      if (excelPath && directoryPath) {
        log('✅ Пути успешно загружены из paths.json', 'success')
        log(`📄 Excel файл: ${excelPath}`, 'info')
        log(`📁 Директория файлов: ${directoryPath}`, 'info')
        
        // Проверяем существование файлов по загруженным путям
        log(`🔍 Проверяем существование Excel файла: ${excelPath}`, 'info')
        if (fs.existsSync(excelPath)) {
          log(`✅ Excel файл найден`, 'success')
        } else {
          log(`❌ Excel файл не найден по пути из paths.json`, 'error')
        }
        
        log(`🔍 Проверяем существование директории: ${directoryPath}`, 'info')
        if (fs.existsSync(directoryPath)) {
          log(`✅ Директория найдена`, 'success')
        } else {
          log(`❌ Директория не найдена по пути из paths.json`, 'error')
        }
        
        return {
          excelPath: excelPath,
          filesDirectory: directoryPath
        }
      } else {
        log('❌ Пути в paths.json неполные', 'warning')
        log(`   excel_file_path: ${excelPath || 'отсутствует'}`, 'warning')
        log(`   directory_path: ${directoryPath || 'отсутствует'}`, 'warning')
      }
    } else {
      log('❌ Файл paths.json не найден ни по одному из путей', 'warning')
    }
  } catch (error) {
    log(`❌ Ошибка чтения paths.json: ${error}`, 'error')
  }
  
  // Стандартные пути для тестового скрипта
  log('⚠️ Используем стандартные пути для тестирования', 'warning')
  
  // Определяем абсолютные пути к файлам тестового скрипта
  const defaultExcelPath = path.join(__dirname, 'files/releases.xlsx')
  const defaultFilesDirectory = path.join(__dirname, 'files')
  
  log(`📄 Excel файл: ${defaultExcelPath}`, 'info')
  log(`📁 Директория файлов: ${defaultFilesDirectory}`, 'info')
  
  // Проверяем существование стандартных файлов
  log(`🔍 Проверяем существование стандартного Excel файла: ${defaultExcelPath}`, 'info')
  if (fs.existsSync(defaultExcelPath)) {
    log(`✅ Стандартный Excel файл найден`, 'success')
  } else {
    log(`❌ Стандартный Excel файл не найден`, 'error')
  }
  
  log(`🔍 Проверяем существование стандартной директории: ${defaultFilesDirectory}`, 'info')
  if (fs.existsSync(defaultFilesDirectory)) {
    log(`✅ Стандартная директория найдена`, 'success')
  } else {
    log(`❌ Стандартная директория не найдена`, 'error')
  }
  
  return {
    excelPath: defaultExcelPath,
    filesDirectory: defaultFilesDirectory
  }
}

// Функция для валидации окружения через apiConfig
const validateEnvironment = (): boolean => {
  log('Проверка конфигурации API...', 'info')
  
  // Проверяем конфигурацию через apiConfig (как в рабочем скрипте)
  const requiredFields = [
    { key: 'apiUrl', value: apiConfig.apiUrl, env: 'EMD_API' },
    { key: 'spaceId', value: apiConfig.spaceId, env: 'EMD_SPACE' },
    { key: 'token', value: apiConfig.token, env: 'EMD_TOKEN' },
    { key: 'user_id', value: apiConfig.user_id, env: 'EMD_USER_ID' }
  ]
  
  let allValid = true
  
  log('Детальная проверка конфигурации API:', 'info')
  requiredFields.forEach(field => {
    if (field.value) {
      const displayValue = field.key === 'token' ? '***скрыто***' : field.value
      log(`✅ ${field.key}: ${displayValue}`, 'success')
    } else {
      log(`❌ ${field.key}: отсутствует (переменная ${field.env})`, 'error')
      allValid = false
    }
  })
  
  // Показываем все EMD_ переменные для диагностики
  log('Доступные EMD_ переменные:', 'info')
  Object.keys(process.env)
    .filter(key => key.startsWith('EMD_'))
    .forEach(key => {
      const value = process.env[key]
      const displayValue = key.includes('TOKEN') ? '***скрыто***' : (value ? `${value.substring(0, 50)}...` : 'пустая')
      log(`📋 ${key}: ${displayValue}`, 'info')
    })
  
  if (!allValid) {
    log('Некоторые поля конфигурации API отсутствуют', 'error')
    log('💡 Проверьте настройки токенов в PyQt приложении', 'warning')
    return false
  }
  
  log('✅ Конфигурация API полностью настроена', 'success')
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

    // Валидация конфигурации API (как в рабочем скрипте)
    const envValid = validateEnvironment()
    if (!envValid) {
      log('⚠️ Конфигурация API не полная, но продолжаем для диагностики...', 'warning')
      log('💡 Для полной функциональности настройте токены в PyQt приложении', 'warning')
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

    log('Тестирование API подключения...', 'info')
    
    let audioPlatformsList: any
    
    try {
      log('Получение списка аудиоплатформ...', 'info')
      audioPlatformsList = await getTableRows({
        tableName: 'audioPlatformsOptions',
      })

      if (!audioPlatformsList?.data) {
        log('API ответил, но данные отсутствуют', 'error')
        log(`Ответ API: ${JSON.stringify(audioPlatformsList, null, 2)}`, 'info')
        
        if (!envValid) {
          log('💡 Возможная причина: неправильные токены авторизации', 'warning')
          log('💡 Проверьте настройки в PyQt приложении', 'warning')
        }
        
        process.exit(1)
      }

      log(`✅ API работает! Загружено аудиоплатформ: ${audioPlatformsList.data.length}`, 'success')
      
    } catch (apiError: any) {
      log('❌ Ошибка подключения к API:', 'error')
      log(`Тип ошибки: ${apiError.name}`, 'error')
      log(`Сообщение: ${apiError.message}`, 'error')
      
      if (apiError.response) {
        log(`HTTP статус: ${apiError.response.status}`, 'error')
        log(`HTTP данные: ${JSON.stringify(apiError.response.data, null, 2)}`, 'error')
      }
      
      if (apiError.code === 'ENOTFOUND') {
        log('💡 Проблема с DNS/интернет соединением', 'warning')
      } else if (apiError.response?.status === 401) {
        log('💡 Проблема с авторизацией - проверьте токены', 'warning')
      } else if (apiError.response?.status === 403) {
        log('💡 Доступ запрещен - проверьте права пользователя', 'warning')
      } else if (apiError.response?.status >= 500) {
        log('💡 Проблема на стороне сервера', 'warning')
      }
      
      process.exit(1)
    }

    log('Парсинг данных релизов из Excel...', 'info')
    
    let releasesData: any[]
    
    try {
      releasesData = getReleasesDataJson({
        sourceFile: excelPath,
        allCountries: countryCodes.map((item) => item.country),
        allAudioPlatformsList: audioPlatformsList?.data.map(({ data }: any) => data.value)
      })

      if (!releasesData || releasesData.length === 0) {
        log('❌ Не найдены данные релизов для загрузки', 'error')
        log('💡 Проверьте:', 'warning')
        log('   - Есть ли данные в Excel файле', 'warning')
        log('   - Правильно ли заполнены обязательные поля', 'warning')
        log('   - Соответствует ли формат файла ожидаемому', 'warning')
        process.exit(1)
      }

      stats.totalReleases = releasesData.length
      stats.totalTracks = releasesData.reduce((sum, release) => sum + (release?.tracks?.length || 0), 0)

      log(`✅ Найдено релизов для загрузки: ${stats.totalReleases}`, 'success')
      log(`Общее количество треков: ${stats.totalTracks}`, 'info')
      
    } catch (parseError: any) {
      log('❌ Ошибка при парсинге Excel файла:', 'error')
      log(`Сообщение: ${parseError.message}`, 'error')
      
      if (parseError.message.includes('XLSX') || parseError.message.includes('workbook')) {
        log('💡 Проблема с форматом Excel файла', 'warning')
        log('💡 Убедитесь что файл имеет расширение .xlsx', 'warning')
      } else if (parseError.message.includes('sheet') || parseError.message.includes('worksheet')) {
        log('💡 Проблема с листами Excel файла', 'warning')
        log('💡 Проверьте названия листов в файле', 'warning')
      }
      
      process.exit(1)
    }

    // Валидация файлов
    log('Проверка наличия аудиофайлов и обложек...', 'info')
    
    try {
      const filesValid = await validateFiles(releasesData, filesDirectory)
      if (!filesValid) {
        log('⚠️ Некоторые файлы отсутствуют', 'warning')
        log('💡 Проверьте папку с файлами:', 'warning')
        log(`   ${filesDirectory}`, 'warning')
        log('Продолжаем загрузку с доступными файлами...', 'warning')
      } else {
        log('✅ Все необходимые файлы найдены', 'success')
      }
    } catch (fileError: any) {
      log('❌ Ошибка при проверке файлов:', 'error')
      log(`Сообщение: ${fileError.message}`, 'error')
      log('Продолжаем загрузку...', 'warning')
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

        } catch (error: any) {
          stats.failedUploads++
          log(`❌ Ошибка загрузки релиза ${data.name}:`, 'error')
          log(`   Тип ошибки: ${error.name || 'Unknown'}`, 'error')
          log(`   Сообщение: ${error.message}`, 'error')
          
          if (error.response) {
            log(`   HTTP статус: ${error.response.status}`, 'error')
            if (error.response.data) {
              log(`   Детали ошибки: ${JSON.stringify(error.response.data, null, 2)}`, 'error')
            }
          }
          
          if (error.code === 'ENOTFOUND') {
            log('💡 Проблема с интернет соединением', 'warning')
          } else if (error.response?.status === 413) {
            log('💡 Файл слишком большой для загрузки', 'warning')
          } else if (error.response?.status === 422) {
            log('💡 Проблема с валидацией данных', 'warning')
          }
        }
      },
      { iterations: stats.totalReleases, interval: 1000 }
    )

    stats.endTime = new Date()
    log('🎉 ЗАГРУЗКА РЕЛИЗОВ ЗАВЕРШЕНА', 'success')
    showFinalReport(stats)

  } catch (error: any) {
    stats.endTime = new Date()
    log('💥 КРИТИЧЕСКАЯ ОШИБКА:', 'error')
    log(`Тип ошибки: ${error.name || 'Unknown'}`, 'error')
    log(`Сообщение: ${error.message}`, 'error')
    
    if (error.stack) {
      log('Стек вызовов:', 'error')
      log(error.stack, 'error')
    }
    
    if (error.code) {
      log(`Код ошибки: ${error.code}`, 'error')
    }
    
    log('💡 Возможные причины:', 'warning')
    log('   - Проблемы с интернет соединением', 'warning')
    log('   - Неправильные настройки API', 'warning')
    log('   - Поврежденные файлы данных', 'warning')
    log('   - Недостаточно прав доступа', 'warning')
    
    showFinalReport(stats)
    process.exit(1)
  }
})()
