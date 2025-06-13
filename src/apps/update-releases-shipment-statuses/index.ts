// ** Modules Imports
require('dotenv').config()
import fs from 'fs'
import path from 'path'

// ** Source code Imports
import {
  getTableRows,
  getTableRowsCount,
  upsertTableRow
} from 'src/tools/table'
import { tableFlowIterations  } from 'src/tools/flow'
import apiConfig from 'src/configs/api'

(async () => {
  const limit: number = 100
  const query = {
    $and: [
      { user: { $eq: apiConfig.user_id } },
      { 'data.status': { $eq: 'new' } }
    ]
  }

  const { count }: any = await getTableRowsCount({
    tableName: 'releases',
    query
  })

  let releases: any[] = []

  const iterationsCount = Math.ceil(count / limit)

  // Get releases
  await tableFlowIterations(
    async (iteration: number) => {
      const { data }: any = await getTableRows({
        tableName: 'releases',
        page: iteration,
        limit,
        query
      })

      releases = [...releases, ...data]
    },
    { iterations: iterationsCount, interval: 500 }
  )

  const iterations = releases.length

  // Create backup (ПОРТАТИВНОЕ РЕШЕНИЕ)
  const filesDir = path.join(__dirname, 'files')
  const backupPath = path.join(filesDir, 'backup.json')
  
  // Создаем директорию files если её нет
  if (!fs.existsSync(filesDir)) {
    fs.mkdirSync(filesDir, { recursive: true })
    console.log('📁 Создана директория files')
  }
  
  fs.writeFile(backupPath, JSON.stringify(releases), (err) => {
    if (err) throw err

    console.log(`Backup is created ✅ (${backupPath})`)
  })

  // Updating releases
  tableFlowIterations(
    async (iteration: number) => {
      const release = releases[iteration]

      await upsertTableRow({
        tableName: 'releases',
        _id: release._id,
        payload: {
          shouldUploadReleaseToZvonko: true
        },
        notice: 'automated generate silk',
        user: release.user._id
      })

      await new Promise((res) => setTimeout(res, 1000))

      await upsertTableRow({
        tableName: 'releases',
        _id: release._id,
        payload: {
          status: 'moderation',
        },
        notice: 'automated generate silk',
        user: release.user._id
      })
    },
    { iterations, interval: 1000 }
  )
})()
