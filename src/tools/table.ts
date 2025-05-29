// Modules Imports
import axios from 'axios'

// Source code Imports
import apiConfig from 'src/configs/api'

axios.defaults.headers.common.Authorization = `${apiConfig.headerTokenKeyName} ${apiConfig.token}`

export const getTableColumns = async ({
  spaceId = apiConfig.spaceId,
  tableName
}: {
  spaceId?: string
  tableName: string
}) => {
  return new Promise(async (resolve, regect) => {
    try {
      const { data } = await axios.get(`${apiConfig.apiUrl}/${spaceId}/database/${tableName}/column`)

      console.log(`Get columns from "${tableName}" table  in "${spaceId}" space is success ✅`)
      resolve(data)
    } catch (err) {
      console.error(`Error get columns from "${tableName}" table  in "${spaceId}" space ❌`)
      regect(err)
    }
  })
}

export const getTableRows = async ({
  spaceId = apiConfig.spaceId,
  tableName,
  limit = 100,
  page = 0,
  query = {}
}: {
  spaceId?: string
  tableName: string
  limit?: number
  page?: number
  query?: Record<string, any>
}) => {
  return new Promise(async (resolve, regect) => {
    try {
      const { data } = await axios.post(`${apiConfig.apiUrl}/${spaceId}/database/${tableName}/row`, {
        limit,
        page,
        query
      })

      console.log(`Get rows from "${tableName}" table  in "${spaceId}" space is success ✅`)
      resolve(data)
    } catch (err) {
      console.error(`Error get rows from "${tableName}" table  in "${spaceId}" space ❌`)
      regect(err)
    }
  })
}

export const getTableRowsCount = async ({
  spaceId = apiConfig.spaceId,
  tableName,
  query = {}
}: {
  spaceId?: string
  tableName: string
  query?: Record<string, any>
}) => {
  return new Promise(async (resolve, regect) => {
    try {
      const { data } = await axios.post(`${apiConfig.apiUrl}/${spaceId}/database/${tableName}/row/count`, {
        query
      })

      console.log(`Get rows count from "${tableName}" table  in "${spaceId}" space is success ✅`)
      resolve(data)
    } catch (err) {
      console.error(`Error get rows count from "${tableName}" table  in "${spaceId}" space ❌`)
      regect(err)
    }
  })
}

export const upsertTableRow = async ({
  spaceId = apiConfig.spaceId,
  tableName,
  _id,
  payload,
  notice,
  user,
}: {
  spaceId?: string
  tableName: string
  _id?: string
  payload: Record<string, any>
  notice: string
  user?: string
}) => {
  return new Promise(async (resolve, regect) => {
    try {
      const body: any = {
        data: payload,
        notice
      }

      if (_id) body._id = _id
      if (user) body.user = user

      const { data } = await axios.put(`${apiConfig.apiUrl}/${spaceId}/database/${tableName}/row`, body)

      console.log(`Upsert row from "${tableName}" table  in "${spaceId}" space is success ✅`)
      resolve(data)
    } catch (err) {
      console.error(`Error upsert row from "${tableName}" table  in "${spaceId}" space ❌`)
      console.error(err)
      regect(err)
    }
  })
}

export const deleteTableRow = async ({
  spaceId = apiConfig.spaceId,
  tableName,
  _id
}: {
  spaceId?: string
  tableName: string
  _id: string
}) => {
  return new Promise(async (resolve, regect) => {
    try {
      const { data } = await axios.delete(`${apiConfig.apiUrl}/${spaceId}/database/${tableName}/row`, { data: { _id } })

      console.log(`Delele row from "${tableName}" table  in "${spaceId}" space is success ✅`)
      resolve(data)
    } catch (err) {
      console.error(`Error delete row from "${tableName}" table  in "${spaceId}" space ❌`)
      console.error(err)
      regect(err)
    }
  })
}